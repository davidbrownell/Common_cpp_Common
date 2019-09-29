# ----------------------------------------------------------------------
# |
# |  CMakeTestParser.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-04 10:08:14
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the TestParser object"""

import os

import CommonEnvironment
from CommonEnvironment import FileSystem
from CommonEnvironment import Interface
from CommonEnvironment.TestParserImpl import TestParserImpl

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
#  ----------------------------------------------------------------------

# ----------------------------------------------------------------------
@Interface.staticderived
class TestParser(TestParserImpl):
    """Parses content produced by Cmake"""

    # ----------------------------------------------------------------------
    # |  Public Properties
    Name                                    = Interface.DerivedProperty("CMake")
    Description                             = Interface.DerivedProperty("Parses CMake CTest output.")

    # ----------------------------------------------------------------------
    # |  Methods
    @staticmethod
    @Interface.override
    def IsSupportedCompiler(compiler):
        return compiler.Name == "CMake"

    # ----------------------------------------------------------------------
    @classmethod
    @Interface.override
    def Parse(cls, test_data):
        if "100% tests passed" in test_data:
            return 0

        return -1

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.override
    def CreateInvokeCommandLine(context, debug_on_error):
        return 'cd "{output_dir}" && ctest --verbose{parallel}'.format(
            output_dir=context["output_dir"],
            parallel=" --parallel" if not context.get("is_profile", False) else "",
        )

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.override
    def RemoveTemporaryArtifacts(context):
        for potential_dir in ["Testing"]:
            potential_dir = os.path.join(context["output_dir"], potential_dir)
            FileSystem.RemoveTree(potential_dir)

        for potential_file in ["CTestTestfile.cmake"]:
            potential_file = os.path.join(context["output_dir"], potential_file)
            FileSystem.RemoveFile(potential_file)
