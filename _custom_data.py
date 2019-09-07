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
                    (
                        "Windows",
                        "cfb94e2e356f1e0cf8574b345798410ba1b98c3f5b8f8d568e87879811c2a9f1",
                    ),
                    (
                        "Linux",
                        "8cdb78b6d2919be9cc276f2c7954198aab25435f6d2a2f0fc683b9055c3f141a",
                    ),
                ],
            ),
        ],
    ),
    (
        "Doxygen",
        [
            (
                "v1.8.16",
                [
                    (
                        "Windows",
                        "ca368c49920b8c4c842acde913b1c33276794041534a6b136479de9f8052e1b9",
                    ),
                    (
                        "Linux",
                        "f9d2a063e9aab5aa53b61d1a40b3f68b7314fd75eb89658e2747802fc9c82941",
                    ),
                ],
            ),
        ],
    ),
    (
        "ninja",
        [
            (
                "v1.9.0",
                [
                    (
                        "Windows",
                        "4594f25878ec07bc25795ba27def1f83d8f3d2b5ff62335a0f1a25154407384d",
                    ),
                    (
                        "Linux",
                        "cc9f3ed1431fd9008062143272f4701d3d13dc55a75ee860353f88cb7035d63b",
                    ),
                ],
            ),
        ],
    ),
]
