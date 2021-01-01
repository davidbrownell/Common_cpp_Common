# ----------------------------------------------------------------------
# |
# |  __init__.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-15 15:10:53
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-21
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""
Contains functionality that is useful when parsing code coverage filters according
to the format defined in CodeCoverageFilter.SimpleSchema.
"""

from fnmatch import fnmatch
import os
import sys

from functools import lru_cache

import CommonEnvironment
from CommonEnvironment.CallOnExit import CallOnExit

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

sys.path.insert(0, os.path.join(_script_dir, "GeneratedCode"))
with CallOnExit(lambda: sys.path.pop(0)):
    import CodeCoverageFilter_PythonYamlSerialization as Yaml


# ----------------------------------------------------------------------
FILTER_FILENAME                             = "code_coverage.yaml"

# ----------------------------------------------------------------------
def GetFilters(filename):
    """\
    Given a filename, will parse all coverage yaml files in its ancestors and
    create a list of includes and excludes based on the union of all filters
    found that apply to the file.
    """

    yaml_filenames = []

    dirname = os.path.dirname(os.path.realpath(filename))
    while True:
        potential_filename = os.path.join(dirname, FILTER_FILENAME)
        if os.path.isfile(potential_filename):
            yaml_filenames.append(potential_filename)

        potential_dirname = os.path.dirname(dirname)
        if potential_dirname == dirname:
            break

        dirname = potential_dirname

    nonlocals = CommonEnvironment.Nonlocals(
        includes=[],
        excludes=[],
    )

    # ----------------------------------------------------------------------
    def ProcessFilter(filter):
        nonlocals.includes += filter.includes
        nonlocals.excludes += filter.excludes

        return filter.continue_processing

    # ----------------------------------------------------------------------

    should_continue = True

    for yaml_filename in yaml_filenames:
        obj = _Load(yaml_filename)

        if obj.filter is not None:
            if ProcessFilter(obj.filter) is False:
                break

        for named_filter in obj.named_filters:
            if fnmatch(filename, named_filter.glob):
                should_continue = ProcessFilter(named_filter)
                if not should_continue:
                    break

        if not should_continue:
            break

    return nonlocals.includes, nonlocals.excludes


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
@lru_cache()
def _Load(yaml_filename):
    return Yaml.Deserialize(
        yaml_filename,
        always_include_optional=True,
    )
