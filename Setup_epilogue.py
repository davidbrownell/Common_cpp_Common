# ----------------------------------------------------------------------
# |
# |  Setup_epilogue.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-08-26 19:44:24
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-21
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Performs epilogue activities for setup"""

import os
import shutil
import sys

import CommonEnvironment
from CommonEnvironment import FileSystem

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

fundamental_repo                            = os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL")
assert os.path.isdir(fundamental_repo), fundamental_repo

sys.path.insert(0, fundamental_repo)
from RepositoryBootstrap import *                                           # <Unused import> pylint: disable = W0614
from RepositoryBootstrap.SetupAndActivate import CurrentShell               # <Unused import> pylint: disable = W0614
from RepositoryBootstrap.SetupAndActivate.Configuration import *            # <Unused import> pylint: disable = W0614

del sys.path[0]

# ----------------------------------------------------------------------
source_dir                                  = os.path.join(_script_dir, "Tools", "cmake", "v3.13.4", "customizations")
assert os.path.isdir(source_dir), source_dir

dest_dir                                    = os.path.join(
    _script_dir,
    "Tools",
    "cmake",
    "v3.13.4",
    CurrentShell.CategoryName,
    os.getenv("DEVELOPMENT_ENVIRONMENT_ENVIRONMENT_NAME"),
    "share",
    "cmake-3.13",
    "Modules",
)

for filename in FileSystem.WalkFiles(source_dir):
    shutil.copyfile(filename, os.path.join(dest_dir, os.path.basename(filename)))
