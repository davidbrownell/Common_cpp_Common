# ----------------------------------------------------------------------
# |
# |  Build.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-03-09 23:47:06
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-22
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Builds clang-formatProxy"""

import os
import sys

import CommonEnvironment
from CommonEnvironment import BuildImpl
from CommonEnvironment import CommandLine
from CommonEnvironment import FileSystem
from CommonEnvironment import Process
from CommonEnvironment.Shell.All import CurrentShell
from CommonEnvironment.StreamDecorator import StreamDecorator

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

EXCLUDE_MODULES                             = [
    "colorama",
    "concurrent",
    "ctypes",
    "distutils",
    "email",
    "html",
    "http",
    "logging",
    "multiprocessing",
    "pkg_resources",
    "pydoc_data",
    "tqdm",
    "unittest",
    "urllib",
    "win32com",
    "xml",
    "xmlrpc",
]

# ----------------------------------------------------------------------
@CommandLine.EntryPoint()
@CommandLine.Constraints(
    output_stream=None,
)
def Build(
    output_stream=sys.stdout,
):
    """Builds clang-formatProxy"""

    with StreamDecorator(output_stream).DoneManager(
        line_prefix="",
        prefix="\nResults: ",
        suffix="\n",
    ) as dm:
        command_line = '"{script}" Compile "/input={input}" "/output_dir={output_dir}" /no_bundle {exclude_modules}'.format(
            script=CurrentShell.CreateScriptName("CxFreezeCompiler"),
            input=os.path.join(_script_dir, "clang-formatProxy.py"),
            output_dir=os.path.join(
                _script_dir,
                "..",
                "..",
                "Tools",
                "clang-formatProxy",
                "v1.0",
                CurrentShell.CategoryName,
            ),
            exclude_modules=" ".join(
                ['"/exclude_module={}"'.format(module) for module in EXCLUDE_MODULES],
            ),
        )

        dm.result = Process.Execute(command_line, dm.stream)
        if dm.result != 0:
            return dm.result

        return dm.result


# ----------------------------------------------------------------------
@CommandLine.EntryPoint()
@CommandLine.Constraints(
    output_stream=None,
)
def Clean(
    output_stream=sys.stdout,
):
    output_stream.write("Clean functionality is not enabled for this build.\n")
    return 0


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        sys.exit(
            BuildImpl.Main(
                BuildImpl.Configuration(
                    "clang-formatProxy",
                    requires_output_dir=False,
                ),
            ),
        )
    except KeyboardInterrupt:
        pass
