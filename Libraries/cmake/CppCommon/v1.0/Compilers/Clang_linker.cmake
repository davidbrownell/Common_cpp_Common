# ----------------------------------------------------------------------
# |
# |  Clang_linker.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-07-28 09:12:53
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-20
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# |  Static Flags
foreach(_flag IN ITEMS
    # No flags at this time
)
    string(APPEND _EXE_LINKER_FLAGS_RELEASE " ${_flag}")
    string(APPEND _EXE_LINKER_FLAGS_RELEASEMINSIZE " ${_flag}")
    string(APPEND _EXE_LINKER_FLAGS_RELEASENOOPT " ${_flag}")
endforeach()

# ----------------------------------------------------------------------
# |  Dynamic Flags

# CppCommon_CODE_COVERAGE
foreach(_flag IN ITEMS
    -fprofile-instr-generate                # For use with llvm-cov
)
    string(APPEND _EXE_LINKER_FLAGS_CppCommon_CODE_COVERAGE_TRUE " ${_flag}")
endforeach()
