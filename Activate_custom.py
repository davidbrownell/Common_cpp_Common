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

from collections import OrderedDict

sys.path.insert(0, os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL"))
from RepositoryBootstrap import Constants as RepositoryBootstrapConstants
from RepositoryBootstrap.SetupAndActivate import CommonEnvironment, CurrentShell
from RepositoryBootstrap.SetupAndActivate import DynamicPluginArchitecture
from RepositoryBootstrap.Impl.ActivationActivity import ActivationActivity

del sys.path[0]

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# Ensure that we are loading custom data from this dir and not some other repository.
sys.modules.pop("_custom_data", None)

from _custom_data import _CUSTOM_DATA

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

    if fast:
        actions.append(
            CurrentShell.Commands.Message(
                "** FAST: Activating without verifying content. ({})".format(
                    _script_fullpath,
                ),
            ),
        )
    else:
        for tool, version_infos in _CUSTOM_DATA:
            for version, operating_system_infos in version_infos:
                for operating_system, hash in operating_system_infos:
                    if CurrentShell.CategoryName != operating_system:
                        continue

                    tool_dir = os.path.join(
                        _script_dir,
                        "Tools",
                        tool,
                        version,
                        operating_system,
                    )
                    assert os.path.isdir(tool_dir), tool_dir

                    actions.append(
                        CurrentShell.Commands.Execute(
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

    # Get the cmake path
    cmake_dirs = []

    version_info = version_specs.Libraries.get("cmake", {})

    for repository in repositories:
        for directory in _EnumLibraryDependencies("cmake", repository.Root, version_info):
            cmake_dirs.append(directory.replace("\\", "/"))

    actions.append(
        CurrentShell.Commands.Augment(
            "DEVELOPMENT_ENVIRONMENT_CMAKE_MODULE_PATH",
            cmake_dirs,
        ),
    )

    # Load all libraries
    includes = []

    version_info = version_specs.Libraries.get("C++", {})

    for repository in repositories:
        for directory in _EnumLibraryDependencies("C++", repository.Root, version_info):
            potential_include = os.path.join(directory, "include")
            if os.path.isdir(potential_include):
                includes.append(potential_include)
            else:
                includes.append(directory)

    actions.append(CurrentShell.Commands.Augment("INCLUDE", includes))

    # Add a compiler name (that will likely be overridden by a repo that depends on this one)
    actions.append(
        CurrentShell.Commands.Set(
            "DEVELOPMENT_ENVIRONMENT_CPP_COMPILER_NAME",
            "SystemCompiler",
        ),
    )

    # Add the architecture
    actions.append(
        CurrentShell.Commands.Set(
            "DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE",
            configuration,
        ),
    )

    # Add scripts that augment existing functionality
    actions += DynamicPluginArchitecture.CreateRegistrationStatements(
        "DEVELOPMENT_ENVIRONMENT_COMPILERS",
        os.path.join(_script_dir, "Scripts", "Compilers"),
        lambda fullpath, name, ext: ext == ".py"
        and (
            name.endswith("Compiler")
            or name.endswith("CodeGenerator")
            or name.endswith("Verifier")
        ),
    )

    actions += DynamicPluginArchitecture.CreateRegistrationStatements(
        "DEVELOPMENT_ENVIRONMENT_TEST_PARSERS",
        os.path.join(_script_dir, "Scripts", "TestParsers"),
        lambda fullpath, name, ext: ext == ".py" and name.endswith("TestParser"),
    )

    actions += DynamicPluginArchitecture.CreateRegistrationStatements(
        "DEVELOPMENT_ENVIRONMENT_FORMATTERS",
        os.path.join(_script_dir, "Scripts", "Formatters"),
        lambda fullpath, name, ext: ext == ".py" and name.endswith("Formatter"),
    )

    actions.append(
        CurrentShell.Commands.Augment(
            "DEVELOPMENT_ENVIRONMENT_TESTER_CONFIGURATIONS",
            ["c++-compiler-CMake", "c++-test_parser-CMake"],
        ),
    )

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


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _EnumLibraryDependencies(type, root, version_info):
    library_fullpath = os.path.join(
        root,
        RepositoryBootstrapConstants.LIBRARIES_SUBDIR,
        type,
    )
    if not os.path.isdir(library_fullpath):
        return

    for name in os.listdir(library_fullpath):
        fullpath = os.path.join(library_fullpath, name)
        if not os.path.isdir(fullpath):
            continue

        value = ActivationActivity.GetVersionedDirectory(version_info, fullpath)
        assert os.path.isdir(value), value

        yield value
