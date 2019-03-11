# ----------------------------------------------------------------------
# |
# |  __init__.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-03-10 16:55:33
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Applies clang-format (https://clang.llvm.org/docs/ClangFormat.html) followed by customizations by David BROWNell"""

import itertools
import importlib
import os
import sys

import CommonEnvironment
from CommonEnvironment.CallOnExit import CallOnExit
from CommonEnvironment import FileSystem
from CommonEnvironment import Process
from CommonEnvironment import StringHelpers

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
#  ----------------------------------------------------------------------

# ----------------------------------------------------------------------
class Executor(object):
    """\
    Object that is capable of formatting source based on clang-format and
    one or more plugins.
    """

    # ----------------------------------------------------------------------
    def __init__(self, output_stream, *plugin_input_dirs, **plugin_args):
        plugins = []
        debug_plugin = None

        for plugin_input_dir in itertools.chain(
            [os.path.join(_script_dir, "Plugins")],
            plugin_input_dirs,
        ):
            if not os.path.isdir(plugin_input_dir):
                raise Exception("'{}' is not a valid directory".format(plugin_input_dir))

            sys.path.insert(0, plugin_input_dir)
            with CallOnExit(lambda: sys.path.pop(0)):
                for filename in FileSystem.WalkFiles(
                    plugin_input_dir,
                    include_file_extensions=[".py"],
                    include_file_base_names=[lambda basename: basename.endswith("Plugin")],
                ):
                    plugin_name = os.path.splitext(os.path.basename(filename))[0]

                    mod = importlib.import_module(plugin_name)
                    if mod is None:
                        output_stream.write(
                            "WARNING: Unable to import the module at '{}'.\n".format(filename),
                        )
                        continue

                    potential_class = None
                    potential_class_names = [plugin_name, "Plugin"]

                    for potential_class_name in potential_class_names:
                        potential_class = getattr(mod, potential_class_name, None)
                        if potential_class is not None:
                            break

                    if potential_class is None:
                        output_stream.write(
                            "WARNING: The module at '{}' does not contain a supported class ({}).\n".format(
                                filename,
                                ", ".join(["'{}'".format(pcn) for pcn in potential_class_names]),
                            ),
                        )
                        continue

                    plugins.append(potential_class)

                    if debug_plugin is None and potential_class.Name == "Debug":
                        debug_plugin = potential_class

        plugins.sort(
            key=lambda plugin: (plugin.Priority, plugin.Name),
        )

        self._plugins                       = plugins
        self._plugin_args                   = plugin_args
        self._debug_plugin                  = debug_plugin

    # ----------------------------------------------------------------------
    @property
    def Plugins(self):
        return iter(self._plugins)

    # ----------------------------------------------------------------------
    def Format(
        self,
        input_filename_or_content,
        include_plugin_names=None,
        exclude_plugin_names=None,
        debug=False,
    ):
        """Formats the input file or content and returns the results"""

        plugin_args = self._plugin_args

        if len(input_filename_or_content) < 2000 and os.path.isfile(input_filename_or_content):
            original_filename = input_filename_or_content
            input_filename_or_content = open(input_filename_or_content).read()
        else:
            original_filename = None

        input_content = input_filename_or_content
        del input_filename_or_content

        include_plugin_names = set(include_plugin_names or [])
        exclude_plugin_names = set(exclude_plugin_names or [])

        if debug:
            if include_plugin_names:
                include_plugin_names.add(self._debug_plugin.Name)
        else:
            exclude_plugin_names.add(self._debug_plugin.Name)

        plugins = [plugin for plugin in self.Plugins if plugin.Name not in exclude_plugin_names and (not include_plugin_names or plugin.Name in include_plugin_names)]

        # Preprocess the content
        lines = input_content.split("\n")

        for plugin in plugins:
            lines = plugin.PreprocessLines(lines)

        input_content = "\n".join(lines)

        # Invoke clang-format
        command_line = "clang-format -style=file"
        if original_filename is not None:
            command_line += ' "-assume-filename={}"'.format(original_filename)

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
                ).format(
                    result,
                    StringHelpers.LeftJustify(output, 4),
                ),
            )

        # Decorate the lines
        lines = output.split("\n")

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

        output = "\n".join(lines)

        return output, output != input_content


    # ----------------------------------------------------------------------
    def HasChanges(
        self,
        input_filename_or_content,
        include_plugin_names=None,
        exclude_plugin_names=None,
    ):
        """Returns True if the provided content will change with formatting and False if it will not"""

        return self.Format(
            input_filename_or_content,
            include_plugin_names=include_plugin_names,
            exclude_plugin_names=exclude_plugin_names,
        )[1]
