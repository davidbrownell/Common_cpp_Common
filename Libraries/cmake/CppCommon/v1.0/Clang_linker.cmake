# ----------------------------------------------------------------------
# |
# |  Clang_linker.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-07-28 09:12:53
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# |  Static Flags
foreach(_flag IN ITEMS
    -pie                                    # Full address space layout randomization (ASLR) for executables
)
    string(APPEND _local_EXE_LINKER_flags_RELEASE " ${_flag}")
endforeach()
