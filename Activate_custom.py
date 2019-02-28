# ----------------------------------------------------------------------
# |
# |  Activate_custom.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2018-05-07 08:59:57
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2018-19.
# |  Distributed under the Boost Software License, Version 1.0.
# |  (See accompanying file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# |
# ----------------------------------------------------------------------
"""Performs repository-specific activation activities."""

import os
import sys

sys.path.insert(0, os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL"))
from RepositoryBootstrap.SetupAndActivate import CommonEnvironment, CurrentShell

del sys.path[0]

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# <Class '<name>' has no '<attr>' member> pylint: disable = E1101
# <Unrearchable code> pylint: disable = W0101
# <Unused argument> pylint: disable = W0613

# ----------------------------------------------------------------------
def GetCustomActions(
    output_stream,
    configuration,
    version_specs,
    generated_dir,
    debug,
    verbose,
    fast,
    repositories,
    is_mixin_repo,
):
    """
    Returns an action or list of actions that should be invoked as part of the activation process.

    Actions are generic command line statements defined in 
    <Common_Environment>/Libraries/Python/CommonEnvironment/v1.0/CommonEnvironment/Shell/Commands/__init__.py
    that are converted into statements appropriate for the current scripting language (in most
    cases, this is Bash on Linux systems and Batch or PowerShell on Windows systems.
    """

    actions = []

    for tool, version_infos in [
        (
            "cmake",
            [
                (
                    "v3.13.4",
                    [("Windows", "CFB94E2E356F1E0CF8574B345798410BA1B98C3F5B8F8D568E87879811C2A9F1"), ("Linux", "B786120D2D1741ABFF9E2E69B7B94139216CA800559F28707522658568CCB98F")],
                ),
            ],
        ),
        (
            "ninja",
            [
                (
                    "v1.9.0",
                    [("Windows", "4594F25878EC07BC25795BA27DEF1F83D8F3D2B5FF62335A0F1A25154407384D"), ("Linux", "D53ACC6579E21FC5B36BA923C758F1B53C85B0177765F014C43B9B4B48E7166E")],
                ),
            ],
        ),
    ]:
        for version, operating_system_infos in version_infos:
            for operating_system, hash in operating_system_infos:
                if CurrentShell.CategoryName != operating_system:
                    continue

                tool_dir = os.path.join(_script_dir, "Tools", tool, version, operating_system)
                assert os.path.isdir(tool_dir), tool_dir

                if not actions:
                    actions.append(CurrentShell.Commands.Message(""))

                actions.append(
                    CurrentShell.Commands.Call(
                        'python "{script}" Verify "{tool} - {version}" "{dir}" {hash}'.format(
                            script=os.path.join(
                                os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL"),
                                "RepositoryBootstrap",
                                "SetupAndActivate",
                                "AcquireBinaries.py",
                            ),
                            tool=tool,
                            version=version,
                            dir=tool_dir,
                            hash=hash,
                        ),
                    ),
                )

        actions.append(CurrentShell.Commands.Message(""))

    return actions


# ----------------------------------------------------------------------
def GetCustomScriptExtractors():
    """
    Returns information that can be used to enumerate, extract, and generate documentation
    for scripts stored in the Scripts directory in this repository and all repositories
    that depend upon it.

    ****************************************************
    Note that it is very rare to have the need to implement 
    this method. In most cases, it is safe to delete it.
    ****************************************************

    There concepts are used with custom script extractors:

        - DirGenerator:             Method to enumerate sub-directories when searching for scripts in a
                                    repository's Scripts directory.

                                        def Func(directory, version_sepcs) -> [ (subdir, should_recurse), ... ] 
                                                                              [ subdir, ... ]
                                                                              (subdir, should_recurse)
                                                                              subdir

        - CreateCommands:           Method that creates the shell commands to invoke a script.

                                        def Func(script_filename) -> [ command, ...]
                                                                     command
                                                                     None           # Indicates not supported
        
        - CreateDocumentation:      Method that extracts documentation from a script.

                                        def Func(script_filename) -> documentation string

        - ScriptNameDecorator:      Returns a new name for the script.

                                        def Func(script_filename) -> name string

    See <Common_Environment>/Activate_custom.py for an example of how script extractors
    are used to process Python and PowerShell scripts.
    """

    return
