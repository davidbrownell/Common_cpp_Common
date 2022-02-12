# ----------------------------------------------------------------------
# |
# |  DebugPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-03-10 17:42:59
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-22
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the Plugin object"""

import os
import sys
import textwrap

import CommonEnvironment
from CommonEnvironment import Interface

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# This is available because it is imported in CppFormatter.py
from CppFormatterImpl import PluginBase

# ----------------------------------------------------------------------
@Interface.staticderived
class Plugin(PluginBase):
    """Prints diagnostic information about the input code"""

    # ----------------------------------------------------------------------
    # |  Properties
    Name                                    = Interface.DerivedProperty("Debug")
    Priority                                = Interface.DerivedProperty(1)

    # ----------------------------------------------------------------------
    # |  Methods
    @classmethod
    @Interface.override
    def PreprocessLines(cls, lines):
        return cls._Display("Pre clang-format", lines)

    # ----------------------------------------------------------------------
    @classmethod
    @Interface.override
    def Decorate(cls, lines):
        return cls._Display("Post clang-format", lines)

    # ----------------------------------------------------------------------
    @classmethod
    @Interface.override
    def PostprocessLines(cls, lines):
        return cls._Display("Post-Decoration", lines)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @staticmethod
    def _Display(header, lines):
        sys.stdout.write(
            textwrap.dedent(
                """\
                # ----------------------------------------------------------------------
                # |
                # |  {}
                # |
                # ----------------------------------------------------------------------
                """,
            ).format(header),
        )

        for line_index, line in enumerate(lines):
            sys.stdout.write("{0:>3}) {1}\n".format(line_index + 1, line))

        sys.stdout.write("\n")

        return lines
