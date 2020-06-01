# ----------------------------------------------------------------------
# |
# |  Clang_compiler.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-07-28 09:11:21
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
    -fasynchronous-unwind-tables            # Increased reliability of backtraces
    -fexceptions                            # Enable table-based thread cancellation
    -fvisibility=hidden                     # Symbols in shared libraries are hidden by default (which is consistent with Windows)
    -pipe                                   # Avoid temporary files
    -pthread                                # Thread functionality
    -Wl,-rpath,'\\\$ORIGIN'                 # Look for libs in the same dir
)
    STRING(APPEND _CXX_FLAGS " ${_flag}")
endforeach()

# Debug
foreach(_flag IN ITEMS
    -DDEBUG
    -D_DEBUG
    -O0                                     # No optimizations
)
    STRING(APPEND _CXX_FLAGS_DEBUG " ${_flag}")
endforeach()

# Release args
foreach(_flag IN ITEMS
    -DNDEBUG
    -D_NDEBUG
    -D_FORTIFY_SOURCE=2                     # Run-time buffer overflow detection
    -D_GLIBCXX_ASSERTIONS                   # Run-time bounds checking for C++ strings and containers
    -fstack-protector-strong                # Stack smashing protection
    -O3                                     # Advanced optimizations
)
    STRING(APPEND _CXX_FLAGS_RELEASE " ${_flag}")
endforeach()

# ReleaseMinSize
foreach(_flag IN ITEMS
    -DNDEBUG
    -D_NDEBUG
    -D_FORTIFY_SOURCE=2                     # Run-time buffer overflow detection
    -D_GLIBCXX_ASSERTIONS                   # Run-time bounds checking for C++ strings and containers
    -fstack-protector-strong                # Stack smashing protection
    -Os                                     # Optimize for small code
)
    STRING(APPEND _CXX_FLAGS_RELEASEMINSIZE " ${_flag}")
endforeach()

# ReleaseNoOpt
foreach(_flag IN ITEMS
    -DNDEBUG
    -D_NDEBUG
    -D_FORTIFY_SOURCE=2                     # Run-time buffer overflow detection
    -D_GLIBCXX_ASSERTIONS                   # Run-time bounds checking for C++ strings and containers
    -fstack-protector-strong                # Stack smashing protection
    -O0                                     # No optimizations
)
    STRING(APPEND _CXX_FLAGS_RELEASENOOPT " ${_flag}")
endforeach()

if(APPLE)
    # Do not add additional flags
else()
    foreach(_dest_flag IN ITEMS
        _CXX_FLAGS_RELEASE
        _CXX_FLAGS_RELEASEMINSIZE
        _CXX_FLAGS_RELEASENOOPT
    )
        foreach(_flag IN ITEMS
            -Wl,-z,defs                     # Detect and reject underlinking
            -Wl,-z,now                      # Disable lazy binding
            -Wl,-z,relro                    # Read-only segments after relocation
        )
            STRING(APPEND ${_dest_flag} " ${_flag}")
        endforeach()
    endforeach()
endif()

# ----------------------------------------------------------------------
# |  Dynamic Flags

# CppCommon_UNICODE
set(_CXX_FLAGS_CppCommon_UNICODE_TRUE "-DUNICODE -D_UNICODE")
set(_CXX_FLAGS_CppCommon_UNICODE_FALSE "-DMBCS -D_MBCS")

# CppCommon_STATIC_CRT
set(_CXX_FLAGS_CppCommon_STATIC_CRT_TRUE "-static-libstdc++")

# CppCommon_NO_DEBUG_INFO
foreach(_flag IN ITEMS
    -g                                      # Generate debugging information
    -grecord-gcc-switches                   # Store compiler flags in debugging information
)
    STRING(APPEND _CXX_FLAGS_CppCommon_NO_DEBUG_INFO_FALSE " ${_flag}")
endforeach()

# CppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION
set(_CXX_FLAGS_CppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION_FALSE "-fPIC")
set(_EXE_LINKER_FLAGS_CppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION_FALSE "-pie")

# CppCommon_PREPROCESSOR_OUTPUT
set(_CXX_FLAGS_CppCommon_PREPROCESSOR_OUTPUT_TRUE "-E")
