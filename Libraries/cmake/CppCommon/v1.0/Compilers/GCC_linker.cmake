# ----------------------------------------------------------------------
# |
# |  GCC_linker.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-09-26 16:30:28
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
    # No flags at this time
)
    string(APPEND _EXE_LINKER_FLAGS_RELEASE " ${_flag}")
    string(APPEND _EXE_LINKER_FLAGS_RELEASEMINSIZE " ${_flag}")
    string(APPEND _EXE_LINKER_FLAGS_RELEASENOOPT " ${_flag}")
endforeach()
