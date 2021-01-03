# ----------------------------------------------------------------------
# |
# |  MSVC_compiler.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-07-28 09:04:34
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-21
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------

# When profiling, MSVC is not able to instrument x64 binaries compiled with the
# static CRT. If this is the case, disable the static CRT.
if(${CppCommon_CODE_COVERAGE} AND ${CppCommon_STATIC_CRT} AND "$ENV{DEVELOPMENT_ENVIRONMENT_CPP_ARCHITECTURE}" MATCHES "x64")
    message(WARNING "The static CRT cannot be used with code coverage builds on x64; disabling static CRT.\n")
    set(CppCommon_STATIC_CRT OFF)
endif()

# ----------------------------------------------------------------------
# |  Static Flags
foreach(_flag IN ITEMS
    /DWIN32
    /D_WINDOWS
    /bigobj                                 # generate extended object format
    /EHsc                                   # enable C++ EH
    /FC                                     # use full pathnames in diagnostics
    /fp:precise                             # "precise" floating-point model; results are predictable
    /Gd                                     # __cdecl calling convention
    /Gm-                                    # Disable minimal rebuild
    /GR                                     # enable C++ RTTI
    /GS                                     # enable security checks
    /Oy-                                    # Omit frame pointers
    /permissive-                            # Disable some nonconforming code to compile (feature set subject to change)
    /sdl                                    # enable additional security features and warnings
    /W4                                     # warning-level 4
    /WX                                     # treat warnings as errors
    /Zc:forScope                            # enforce Standard C++ for scoping rules
    /Zc:wchar_t                             # wchar_t is the native type, not a typedef
)
    STRING(APPEND _CXX_FLAGS " ${_flag}")
endforeach()

# Debug
foreach(_flag IN ITEMS
    /DDEBUG
    /D_DEBUG
    /Ob0                                    # inline expansion (default n=0)
    /Od                                     # disable optimizations
    /RTC1                                   # Enable fast checks
)
    STRING(APPEND _CXX_FLAGS_DEBUG " ${_flag}")
endforeach()

# Release
foreach(_flag IN ITEMS
    /DNDEBUG
    /D_NDEBUG
    /GL                                     # enable link-time code generation
    /Gy                                     # separate functions for linker
    /O2                                     # maximum optimizations (favor speed)
    /Ob2                                    # inline expansion (default n=0)
    /Oi                                     # enable intrinsic functions
    /Ot                                     # favor code speed
    /Ox                                     # optimizations (favor speed)
)
    STRING(APPEND _CXX_FLAGS_RELEASE " ${_flag}")
endforeach()

if(CMAKE_CXX_COMPILER_ID MATCHES Clang)
    foreach(_flag IN ITEMS
        "-Xclang -O3"                       # Advanced optimizations
        "-Xclang -fno-inline"               # Inline optimizations present problems with -O3
    )
        STRING(APPEND _CXX_FLAGS_RELEASE " ${_flag}")
    endforeach()
endif()

# ReleaseMinSize
foreach(_flag IN ITEMS
    /DNDEBUG
    /D_NDEBUG
    /O1                                     # maximum optimizations (favor space)
    /Ob1                                    # inline expansion (default n=0)
    /Os                                     # favor code space
)
    STRING(APPEND _CXX_FLAGS_RELEASEMINSIZE " ${_flag}")
endforeach()

# ReleaseNoOpt
foreach(_flag IN ITEMS
    /DNDEBUG
    /D_NDEBUG
    /Ob0                                    # inline expansion (default n=0)
    /Od                                     # disable optimizations
)
    STRING(APPEND _CXX_FLAGS_RELEASENOOPT " ${_flag}")
endforeach()

# ----------------------------------------------------------------------
# |  Dynamic Flags

# CppCommon_UNICODE
set(_CXX_FLAGS_CppCommon_UNICODE_TRUE "/DUNICODE /D_UNICODE")
set(_CXX_FLAGS_CppCommon_UNICODE_FALSE "/DMBCS /D_MBCS")

# CppCommon_STATIC_CRT
set(_CXX_FLAGS_CppCommon_STATIC_CRT_TRUE_DEBUG "/MTd /D_MT")
set(_CXX_FLAGS_CppCommon_STATIC_CRT_TRUE_RELEASE "/MT /D_MT")
set(_CXX_FLAGS_CppCommon_STATIC_CRT_TRUE_RELEASEMINSIZE "${_CXX_FLAGS_CppCommon_STATIC_CRT_TRUE_RELEASE}")
set(_CXX_FLAGS_CppCommon_STATIC_CRT_TRUE_RELEASENOOPT "${_CXX_FLAGS_CppCommon_STATIC_CRT_TRUE_RELEASE}")

set(_CXX_FLAGS_CppCommon_STATIC_CRT_FALSE_DEBUG "/MDd /D_MT /D_DLL")
set(_CXX_FLAGS_CppCommon_STATIC_CRT_FALSE_RELEASE "/MD /D_MT /D_DLL")
set(_CXX_FLAGS_CppCommon_STATIC_CRT_FALSE_RELEASEMINSIZE "${_CXX_FLAGS_CppCommon_STATIC_CRT_FALSE_RELEASE}")
set(_CXX_FLAGS_CppCommon_STATIC_CRT_FALSE_RELEASENOOPT "${_CXX_FLAGS_CppCommon_STATIC_CRT_FALSE_RELEASE}")

# CppCommon_CODE_COVERAGE
foreach(_flag IN ITEMS
    /Zc:inline                              # remove unreferenced function or data if it is COMDAT or has internal linkage only
)
    STRING(APPEND _CXX_FLAGS_CppCommon_CODE_COVERAGE_FALSE " ${_flag}")
endforeach()

# CppCommon_NO_DEBUG_INFO
set(_CXX_FLAGS_CppCommon_NO_DEBUG_INFO_FALSE_DEBUG "/ZI")
set(_CXX_FLAGS_CppCommon_NO_DEBUG_INFO_FALSE_RELEASE "/Zi")
set(_CXX_FLAGS_CppCommon_NO_DEBUG_INFO_FALSE_RELEASEMINSIZE "${_CXX_FLAGS_CppCommon_NO_DEBUG_INFO_FALSE_RELEASE}")
set(_CXX_FLAGS_CppCommon_NO_DEBUG_INFO_FALSE_RELEASENOOPT "${_CXX_FLAGS_CppCommon_NO_DEBUG_INFO_FALSE_RELEASE}")

# CppCommon_PREPROCESSOR_OUTPUT
set(_CXX_FLAGS_CppCommon_PREPROCESSOR_OUTPUT_TRUE "/P")
