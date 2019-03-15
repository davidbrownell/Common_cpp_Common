# ----------------------------------------------------------------------
# |
# |  clang-formatProxy.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-03-09 23:43:20
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""\
Updates C++ source code with the CppFormatter while presenting an
interface similar to the clang-format tool.

This proxy is useful for tools that are configured to invoke clang-format
(see the list below) by presenting a consistent interface. Note that most
tools that invoke clang-format expect to invoke an executable; because of
this, Build.py will convert this script into a binary that is available at
<repo_root>/Tools/clang-formatProxy/v1.0/<os>.

The following are instructions to configure different editors to use this proxy:

VSCODE
------
Update `settings.json` with the following information

{
    "C_Cpp.clang_format_path": "clang-formatProxy",
    "editor.formatOnSaveTimeout": 10000
}
"""

import os
import sys

import CommonEnvironment
from CommonEnvironment.CallOnExit import CallOnExit
from CommonEnvironment import CommandLine
from CommonEnvironment import FileSystem
from CommonEnvironment import Process
from CommonEnvironment.Shell.All import CurrentShell

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
@CommandLine.EntryPoint
@CommandLine.Constraints(
    arg=CommandLine.StringTypeInfo(
        arity="+",
    ),
    output_stream=None,
)
def EntryPoint(
    arg,
    output_stream=sys.stdout,
):
    args = arg
    del arg

    # One of the args will be the filename
    input_filename = None

    for arg in args:
        if arg.startswith("-assume-filename="):
            input_filename = arg[len("-assume-filename=") :]
            break

    if input_filename is None:
        raise Exception("Unable to extract the filename from '{}'".format(args))

    # Write the contents from stdin to a temp file
    input_content = sys.stdin.read()
    assert input_content

    temp_filename = CurrentShell.CreateTempFilename(os.path.splitext(input_filename)[1])

    with open(temp_filename, "w") as f:
        f.write(input_content)

    with CallOnExit(lambda: FileSystem.RemoveFile(temp_filename)):
        # Invoke the script
        command_line = '"{script}" Format "{filename}" /quiet "/hint_filename={original_filename}"'.format(
            script=CurrentShell.CreateScriptName("Formatter"),
            filename=temp_filename,
            original_filename=input_filename,
        )

        result, formatted_output = Process.Execute(command_line)

    output_stream.write(formatted_output)
    return result


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        sys.exit(CommandLine.Main())
    except KeyboardInterrupt:
        pass
