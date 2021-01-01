# ----------------------------------------------------------------------
# |
# |  ClosingBracketNewlinePlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-03-10 17:50:54
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-21
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

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# This is available because it is imported in CppFormatter.py
from CppFormatterImpl import PluginBase

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
                current_line_content = lines[current_line_index].content

                for char_index, char in enumerate(current_line_content):
                    if char == opening:
                        bracket_counter += 1
                    elif char == closing:
                        bracket_counter -= 1

                        if bracket_counter == 0:
                            # Get the whitespace associated with the opening line
                            opening_line_content = lines[opening_line_index].content

                            whitespace_index = 0
                            while whitespace_index < len(opening_line_content) and opening_line_content[whitespace_index].isspace(
                            ):
                                whitespace_index += 1

                            # Update the line
                            lines.insert(
                                current_line_index + 1,
                                lines[current_line_index].Clone(
                                    "{}{}".format(opening_line_content[:whitespace_index], current_line_content[char_index:]),
                                    current_line_content=current_line_content[:char_index],
                                ),
                            )
                            return

                current_line_index += 1

        # ----------------------------------------------------------------------

        line_index = 0

        while line_index < len(lines):
            line = lines[line_index].content.rstrip()

            for opening, closing in six.iteritems(brackets):
                if line.endswith(opening):
                    UpdateClosingBracket(line_index, opening, closing)
                    break

            line_index += 1

        return lines
