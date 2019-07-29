# ----------------------------------------------------------------------
# |
# |  MSVC_linker.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-07-28 09:08:30
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
    /DYNAMICBASE                        # Randomized base address
    /MANIFEST                           # Creates a side-by-side manifest file and optionally embeds it in the binary.
    /NXCOMPAT                           # Data Execution Prevention
    /MANIFESTUAC:"level='asInvoker' uiAccess='false'"   # Specifies whether User Account Control (UAC) information is embedded in the program manifest.
    /TLBID:1                            # Specifies the resource ID of the linker-generated type library.
)
    string(APPEND _local_EXE_LINKER_flags " ${_flag}")
endforeach()

# The following flags are valid for MSVC but not for Clang
if(CMAKE_CXX_COMPILER_ID MATCHES MSVC)
    foreach(_flag IN ITEMS
        /LTCG                           # Link-time code generation
    )
        string(APPEND _local_EXE_LINKER_flags_release " ${_flag}")
    endforeach()
endif()

# The following flags are valid for both MSVC and Clang
foreach(_flag IN ITEMS
    /OPT:ICF                            # Enable COMDAT Folding
    /OPT:REF                            # References
)
    string(APPEND _local_EXE_LINKER_flags_release " ${_flag}")
endforeach()

set(_local_EXE_LINKER_flags_release_min_size "${_local_EXE_LINKER_flags_release}")
set(_local_EXE_LINKER_flags_release_no_opt "${_local_EXE_LINKER_flags_release}")

# ----------------------------------------------------------------------
# |  Dynamic Flags

# CppCommon_CODE_COVERAGE
foreach(_flag IN ITEMS
    /PROFILE
    /OPT:NOREF
    /OPT:NOICF
)
    string(APPEND _local_EXE_LINKER_flags_CppCommon_CODE_COVERAGE_TRUE " ${_flag}")
endforeach()

set(_local_EXE_LINKER_flags_CppCommon_CODE_COVERAGE_FALSE_DEBUG "/INCREMENTAL")
set(_local_EXE_LINKER_flags_CppCommon_CODE_COVERAGE_FALSE_RELEASE "/INCREMENTAL:NO")

# CppCommon_NO_DEBUG_INFO
set(_local_EXE_LINKER_flags_CppCommon_NO_DEBUG_INFO_FALSE "/DEBUG")
