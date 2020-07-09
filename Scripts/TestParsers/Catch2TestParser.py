# ----------------------------------------------------------------------
# |
# |  Catch2TestParser.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-12-19 10:52:08
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-20
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the TestParser object"""

import os
import re
import textwrap

from collections import OrderedDict

import CommonEnvironment
from CommonEnvironment import Interface
from CommonEnvironment import RegularExpression
from CommonEnvironment.TestParserImpl import TestParserImpl

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
@Interface.staticderived
class TestParser(TestParserImpl):
    """Parses content produced by Catch2"""

    # ----------------------------------------------------------------------
    # |  Public Properties
    Name                                    = Interface.DerivedProperty("Catch2")
    Description                             = Interface.DerivedProperty("Parses Catch2 output.")

    # ----------------------------------------------------------------------
    # |  Public Methods
    @staticmethod
    @Interface.override
    def IsSupportedCompiler(compiler):
        # Many compilers are supported
        return True

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.override
    def Parse(test_data):
        if "All tests passed" not in test_data:
            return -1

        benchmark_data = ExtractBenchmarkOutput(test_data)
        if benchmark_data:
            return 0, benchmark_data

        return 0

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.override
    def CreateInvokeCommandLine(context, debug_on_error):
        if "output_filename" in context and context["output_filename"]:
            output_filename = context["output_filename"]
        elif "output_filenames" in context and context["output_filenames"]:
            assert len(context["output_filenames"]) == 1, context["output_filenames"]
            output_filename = context["output_filenames"][0]
        else:
            assert False, context

        dirname, basename = os.path.split(output_filename)

        if context.get("is_benchmark", False):
            flags = "[benchmark]"
        else:
            flags = "~[benchmark] --success"

        return 'cd "{output_dir}" && {output_name} {flags}'.format(
            output_dir=dirname,
            output_name=basename,
            flags=flags,
        )


# ----------------------------------------------------------------------
_ExtractBenchmarkOutput_content_regex       = re.compile(
    textwrap.dedent(
        r"""(?#
        Header          )\~~~~+\r?\n(?#
        Name            )(?P<name>[^\n]+)(?#
        text            ) is a Catch v(?#
        Version         )(?P<catch_version>[\d\.]+)(?#
        text            ) host application.\s+(?#
        Content         )(?P<content>.+?)(?#
        Footer          )====+\r?\n(?#
        )""",
    ),
    re.DOTALL | re.MULTILINE,
)

# Note that the representation of line numbers is different on Linux
# and Windows.
_ExtractBenchmarkOutput_benchmarks_regex    = re.compile(
    textwrap.dedent(
        r"""(?#
        Header 1        )----+\r?\n(?#
        Test Name       )(?P<test_name>[^\r\n]+)\r?\n(?#
        Header 2        )----+\r?\n(?#
        Test Filename   )(?P<test_filename>[^\r\n]+)(?#
        Test line       )(?:(?#
            Windows     )\((?P<test_line_windows>\d+)\)(?#
                        )|(?#
            Linux       ):(?P<test_line_linux>\d+)(?#
                        ))\r?\n(?#
        Header 3        )\.+\r?\n(?#
        Benchmark hdr   )\s+benchmark name\s+samples.+?(?#
        Header 4        )----+\r?\n(?#
        )""",
    ),
    re.DOTALL | re.MULTILINE,
)

_ExtractBenchmarkOutput_stats_regex         = re.compile(
    textwrap.dedent(
        r"""(?#
        Name            )(?P<name>[^\n]+?)(?#
        Samples         )\s+(?P<samples>\d+)(?#
        Iterations      )\s+(?P<iterations>\d+)(?#
        Estimated       )\s+(?P<estimated>[\d\.]+) (?P<estimated_units>\S+)(?#
        newline         )\s*\r?\n(?#
        Mean            )\s+(?P<mean>[\d\.]+) (?P<mean_units>\S+)(?#
        Low Mean        )\s+(?P<low_mean>[\d\.]+) (?P<low_mean_units>\S+)(?#
        High Mean       )\s+(?P<high_mean>[\d\.]+) (?P<high_mean_units>\S+)(?#
        newline         )\s*\r?\n(?#
        Deviation       )\s+(?P<deviation>[\d\.]+) (?P<deviation_units>\S+)(?#
        Low Deviation   )\s+(?P<low_deviation>[\d\.]+) (?P<low_deviation_units>\S+)(?#
        High Deviation  )\s+(?P<high_deviation>[\d\.]+) (?P<high_deviation_units>\S+)(?#
        newline         )\s*\r?\n(?#
        )""",
    ),
    re.DOTALL | re.MULTILINE,
)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def ExtractBenchmarkOutput(output):
    benchmarks = OrderedDict()

    for match in _ExtractBenchmarkOutput_content_regex.finditer(output):
        name = match.group("name")
        catch_version = "Catch v{}".format(match.group("catch_version"))
        content = match.group("content")

        these_benchmarks = []
        dest_units = "ns"

        for match in RegularExpression.Generate(
            _ExtractBenchmarkOutput_benchmarks_regex,
            content,
            leading_delimiter=True,
        ):
            # If there is only one match, that means nothing was found
            if len(match) == 1:
                assert None in match, match
                continue

            test_line = match["test_line_windows"]
            if test_line is None:
                test_line = match["test_line_linux"]
                if test_line is None:
                    assert False

            for stats in _ExtractBenchmarkOutput_stats_regex.finditer(match[None]):
                these_benchmarks.append(
                    TestParserImpl.BenchmarkStat(
                        "{} - {}".format(match["test_name"], stats.group("name")),
                        match["test_filename"],
                        int(test_line),
                        catch_version,
                        TestParserImpl.BenchmarkStat.ConvertTime(
                            float(stats.group("low_mean")),
                            stats.group("low_mean_units"),
                            dest_units,
                        ),
                        TestParserImpl.BenchmarkStat.ConvertTime(
                            float(stats.group("high_mean")),
                            stats.group("high_mean_units"),
                            dest_units,
                        ),
                        TestParserImpl.BenchmarkStat.ConvertTime(
                            float(stats.group("mean")),
                            stats.group("mean_units"),
                            dest_units,
                        ),
                        TestParserImpl.BenchmarkStat.ConvertTime(
                            float(stats.group("deviation")),
                            stats.group("deviation_units"),
                            dest_units,
                        ),
                        int(stats.group("samples")),
                        dest_units,
                        int(stats.group("iterations")),
                    ),
                )

        if these_benchmarks:
            benchmarks[name] = these_benchmarks

    return benchmarks
