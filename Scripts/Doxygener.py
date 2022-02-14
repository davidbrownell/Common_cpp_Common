# ----------------------------------------------------------------------
# |
# |  Doxygener.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-09-06 23:31:34
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-22
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Invokes doxygen on discovered files"""

import json
import os
import re
import shutil
import sys

from collections import OrderedDict

import inflect as inflect_mod

import CommonEnvironment
from CommonEnvironment.CallOnExit import CallOnExit
from CommonEnvironment import CommandLine
from CommonEnvironment import FileSystem
from CommonEnvironment import Process
from CommonEnvironment.StreamDecorator import StreamDecorator

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

inflect                                     = inflect_mod.engine()

# ----------------------------------------------------------------------
DOXYGEN_EXTENSION                           = ".doxygen"
DOXYGEN_EXTENSION_IGNORE                    = "{}-ignore".format(DOXYGEN_EXTENSION)

# ----------------------------------------------------------------------
@CommandLine.EntryPoint
@CommandLine.Constraints(
    code_dir_or_doxygen_filename=CommandLine.FilenameTypeInfo(
        match_any=True,
    ),
    output_dir=CommandLine.DirectoryTypeInfo(
        ensure_exists=False,
    ),
    output_stream=None,
)
def EntryPoint(
    code_dir_or_doxygen_filename,
    output_dir,
    output_stream=sys.stdout,
    verbose=False,
):
    with StreamDecorator(output_stream).DoneManager(
        line_prefix="",
        prefix="\nResults: ",
        suffix="\n",
    ) as dm:
        # Get the doxygen files
        doxygen_files = []

        if os.path.isfile(code_dir_or_doxygen_filename):
            doxygen_files.append(code_dir_or_doxygen_filename)
        else:
            dm.stream.write(
                "Searching for doxygen files in '{}'...".format(
                    code_dir_or_doxygen_filename,
                ),
            )
            with dm.stream.DoneManager(
                done_suffix=lambda: "{} found".format(
                    inflect.no("file", len(doxygen_files)),
                ),
                suffix="\n",
            ) as this_dm:
                for fullpath in FileSystem.WalkFiles(
                    code_dir_or_doxygen_filename,
                    include_file_extensions=[DOXYGEN_EXTENSION],
                    traverse_exclude_dir_names=FileSystem.CODE_EXCLUDE_DIR_NAMES,
                ):
                    if not os.path.isfile(
                        "{}{}".format(
                            os.path.splitext(fullpath)[0],
                            DOXYGEN_EXTENSION_IGNORE,
                        ),
                    ):
                        doxygen_files.append(fullpath)

            if not doxygen_files:
                return dm.result

        # Process the files

        # ----------------------------------------------------------------------
        class GetDoxygenValueError(KeyError):
            """Exception raised when a doxygen tag is not found"""

            pass

        # ----------------------------------------------------------------------
        def GetDoxygenValue(tag, content):
            match = re.search(
                r"{}[ \t]*=[ \t]*(?P<value>.*?)\r?\n".format(re.escape(tag)),
                content,
                re.IGNORECASE,
            )

            if not match:
                raise GetDoxygenValueError(
                    "Unable to find '{}' in the doxygen configuration file".format(tag),
                )

            return match.group("value")

        # ----------------------------------------------------------------------

        results = OrderedDict()

        dm.stream.write(
            "Processing {}...".format(inflect.no("doxygen file", len(doxygen_files))),
        )
        with dm.stream.DoneManager(
            suffix="\n",
        ) as doxygen_dm:
            for index, doxygen_file in enumerate(doxygen_files):
                doxygen_dm.stream.write(
                    "Processing '{}' ({} of {})...".format(
                        doxygen_file,
                        index + 1,
                        len(doxygen_files),
                    ),
                )
                with doxygen_dm.stream.DoneManager() as this_dm:
                    prev_dir = os.getcwd()

                    os.chdir(os.path.dirname(doxygen_file))
                    with CallOnExit(lambda: os.chdir(prev_dir)):
                        # Execute
                        this_dm.result = Process.Execute(
                            'dot -c && doxygen "{}"'.format(doxygen_file),
                            StreamDecorator(this_dm.stream if verbose else None),
                        )

                        if this_dm.result != 0:
                            continue

                        # Extract data from the doxygen file
                        with open(doxygen_file) as f:
                            content = f.read()

                        project_name = GetDoxygenValue("PROJECT_NAME", content)

                        # Older doxygen files don't have a PROJECT_VERSION
                        try:
                            project_version = GetDoxygenValue("PROJECT_VERSION", content)
                        except GetDoxygenValueError:
                            project_version = GetDoxygenValue("PROJECT_NUMBER", content)

                        output_directory = GetDoxygenValue("OUTPUT_DIRECTORY", content)

                        source_dir = os.path.dirname(doxygen_file)
                        if output_directory:
                            output_directory = os.pth.join(source_dir, output_directory)

                        dest_dir = os.path.join(output_dir, project_name)
                        if project_version:
                            dest_dir = os.path.join(dest_dir, project_version)

                        dest_dir = dest_dir.replace('"', "").strip()
                        FileSystem.MakeDirs(dest_dir)

                        for content_type in [
                            "html",
                            "Latex",
                            "RTF",
                            "man",
                            "XML",
                        ]:
                            value = GetDoxygenValue(
                                "GENERATE_{}".format(content_type),
                                content,
                            )
                            if not value or value.lower() != "yes":
                                continue

                            output_name = GetDoxygenValue(
                                "{}_OUTPUT".format(content_type),
                                content,
                            )

                            source_fullpath = os.path.join(source_dir, output_name)
                            dest_fullpath = os.path.join(dest_dir, output_name)

                            if not os.path.isdir(source_fullpath):
                                this_dm.stream.write(
                                    "ERROR: The directory '{}' does not exist.\n".format(
                                        source_fullpath,
                                    ),
                                )
                                this_dm.result = -1
                                continue

                            FileSystem.RemoveTree(dest_fullpath)
                            shutil.move(source_fullpath, dest_fullpath)

                            results.setdefault(doxygen_file, OrderedDict())[
                                content_type
                            ] = dest_fullpath

                        # Tagfile
                        value = GetDoxygenValue("GENERATE_TAGFILE", content)
                        if value:
                            source_fullpath = os.path.join(source_dir, value)
                            dest_fullpath = os.path.join(dest_dir, value)

                            if not os.path.isfile(source_fullpath):
                                this_dm.stream.write(
                                    "ERROR: The filename '{}' does not exist.\n".format(
                                        source_fullpath,
                                    ),
                                )
                                this_dm.result = -1
                                continue

                            FileSystem.RemoveFile(dest_fullpath)
                            shutil.move(source_fullpath, dest_fullpath)

                            results.setdefault(doxygen_file, OrderedDict())[
                                "tagfile"
                            ] = dest_fullpath

        # Generate the json file
        output_filename = os.path.join(
            output_dir,
            "{}.json".format(os.path.splitext(_script_name)[0]),
        )

        dm.stream.write("Writing '{}'...".format(output_filename))
        with dm.stream.DoneManager() as this_dm:
            with open(output_filename, "w") as f:
                json.dump(results, f)

        return dm.result

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        sys.exit(CommandLine.Main())
    except KeyboardInterrupt:
        pass
