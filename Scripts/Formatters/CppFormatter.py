# ----------------------------------------------------------------------
# |
# |  CppFormatter.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-03-11 20:57:43
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-20
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the Formatter object"""

import importlib
import itertools
import os
import re
import sys
import textwrap

import six

import CommonEnvironment
from CommonEnvironment.CallOnExit import CallOnExit
from CommonEnvironment import FileSystem
from CommonEnvironment.FormatterImpl import FormatterImpl
from CommonEnvironment import Interface
from CommonEnvironment import Process
from CommonEnvironment import StringHelpers

from CommonEnvironment.TypeInfo.FundamentalTypes.FilenameTypeInfo import FilenameTypeInfo

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# Import this module here so that it is available to plugins, thereby preventing
# them from having to do a wonky import of an __init__.py file.
from CppFormatterImpl import PluginBase

# ----------------------------------------------------------------------
@Interface.staticderived
class Formatter(FormatterImpl):

    SUPPORTED_EXTENSIONS                    = [
        ".cpp",
        ".cc",
        ".c",
        ".hpp",
        ".h",
    ]

    # ----------------------------------------------------------------------
    # |  Properties
    Name                                    = Interface.DerivedProperty("C++")
    Description                             = Interface.DerivedProperty("Formats C++ code using clang-format plus enhancements")
    InputTypeInfo                           = Interface.DerivedProperty(
        FilenameTypeInfo(
            validation_expression=r".+(?:{})".format(
                "|".join([re.escape(ext) for ext in SUPPORTED_EXTENSIONS]),
            ),
        ),
    )

    # ----------------------------------------------------------------------
    # |  Methods
    _is_initialized                         = False

    @classmethod
    def __clsinit__(cls, *plugin_input_dirs):
        if cls._is_initialized:
            return

        plugins = cls._GetPlugins(
            os.path.join(_script_dir, "CppFormatterImpl"),
            *plugin_input_dirs,
        )

        debug_plugin = None
        for potential_plugin in plugins:
            if potential_plugin.Name == "Debug":
                debug_plugin = potential_plugin
                break

        cls._plugins = plugins
        cls._debug_plugin = debug_plugin

        cls._is_initialized = True

    # ----------------------------------------------------------------------
    @classmethod
    @Interface.override
    def Format(
        cls,
        filename_or_content,
        include_plugin_names=None,
        exclude_plugin_names=None,
        debug=False,
        hint_filename=None,
        *plugin_input_dirs,
        **plugin_args
    ):
        cls.__clsinit__(*plugin_input_dirs)

        if FileSystem.IsFilename(filename_or_content):
            with open(filename_or_content) as f:
                filename_or_content = f.read()

        input_content = filename_or_content
        del filename_or_content

        include_plugin_names = set(include_plugin_names or [])
        exclude_plugin_names = set(exclude_plugin_names or [])

        if debug:
            if include_plugin_names:
                include_plugin_names.add(cls._debug_plugin.Name)
        else:
            exclude_plugin_names.add(cls._debug_plugin.Name)

        plugins = [plugin for plugin in cls._plugins if plugin.Name not in exclude_plugin_names and (not include_plugin_names or plugin.Name in include_plugin_names)]

        # Preprocess the content
        lines = input_content.split("\n")

        for plugin in plugins:
            lines = plugin.PreprocessLines(lines)

        input_content = "\n".join(lines)

        # Invoke clang-format
        command_line = "clang-format -style=file{}".format(
            ' "-assume-filename={}"'.format(hint_filename) if hint_filename is not None else "",
        )

        result, output = Process.Execute(
            command_line,
            stdin=input_content,
        )

        if result != 0:
            raise Exception(
                textwrap.dedent(
                    """\
                    clang-format failed: {}

                        {}
                    """,
                ).format(result, StringHelpers.LeftJustify(output, 4)),
            )

        # Convert the lines into line structures
        lines = []
        continuation_block_index = 0
        continuation_block_id = None

        for line_content in output.split("\n"):
            has_continuation_token = False

            if line_content.endswith("\\"):
                if continuation_block_id is None:
                    continuation_block_id = continuation_block_index
                    continuation_block_index += 1

                has_continuation_token = True
                line_content = line_content[:-1].rstrip()

            line = PluginBase.Line(
                line_content,
                continuation_block_id=continuation_block_id,
            )

            if not has_continuation_token:
                continuation_block_id = None

            lines.append(line)

        # Decorate the lines
        for plugin in plugins:
            args = []
            kwargs = {}

            defaults = plugin_args.get(plugin.Name, None)
            if defaults is not None:
                if isinstance(defaults, (list, tuple)):
                    args = defaults
                elif isinstance(defaults, dict):
                    kwargs = defaults
                else:
                    assert False, defaults

            lines = plugin.Decorate(lines, *args, **kwargs)

        # Postprocess the lines
        for plugin in plugins:
            lines = plugin.PostprocessLines(lines)

        # Restore the line continuation chars
        output = []
        continuation_block_id = None

        for line_index, line in enumerate(lines):
            # Add continuation chars
            if line.continuation_block_id is not None and line.continuation_block_id != continuation_block_id:
                continuation_block_id = line.continuation_block_id

                # Process all the lines in this block
                max_line_length = 0
                end_block_index = line_index

                while end_block_index < len(lines) and lines[end_block_index].continuation_block_id == continuation_block_id:
                    max_line_length = max(max_line_length, len(lines[end_block_index].content))
                    end_block_index += 1

                max_line_length += 2

                index = line_index
                while index < end_block_index:
                    if index + 1 == end_block_index:
                        suffix = ""
                    else:
                        suffix = "{}\\".format(" " * (max_line_length - len(lines[index].content)))

                    lines[index].content = "{}{}".format(lines[index].content, suffix)
                    index += 1

        output = "\n".join([line.content for line in lines])

        return output, output != input_content
