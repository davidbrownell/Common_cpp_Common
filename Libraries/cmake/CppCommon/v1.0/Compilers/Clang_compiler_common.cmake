# ----------------------------------------------------------------------
# |
# |  Clang_compiler_common.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-07-28 08:10:54
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-20
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
    -fdiagnostics-absolute-paths
    -fmacro-backtrace-limit=0
    -W
    -Wall                                   # All warnings
    -Werror                                 # Treat warnings as errors
    -Wno-c++98-compat-pedantic
    -Wno-disabled-macro-expansion
    -Wno-extra-semi
    -Wno-extra-semi-stmt
    -Wno-global-constructors
    -Wno-gnu-zero-variadic-macro-arguments
    -Wno-invalid-token-paste
    -Wno-missing-prototypes
    -Wno-reserved-id-macro
    -Wno-string-conversion
    -Wno-undefined-inline
    -Wno-unused-command-line-argument
    -Wno-unused-member-function
    -Wno-unused-template
)
    STRING(APPEND _CXX_FLAGS " ${_flag}")
endforeach()

if("$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}" MATCHES "x64")
    STRING(APPEND _CXX_FLAGS " -m64")
elseif("$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}" MATCHES "x86")
    STRING(APPEND _CXX_FLAGS " -m32")
else()
    message(FATAL_ERROR "'$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}' is not recognized")
endif()

# ----------------------------------------------------------------------
# |  Dynamic Flags

# CppCommon_CODE_COVERAGE
foreach(_flag IN ITEMS
    --coverage                              # For use with gcov (generates "*.gcno" and "*.gcna")

    # TODO: Note that these settings create linker problems for some code; more investigation is required.
    # TODO  -fprofile-instr-generate                # For use with llvm-cov (generates "default.profraw")
    # TODO  -fcoverage-mapping                      # For use with llvm-cov (generates "default.profraw")
)
    STRING(APPEND _CXX_FLAGS_CppCommon_CODE_COVERAGE_TRUE " ${_flag}")
endforeach()
