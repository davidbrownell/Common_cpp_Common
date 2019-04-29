# ----------------------------------------------------------------------
# |
# |  _custom_data.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-25 11:39:51
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Data used by both Setup_custom.py and Activate_custom.py"""

import os

import CommonEnvironment

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
#  ----------------------------------------------------------------------

_CUSTOM_DATA                                = [
    (
        "cmake",
        [
            (
                "v3.13.4",
                [
                    ("Windows", "cfb94e2e356f1e0cf8574b345798410ba1b98c3f5b8f8d568e87879811c2a9f1", None),
                    ("Linux", "b786120d2d1741abff9e2e69b7b94139216ca800559f28707522658568ccb98f", "bin"),
                ],
            )
        ],
    ),
    (
        "ninja",
        [
            (
                "v1.9.0",
                [
                    ("Windows", "4594f25878ec07bc25795ba27def1f83d8f3d2b5ff62335a0f1a25154407384d", None),
                    ("Linux", "d53acc6579e21fc5b36ba923c758f1b53c85b0177765f014c43b9b4b48e7166e", "ninja"),
                ],
            )
        ],
    ),
]
