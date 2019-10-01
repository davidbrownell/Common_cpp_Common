# ----------------------------------------------------------------------
# |
# |  CMakeCompiler.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-04 08:55:24
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the Compiler object and entry point"""

import os
import re
import shutil
import sys
import textwrap

import CommonEnvironment
from CommonEnvironment.CallOnExit import CallOnExit
from CommonEnvironment import CommandLine
from CommonEnvironment import FileSystem
from CommonEnvironment import Interface
from CommonEnvironment import Process
from CommonEnvironment.Shell.All import CurrentShell
from CommonEnvironment.StreamDecorator import StreamDecorator
from CommonEnvironment import StringHelpers

from CommonEnvironment.CompilerImpl import Compiler as CompilerMod
from CommonEnvironment.CompilerImpl.InputProcessingMixin.IndividualInputProcessingMixin import (
    IndividualInputProcessingMixin,
)
from CommonEnvironment.CompilerImpl.InvocationMixin.CommandLineInvocationMixin import (
    CommandLineInvocationMixin,
)
from CommonEnvironment.CompilerImpl.InvocationQueryMixin.ConditionalInvocationQueryMixin import (
    ConditionalInvocationQueryMixin,
)
from CommonEnvironment.CompilerImpl.OutputMixin.MultipleOutputMixin import (
    MultipleOutputMixin,
)

from CommonEnvironment.TypeInfo.FundamentalTypes.DirectoryTypeInfo import (
    DirectoryTypeInfo,
)

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
@Interface.staticderived
class Compiler(
    IndividualInputProcessingMixin,
    CommandLineInvocationMixin,
    ConditionalInvocationQueryMixin,
    MultipleOutputMixin,
    CompilerMod.Compiler,
):
    """Compiles a CMAKE directory"""

    # ----------------------------------------------------------------------
    # |  Properties
    Name                                    = Interface.DerivedProperty("CMake")
    Description                             = Interface.DerivedProperty("Compiles a CMake directory.")
    InputTypeInfo                           = Interface.DerivedProperty(DirectoryTypeInfo())

    # ----------------------------------------------------------------------
    # |  Methods
    @staticmethod
    @Interface.override
    def IsSupportedContent(filename):
        return os.path.isfile(os.path.join(filename, "CMakeLists.txt"))

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.override
    def IsSupportedTestItem(item):
        return item.endswith("Tests")

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.override
    def CreateInvokeCommandLine(context, verbose_stream):
        return 'cmake --build "{build}"'.format(
            build=context["output_dir"],
        )

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.override
    def RemoveTemporaryArtifacts(context):
        output_dir = context["output_dir"]

        # Move GCC-generated profile data to the output dir
        for filename in FileSystem.WalkFiles(
            output_dir,
            include_file_extensions=[".gcno", ".gcda"],
        ):
            dest_filename = os.path.join(output_dir, os.path.basename(filename))
            if dest_filename == filename:
                continue

            if os.path.isfile(dest_filename):
                raise Exception(
                    "The file '{}' already exists ({})".format(dest_filename, filename),
                )

            shutil.copyfile(filename, dest_filename)

        for potential_dir in ["CMakeFiles", "Testing"]:
            potential_dir = os.path.join(output_dir, potential_dir)
            FileSystem.RemoveTree(potential_dir)

        for potential_file in ["CMakeCache.txt", "cmake_install.cmake", "Makefile"]:
            potential_file = os.path.join(output_dir, potential_file)
            FileSystem.RemoveFile(potential_file)

        remove_extensions = set([".ilk"])

        for item in os.listdir(output_dir):
            if os.path.splitext(item)[1] not in remove_extensions:
                continue

            fullpath = os.path.join(output_dir, item)
            FileSystem.RemoveFile(fullpath)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @classmethod
    @Interface.override
    def _GetOptionalMetadata(cls):
        return [
            (
                "generator",
                None
                if os.getenv("DEVELOPMENT_ENVIRONMENT_CPP_USE_DEFAULT_CMAKE_GENERATOR")
                else "Ninja",
            ),
            ("is_debug", True),
            ("cmake_debug_output", False),
            ("use_unicode", False),
            ("static_crt", True),
            ("is_profile", False),
            ("disable_debug_info", False),
            ("disable_aslr", False),
        ] + super(Compiler, cls)._GetOptionalMetadata()

    # ----------------------------------------------------------------------
    @classmethod
    @Interface.override
    def _GetRequiredContextNames(cls):
        return ["output_dir"] + super(Compiler, cls)._GetRequiredContextNames()

    # ----------------------------------------------------------------------
    @classmethod
    @Interface.override
    def _CreateContext(cls, metadata, status_stream):
        if "output_dir" not in metadata:
            return metadata

        # Invoke cmake to get a list of the generated files. The best way that I have found
        # to do this is to parse generated dot files (as we don't want to get into the business
        # of parsing cmake files).
        temp_directory = CurrentShell.CreateTempDirectory()
        with CallOnExit(lambda: FileSystem.RemoveTree(temp_directory)):
            dot_filename = os.path.join(temp_directory, "generated.dot")

            command_line_options = [
                '-S "{}"'.format(metadata["input"]),
                '-B "{}"'.format(metadata["output_dir"]),
                '"--graphviz={}"'.format(dot_filename),
                "-DCMAKE_BUILD_TYPE={}".format(
                    "Debug" if metadata["is_debug"] else "Release",
                ),
                "-DCppCommon_CMAKE_DEBUG_OUTPUT={}".format(
                    "ON" if metadata["cmake_debug_output"] else "OFF",
                ),
                "-DCppCommon_UNICODE={}".format(
                    "ON" if metadata["use_unicode"] else "OFF",
                ),
                "-DCppCommon_STATIC_CRT={}".format(
                    "ON" if metadata["static_crt"] else "OFF",
                ),
                "-DCppCommon_CODE_COVERAGE={}".format(
                    "ON" if metadata["is_profile"] else "OFF",
                ),
                "-DCppCommon_NO_DEBUG_INFO={}".format(
                    "ON" if metadata["disable_debug_info"] else "OFF",
                ),
                "-DCppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION={}".format(
                    "ON" if not metadata["disable_aslr"] else "OFF",
                ),
            ]

            if metadata["generator"]:
                command_line_options.append('-G "{}"'.format(metadata["generator"]))

            result, output = Process.Execute(
                "cmake {}".format(" ".join(command_line_options)),
            )
            if result != 0:
                raise Exception(
                    textwrap.dedent(
                        """\
                        cmake failed ({}):
                            {}
                        """,
                    ).format(result, StringHelpers.LeftJustify(output, 4)),
                )

            # Parse the dot file
            regex = re.compile(
                r"\"node\d+\"\s*\[\s*label=\"(?P<name>.+?)\" shape=\"house\"\s*\];",
            )

            with open(dot_filename) as f:
                content = f.read()

            output_filenames = []

            for match in regex.finditer(content):
                output_filenames.append(
                    os.path.join(
                        metadata["output_dir"],
                        CurrentShell.CreateExecutableName(match.group("name")),
                    ),
                )

            metadata["output_filenames"] = output_filenames

        return super(Compiler, cls)._CreateContext(metadata, status_stream)


# ----------------------------------------------------------------------
@CommandLine.EntryPoint
@CommandLine.Constraints(
    output_dir=CommandLine.DirectoryTypeInfo(
        ensure_exists=False,
    ),
    input=CommandLine.DirectoryTypeInfo(
        arity="+",
    ),
    generator=CommandLine.StringTypeInfo(
        arity="?",
    ),
    output_stream=None,
)
def Compile(
    output_dir,
    input,
    generator=None,
    release=False,
    profile=False,
    disable_debug_info=False,
    no_static_crt=False,
    use_unicode=False,
    output_stream=sys.stdout,
    verbose=False,
):
    """Compiles a CMake directory"""

    inputs = input
    del input

    return CompilerMod.CommandLineCompile(
        Compiler,
        inputs,
        StreamDecorator(output_stream),
        verbose,
        output_dir=output_dir,
        is_debug=not release,
        is_profile=profile,
        disable_debug_info=disable_debug_info,
        static_crt=not no_static_crt,
        use_unicode=use_unicode,
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        sys.exit(CommandLine.Main())
    except KeyboardInterrupt:
        pass
