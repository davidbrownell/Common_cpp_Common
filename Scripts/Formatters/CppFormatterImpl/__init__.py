# ----------------------------------------------------------------------
# |
# |  __init__.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-03-10 17:07:18
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-21
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the PluginBase object"""

import os

import CommonEnvironment
from CommonEnvironment.FormatterImpl.Plugin import Plugin as FormatterPluginBase
from CommonEnvironment import Interface

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
class PluginBase(FormatterPluginBase):
    # ----------------------------------------------------------------------
    # |  Types
    class Line(object):
        # ----------------------------------------------------------------------
        def __init__(
            self,
            content,
            continuation_block_id=None,
        ):
            self.content                    = content
            self.continuation_block_id      = continuation_block_id

        # ----------------------------------------------------------------------
        def __repr__(self):
            return CommonEnvironment.ObjectReprImpl(self)

        # ----------------------------------------------------------------------
        def Clone(
            self,
            new_line_content,
            current_line_content=None,
        ):
            if current_line_content is not None:
                self.content = current_line_content

            return self.__class__(
                new_line_content,
                continuation_block_id=self.continuation_block_id,
            )

    # ----------------------------------------------------------------------
    # |  Protected Methods
    @classmethod
    def EnumerateLines(cls, lines):
        """Enumerates all non-ignored lines in the collection of lines"""

        # Maintain compatibility with python 2.7
        for result in cls._EnumerateLinesImpl(lines):
            yield result

    # ----------------------------------------------------------------------
    @classmethod
    def EnumerateBlocks(cls, lines):
        for line_index, line, set_next_line_func in cls._EnumerateLinesImpl(
            lines,
            include_next_line_func=True,
        ):
            if not line.strip():
                continue

            starting_line_index = line_index
            line_index += 1

            while line_index < len(lines) and lines[line_index].strip():
                line_index += 1

            set_next_line_func(line_index)
            yield starting_line_index, lines[starting_line_index:line_index]

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @classmethod
    def _EnumerateLinesImpl(
        cls,
        lines,
        include_next_line_func=False,
    ):
        nonlocals = CommonEnvironment.Nonlocals(
            index=0,
        )

        if include_next_line_func:
            # ----------------------------------------------------------------------
            def SetNextLine(index):
                nonlocals.index = index

            # ----------------------------------------------------------------------

            yield_func = lambda index, line: (index, line, SetNextLine)
        else:
            yield_func = lambda index, line: (index, line)

        in_disabled_block = False

        while nonlocals.index < len(lines):
            this_line = lines[nonlocals.index]
            this_index = nonlocals.index
            nonlocals.index += 1

            comments = cls._GetComments(this_line)
            if comments is not None:
                if not in_disabled_block and comments == "clang-format off":
                    in_disabled_block = True
                    continue

                elif comments == "clang-format on":
                    in_disabled_block = False
                    continue

            if in_disabled_block:
                continue

            yield yield_func(this_index, this_line)

    # ----------------------------------------------------------------------
    @staticmethod
    def _GetComments(line):
        line = line.strip()

        if line.startswith("//"):
            return line[2:].lstrip()

        if line.startswith("/*") and line.endswith("*/"):
            return line[2:-2].strip()

        return None
