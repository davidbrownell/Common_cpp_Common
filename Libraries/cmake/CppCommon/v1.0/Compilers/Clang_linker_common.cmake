# ----------------------------------------------------------------------
# |
# |  Clang_linker_common.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-07-28 08:12:18
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------

# Contains linker settings common to scenarios when clang is used directly or
# as a proxy for other backend compilers (MSVC or GCC).

# ----------------------------------------------------------------------
# |  Dynamic Flags

# CppCommon_CODE_COVERAGE
if(WIN32)
    foreach(_flag IN ITEMS
        clang_rt.profile-x86_64.lib
    )
        string(APPEND _local_EXE_LINKER_flags_CppCommon_CODE_COVERAGE_TRUE " ${_flag}")
    endforeach()
else()
    foreach(_flag IN ITEMS
        clang_rt.profile-x86_64
    )
        string(APPEND _local_EXE_LINKER_flags_CppCommon_CODE_COVERAGE_TRUE " -l${_flag}")
    endforeach()
endif()