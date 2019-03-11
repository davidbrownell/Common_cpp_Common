# ----------------------------------------------------------------------
# |
# |  ClosingBracketNewlinePlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-03-10 17:50:54
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the Plugin object"""

import os

import six

import CommonEnvironment
from CommonEnvironment import Interface

from CommonCppCommon.clang_formatAndBrown.Plugins import Plugin as PluginBase

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
#  ----------------------------------------------------------------------

# ----------------------------------------------------------------------
@Interface.staticderived
class Plugin(PluginBase):
    """\
    Ensures that the closing bracket associated with bin-packed items 
    appear on a newline that is horizontally aligned with the line
    that contains the opening bracket.
    """

    # ----------------------------------------------------------------------
    # |  Properties
    Name                                    = Interface.DerivedProperty("ClosingBracketNewline")
    Priority                                = Interface.DerivedProperty(PluginBase.STANDARD_PRIORITY)

    # ----------------------------------------------------------------------
    # |  Methods
    @classmethod
    @Interface.override
    def Decorate(cls, lines):
        brackets = {
            "(": ")",
            "<": ">",
            "[": "]",
        }

        # ----------------------------------------------------------------------
        def UpdateClosingBracket(opening_line_index, opening, closing):
            bracket_counter = 1

            current_line_index = opening_line_index + 1
            while current_line_index < len(lines):
                current_line = lines[current_line_index]

                for char_index, char in enumerate(current_line):
                    if char == opening:
                        bracket_counter += 1
                    elif char == closing:
                        bracket_counter -= 1

                        if bracket_counter == 0:
                            # Get the whitespace associated with the opening line
                            opening_line = lines[opening_line_index]

                            whitespace_index = 0
                            while whitespace_index < len(opening_line) and opening_line[whitespace_index].isspace(
                            ):
                                whitespace_index += 1

                            # Update the line
                            lines[current_line_index] = "{}\n{}{}".format(
                                current_line[:char_index],
                                opening_line[:whitespace_index],
                                current_line[char_index:],
                            )
                            return

                current_line_index += 1

        # ----------------------------------------------------------------------

        for line_index, line in cls.EnumerateLines(lines):
            line = line.rstrip()

            for opening, closing in six.iteritems(brackets):
                if line.endswith(opening):
                    UpdateClosingBracket(line_index, opening, closing)
                    break

        return lines
