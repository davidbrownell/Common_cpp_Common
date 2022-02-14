# ----------------------------------------------------------------------
# |
# |  CMakeTestParser.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-04 10:08:14
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-22
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the TestParser object"""

import os
import re

import CommonEnvironment
from CommonEnvironment import FileSystem
from CommonEnvironment import Interface
from CommonEnvironment.TestParserImpl import TestParserImpl

from Catch2TestParser import ExtractBenchmarkOutput as ExtractCatch2BenchmarkOutput

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

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
    @staticmethod
    @Interface.override
    def Parse(test_data):
        if "100% tests passed" not in test_data:
            return -1

        # CTest will append an index before each line of the test output -
        # remove that if it exists.
        line_regex = re.compile(r"^\d+: (?P<content>.*)")

        lines = test_data.split("\n")
        for index, line in enumerate(lines):
            match = line_regex.match(line)
            if not match:
                continue

            lines[index] = match.group("content")

        scrubbed_test_data = "\n".join(lines)

        # CTest can wrap many individual test frameworks - attempt to extract benchmark
        # data from well-know test frameworks.
        benchmark_data = None

        for extract_func in [ExtractCatch2BenchmarkOutput]:
            benchmark_data = extract_func(scrubbed_test_data)
            if benchmark_data:
                return 0, benchmark_data

        return 0

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.override
    def CreateInvokeCommandLine(context, debug_on_error):
        is_profile_or_benchmark = context.get("is_profile", False) or context.get(
            "is_benchmark",
            False,
        )

        return 'cd "{output_dir}" && ctest --verbose{parallel}'.format(
            output_dir=context["output_dir"],
            parallel="" if is_profile_or_benchmark else " --parallel",
        )

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.override
    def RemoveTemporaryArtifacts(context):
        for potential_dir in ["Testing"]:
            potential_dir = os.path.join(context["output_dir"], potential_dir)
            FileSystem.RemoveTree(potential_dir)
