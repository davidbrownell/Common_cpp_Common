# ----------------------------------------------------------------------
# |
# |  CMakeHelpers.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-21 10:12:30
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Tools that operate on cmake in parallel"""

import os
import sys
import textwrap
import threading

import CommonEnvironment
from CommonEnvironment.CallOnExit import CallOnExit
from CommonEnvironment import CommandLine
from CommonEnvironment import FileSystem
from CommonEnvironment import Process
from CommonEnvironment.Shell.All import CurrentShell
from CommonEnvironment.StreamDecorator import StreamDecorator
from CommonEnvironment import TaskPool

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

@CommandLine.EntryPoint
@CommandLine.Constraints(
    working_dir=CommandLine.DirectoryTypeInfo(
        arity="?",
    ),
    cmake_param=CommandLine.StringTypeInfo(
        arity="*",
    ),
    output_stream=None,
)
def Generate(
    working_dir=os.getcwd(),
    generator="Ninja",
    cmake_param=None,
    force=False,
    build=False,
    test=False,
    output_stream=sys.stdout,
    verbose=False,
):
    """Generates build files for multiple build configurations"""

    cmake_params = cmake_param
    del cmake_param

    if test and not build:
        raise CommandLine.UsageException("'/build' must be provided if '/test' is provided")

    command_line_template = 'cmake -G {generator} -S "{working_dir}" -B "{{build_dir}}" -DCMAKE_BUILD_TYPE={{configuration}}{params} {root_dir}'.format(
        generator=generator,
        working_dir=working_dir,
        params=" ".join(cmake_params),
        root_dir=os.path.join(*([".."] * 5)),
    )

    # ----------------------------------------------------------------------
    def Callback(
        test_lock,
        configuration,
        build_dir,
        output_stream,
        on_status_update,
    ):
        on_status_update("Generating")
        _PrintHeader("Generate Output", output_stream)

        if os.path.isdir(build_dir):
            if not force:
                output_stream.write("The output dir '{}' already exists and will not be overwritten.\n".format(build_dir))
                return 1

            FileSystem.RemoveTree(build_dir)

        FileSystem.MakeDirs(build_dir)

        result = Process.Execute(
            command_line_template.format(
                build_dir=build_dir,
                configuration=configuration,
            ),
            output_stream,
        )
        if result != 0:
            return result

        if build:
            on_status_update("Building")
            _PrintHeader("Build Output", output_stream)

            result = _BuildImpl(build_dir, output_stream)
            if result != 0:
                return result

        if test:
            on_status_update("Testing (Waiting)")
            _PrintHeader("Test Output", output_stream)

            with test_lock:
                on_status_update("Testing")
                    
                result = _TestImpl(build_dir, output_stream)
                if result != 0:
                    return result

        return 0

    # ----------------------------------------------------------------------

    return _Impl(
        working_dir,
        output_stream,
        verbose,
        Callback,
    )


# ----------------------------------------------------------------------
@CommandLine.EntryPoint
@CommandLine.Constraints(
    working_dir=CommandLine.DirectoryTypeInfo(
        arity="?",
    ),
    output_stream=None,
)
def Build(
    working_dir=os.getcwd(),
    test=False,
    output_stream=sys.stdout,
    verbose=False,
):
    """Executes builds for multiple configurations"""

    # ----------------------------------------------------------------------
    def Callback(
        test_lock,
        configuration,
        build_dir,
        output_stream,
        on_status_update,
    ):
        if not os.path.isdir(build_dir):
            output_stream.write("ERROR: '{}' is not a valid directory.".format(build_dir))
            return -1

        on_status_update("Building")
        _PrintHeader("Build Output", output_stream)

        result = _BuildImpl(build_dir, output_stream)
        if result != 0:
            return result

        if test:
            on_status_update("Testing (Waiting)")
            _PrintHeader("Test Output", output_stream)

            with test_lock:
                on_status_update("Testing")

                result = _TestImpl(build_dir, output_stream)
                if result != 0:
                    return result

        return 0

    # ----------------------------------------------------------------------

    return _Impl(
        working_dir,
        output_stream,
        verbose,
        Callback,
    )


# ----------------------------------------------------------------------
@CommandLine.EntryPoint
@CommandLine.Constraints(
    working_dir=CommandLine.DirectoryTypeInfo(
        arity="?",
    ),
    output_stream=None,
)
def Test(
    working_dir=os.getcwd(),
    output_stream=sys.stdout,
    verbose=False,
):
    """Executes tests for multiple configurations"""

    # ----------------------------------------------------------------------
    def Callback(
        test_lock,
        configuration,
        build_dir,
        output_stream,
        on_status_update,
    ):
        if not os.path.isdir(build_dir):
            output_stream.write("ERROR: '{}' is not a valid directory.".format(build_dir))
            return -1

        on_status_update("Testing (Waiting)")
        _PrintHeader("Test Output", output_stream)

        with test_lock:
            on_status_update("Testing")

            result = _TestImpl(build_dir, output_stream)
            if result != 0:
                return result

        return 0

    # ----------------------------------------------------------------------

    return _Impl(
        working_dir,
        output_stream,
        verbose,
        Callback,
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _Impl(working_dir, output_stream, verbose, callback_func):
    if not os.path.isfile(os.path.join(working_dir, "CMakeLists.txt")):
        raise CommandLine.UsageException("The directory '{}' does not contain the file 'CMakeLists.txt'".format(working_dir))

    with StreamDecorator(output_stream).DoneManager(
        line_prefix="",
        prefix="\nResults: ",
        suffix="\n",
    ) as dm:
        build_dir_prefix = [
            "build",
            CurrentShell.CategoryName,
            os.getenv("DEVELOPMENT_ENVIRONMENT_CPP_COMPILER_NAME"),
            os.getenv("DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE"),
        ]

        configuration_types = ["Debug", "Release"]

        # Tests cannot execute in parallel, as they must be invoked from the build
        # dir (which impacts the global working directory)
        test_lock = threading.Lock()

        # ----------------------------------------------------------------------
        def Impl(task_index, output_stream, on_status_update):
            configuration = configuration_types[task_index]
            build_dir = os.path.join(*([working_dir] + build_dir_prefix + [configuration]))
            
            return callback_func(
                test_lock, 
                configuration,
                build_dir,
                output_stream,
                on_status_update,
            )

        # ----------------------------------------------------------------------

        dm.result = TaskPool.Execute(
            [TaskPool.Task(configuration_type, Impl) for configuration_type in configuration_types],
            dm.stream,
            progress_bar=True,
            verbose=verbose,
        )

        return dm.result


# ----------------------------------------------------------------------
def _PrintHeader(name, output_stream):
    output_stream.write(
        textwrap.dedent(
            """\


            ----------------------------------------------------------------------
            |  {}
            ----------------------------------------------------------------------
            
            """,
        ).format(name),
    )


# ----------------------------------------------------------------------
def _BuildImpl(build_dir, output_stream):
    return Process.Execute(
        'cmake --build "{build_dir}"'.format(
            build_dir=build_dir,
        ),
        output_stream,
    )


# ----------------------------------------------------------------------
def _TestImpl(build_dir, output_stream):
    # Tests must be executed from the build dir
    prev_dir = os.getcwd()
    os.chdir(build_dir)
    with CallOnExit(lambda: os.chdir(prev_dir)):
        return Process.Execute("ctest --parallel", output_stream)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        sys.exit(CommandLine.Main())
    except KeyboardInterrupt:
        pass