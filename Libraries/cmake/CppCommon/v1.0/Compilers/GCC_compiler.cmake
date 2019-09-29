# ----------------------------------------------------------------------
# |
# |  GCC_compiler.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-09-26 16:30:48
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
# |  Static Flags
foreach(_flag IN ITEMS
    -fasynchronous-unwind-tables        # Increased reliability of backtraces
    -fexceptions                        # Enable table-based thread cancellation
    -fmacro-backtrace-limit=0
    -fvisibility=hidden                 # Symbols in shared libraries are hidden by default (which is consistent with Windows)
    -W
    -Wall
    -Wno-c++98-compat-pedantic
    -Wno-disabled-macro-expansion
    -Wno-extra-semi
    -Wno-global-constructors
    -Wno-gnu-zero-variadic-macro-arguments
    -Wno-invalid-token-paste
    -Wno-missing-prototypes
    -Wno-reserved-id-macro
    -Wno-unused-command-line-argument
    -Wno-unused-template
    -pipe                               # Avoid temporary files
)
    string(APPEND _CXX_FLAGS " ${_flag}")
endforeach()

# Debug
foreach(_flag IN ITEMS
    -DDEBUG
    -D_DEBUG
    -O0                                 # No optimizations
)
    string(APPEND _CXX_FLAGS_DEBUG " ${_flag}")
endforeach()

# Release args
foreach(_flag IN ITEMS
    -DNDEBUG
    -D_NDEBUG
    -D_FORTIFY_SOURCE=2                 # Run-time buffer overflow detection
    -D_GLIBCXX_ASSERTIONS               # Run-time bounds checking for C++ strings and containers
    -fstack-protector-strong            # Stack smashing protection
    -O3                                 # Advanced optimizations
    -Wl,-z,defs                         # Detect and reject underlinking
    -Wl,-z,now                          # Disable lazy binding
    -Wl,-z,relro                        # Read-only segments after relocation
)
    string(APPEND _CXX_FLAGS_RELEASE " ${_flag}")
endforeach()

# ReleaseMinSize
foreach(_flag IN ITEMS
    -DNDEBUG
    -D_NDEBUG
    -D_FORTIFY_SOURCE=2                 # Run-time buffer overflow detection
    -D_GLIBCXX_ASSERTIONS               # Run-time bounds checking for C++ strings and containers
    -fstack-protector-strong            # Stack smashing protection
    -Os                                 # Optimize for small code
    -Wl,-z,defs                         # Detect and reject underlinking
    -Wl,-z,now                          # Disable lazy binding
    -Wl,-z,relro                        # Read-only segments after relocation
)
    string(APPEND _CXX_FLAGS_RELEASEMINSIZE " ${_flag}")
endforeach()

# ReleaseNoOpt
foreach(_flag IN ITEMS
    -DNDEBUG
    -D_NDEBUG
    -D_FORTIFY_SOURCE=2                 # Run-time buffer overflow detection
    -D_GLIBCXX_ASSERTIONS               # Run-time bounds checking for C++ strings and containers
    -fstack-protector-strong            # Stack smashing protection
    -O0                                 # No optimizations
    -Wl,-z,defs                         # Detect and reject underlinking
    -Wl,-z,now                          # Disable lazy binding
    -Wl,-z,relro                        # Read-only segments after relocation
)
    string(APPEND _CXX_FLAGS_RELEASENOOPT " ${_flag}")
endforeach()

if("$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}" MATCHES "x64")
    string(APPEND _CXX_FLAGS " -m64")
elseif("$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}" MATCHES "x86")
    string(APPEND _CXX_FLAGS " -m32")
else()
    message(FATAL_ERROR "'$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}' is not recognized")
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
    -g                                  # Generate debugging information
    -grecord-gcc-switches               # Store compiler flags in debugging information
)
    string(APPEND _CXX_FLAGS_CppCommon_NO_DEBUG_INFO_FALSE " ${_flag}")
endforeach()

# CppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION
set(_CXX_FLAGS_CppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION_FALSE "-fPIC")
set(_EXE_LINKER_FLAGS_CppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION_FALSE "-pie")

# CppCommon_PREPROCESSOR_OUTPUT
set(_CXX_FLAGS_CppCommon_PREPROCESSOR_OUTPUT_TRUE "-E")

# CppCommon_CODE_COVERAGE
foreach(_flag IN ITEMS
    --coverage
)
    string(APPEND _CXX_FLAGS_CppCommon_CODE_COVERAGE_TRUE " ${_flag}")
endforeach()
