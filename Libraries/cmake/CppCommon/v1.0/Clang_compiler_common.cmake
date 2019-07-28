# ----------------------------------------------------------------------
# |
# |  Clang_compiler_common.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-07-28 08:10:54
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
    -W
    -Wall
    -Wno-c++98-compat-pedantic
    -Wno-disabled-macro-expansion
    -Wno-extra-semi
    -Wno-gnu-zero-variadic-macro-arguments
    -Wno-invalid-token-paste
    -Wno-missing-prototypes
    -Wno-reserved-id-macro
    -Wno-unused-command-line-argument
    -Wno-unused-template
)
    string(APPEND _local_CXX_flags " ${_flag}")
endforeach()

if("$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}" MATCHES "x64")
    string(APPEND _local_CXX_flags " -m64")
elseif("$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}" MATCHES "x86")
    string(APPEND _local_CXX_flags " -m32")
else()
    message(FATAL_ERROR "'$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}' is not recognized")
endif()

# ----------------------------------------------------------------------
# |  Dynamic Flags

# CppCommon_CODE_COVERAGE
foreach(_flag IN ITEMS
    --coverage
)
    string(APPEND _local_CXX_flags_CppCommon_CODE_COVERAGE_TRUE " ${_flag}")
endforeach()
