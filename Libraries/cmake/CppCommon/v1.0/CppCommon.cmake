# ----------------------------------------------------------------------
# |
# |  cpp_common.cmake
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-03-01 15:31:28
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
cmake_minimum_required(VERSION 3.5)
cmake_policy(SET CMP0057 NEW)

option(
    CppCommon_CMAKE_FORCE_FLAG_GENERATION
    "Force the repopulation of CMAKE flags, overwriting any changes made after a previous generation."
    "OFF"
)

option(
    CppCommon_CMAKE_DEBUG_OUTPUT
    "Generates cmake debug output"
    "OFF"
)

option(
    CppCommon_UNICODE
    "Use the unicode character set (default is mutli-byte (best practice is to leverage UTF-8))."
    "OFF"
)

option(
    CppCommon_STATIC_CRT
    "Statically link with the CRT (default is dynamic linkage)."
    "OFF"
)

option(
    CppCommon_CODE_COVERAGE
    "Produce builds that can be used when extracting code coverage information (requires a Debug build)."
    "OFF"
)

option(
    CppCommon_NO_DEBUG_INFO
    "Do not generate debug info for the build (this is not recommended)"
    "OFF"
)

option(
    CppCommon_PREPROCESSOR_OUTPUT
    "Generate preprocessor output"
    "OFF"
)

# CMAKE_CONFIGURATION_TYPES
set(_valid_configuration_types 
    Debug                                   # Standard Debug build
    Release                                 # Release build optimizing for speed
    ReleaseMinSize                          # Release build optimizing for code size
    ReleaseNoOpt                            # Release build with no optimizations
)

if(NOT CMAKE_CONFIGURATION_TYPES)
    # Note the following changes from standard cmake:
    #   - `RelWithDebugInfo` has been removed (as it is redundant with the `CppCommon_NO_DEBUG_INFO` flag)
    #   - `MinSizeRel` has been renamed `ReleaseMinSize` (for consistency)
    #   - `ReleaseNoOpt` has been added
    #
    set(CMAKE_CONFIGURATION_TYPES ${_valid_configuration_types})
    
    set(
        CMAKE_CONFIGURATION_TYPES
        "${CMAKE_CONFIGURATION_TYPES}"
        CACHE STRING
        "Available values for CMAKE_BUILD_TYPE"
        FORCE
    )
else()
    # Ensure that each `CMAKE_CONFIGURATION_TYPE` is valid
    foreach(_config_type IN ITEMS ${CMAKE_CONFIGURATION_TYPES})
        if(NOT(${_config_type} IN_LIST _valid_configuration_types))
            message(FATAL_ERROR "'${_config_type}' is not a supported configuration type; valid values are '${_valid_configuration_types}'")
        endif()
    endforeach()
endif()

# Ensure that `CMAKE_BUILD_TYPE` is valid
if (DEFINED CMAKE_BUILD_TYPE AND NOT CMAKE_BUILD_TYPE STREQUAL "" AND NOT ${CMAKE_BUILD_TYPE} IN_LIST CMAKE_CONFIGURATION_TYPES)
    message(FATAL_ERROR "'${CMAKE_BUILD_TYPE}' is not a supported configuration type; valid values are '${CMAKE_CONFIGURATION_TYPES}'")
endif()

# Remove configuration values that won't be used
foreach(_prefix IN ITEMS
    CMAKE_CXX_FLAGS_
    CMAKE_C_FLAGS_
    CMAKE_EXE_LINKER_FLAGS_
    CMAKE_MODULE_LINKER_FLAGS_
    CMAKE_RC_FLAGS_
    CMAKE_SHARED_LINKER_FLAGS_
    CMAKE_STATIC_LINKER_FLAGS_
)
    foreach(_configuration_type IN ITEMS 
        MINSIZEREL
        RELWITHDEBINFO
    )
        unset("${_prefix}${_configuration_type}" CACHE)
    endforeach()
endforeach()

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# |
# |  Compiler/Linker Options
# |
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if(CMAKE_CXX_COMPILER_ID MATCHES MSVC OR (WIN32 AND CMAKE_CXX_COMPILER_ID MATCHES Clang))

    # ----------------------------------------------------------------------
    # |
    # |  Compiler
    # |
    # ----------------------------------------------------------------------
    
    # ----------------------------------------------------------------------
    # |  Static Flags

    # Common Flags
    set(_local_CXX_flags "")
    foreach(_flag IN ITEMS
        /DWIN32
        /D_WINDOWS
        /bigobj                             # generate extended object format
        /EHsc                               # enable C++ EH
        /FC                                 # use full pathnames in diagnostics
        /fp:precise                         # "precise" floating-point model; results are predictable
        /Gd                                 # __cdecl calling convention
        /Gm-                                # Disable minimal rebuild
        /GR                                 # enable C++ RTTI
        /GS                                 # enable security checks
        /Oy-                                # Omit frame pointers
        /permissive-                        # Disable some nonconforming code to compile (feature set subject to change)
        /sdl                                # enable additional security features and warnings
        /W4                                 # warning-level 4
        /WX                                 # treat warnings as errors
        /Zc:forScope                        # enforce Standard C++ for scoping rules
        /Zc:wchar_t                         # wchar_t is the native type, not a typedef
    )
        string(APPEND _local_CXX_flags " ${_flag}")
    endforeach()
    
    # Apply extra arguments for Clang
    if(CMAKE_CXX_COMPILER_ID MATCHES Clang)
        foreach(_flag IN ITEMS
            "-Wno-unused-command-line-argument"
            "-Wno-invalid-token-paste"
            "-Wno-unused-value"             # TODO: Remove this, as it is a valuable warning
                                            # TODO: Enable all warnings (I don't think /W4 is doing it for clang)
        )
            string(APPEND _local_CXX_flags " ${_flag}")
        endforeach()
    endif()

    # Debug
    set(_local_CXX_flags_debug "")
    foreach(_flag IN ITEMS
        /DDEBUG
        /D_DEBUG
        /Ob0                                # inline expansion (default n=0)
        /Od                                 # disable optimizations
        /RTC1                               # Enable fast checks
    )
        string(APPEND _local_CXX_flags_debug " ${_flag}")
    endforeach()

    # Release
    set(_local_CXX_flags_release "")
    foreach(_flag IN ITEMS
        /DNDEBUG
        /D_NDEBUG
        /GL                                 # enable link-time code generation 
        /Gy                                 # separate functions for linker
        /O2                                 # maximum optimizations (favor speed)
        /Ob2                                # inline expansion (default n=0)
        /Oi                                 # enable intrinsic functions
        /Ot                                 # favor code speed
        /Ox                                 # optimizations (favor speed)
    )
        string(APPEND _local_CXX_flags_release " ${_flag}")
    endforeach()

    # ReleaseMinSize
    set(_local_CXX_flags_release_min_size "")
    foreach(_flag IN ITEMS
        /DNDEBUG
        /D_NDEBUG
        /O1                                 # maximum optimizations (favor space)
        /Ob1                                # inline expansion (default n=0)
        /Os                                 # favor code space
    )
        string(APPEND _local_CXX_flags_release_min_size " ${_flag}")
    endforeach()

    # ReleaseNoOpt
    set(_local_CXX_flags_release_no_opt "")
    foreach(_flag IN ITEMS
        /DNDEBUG
        /D_NDEBUG
        /Ob0                                # inline expansion (default n=0)
        /Od                                 # disable optimizations
    )
        string(APPEND _local_CXX_flags_release_no_opt " ${_flag}")
    endforeach()

    # ----------------------------------------------------------------------
    # |  Dynamic Flags
    
    # CppCommon_UNICODE
    set(_local_CXX_flags_CppCommon_UNICODE_TRUE "/DUNICODE /D_UNICODE")
    set(_local_CXX_flags_CppCommon_UNICODE_FALSE "/DMBCS /D_MBCS")

    # CppCommon_STATIC_CRT
    set(_local_CXX_flags_CppCommon_STATIC_CRT_TRUE_DEBUG "/MTd")
    set(_local_CXX_flags_CppCommon_STATIC_CRT_TRUE_RELEASE "/MT")
    set(_local_CXX_flags_CppCommon_STATIC_CRT_TRUE_RELEASEMINSIZE "${_local_CXX_flags_CppCommon_STATIC_CRT_TRUE_RELEASE}")
    set(_local_CXX_flags_CppCommon_STATIC_CRT_TRUE_RELEASENOOPT "${_local_CXX_flags_CppCommon_STATIC_CRT_TRUE_RELEASE}")

    set(_local_CXX_flags_CppCommon_STATIC_CRT_FALSE_DEBUG "/MDd")
    set(_local_CXX_flags_CppCommon_STATIC_CRT_FALSE_RELEASE "/MD")
    set(_local_CXX_flags_CppCommon_STATIC_CRT_FALSE_RELEASEMINSIZE "${_local_CXX_flags_CppCommon_STATIC_CRT_FALSE_RELEASE}")
    set(_local_CXX_flags_CppCommon_STATIC_CRT_FALSE_RELEASENOOPT "${_local_CXX_flags_CppCommon_STATIC_CRT_FALSE_RELEASE}")

    # CppCommon_CODE_COVERAGE
    set(_local_CXX_flags_CppCommon_CODE_COVERAGE_FALSE "")
    foreach(_flag IN ITEMS
        /Zc:inline                          # remove unreferenced function or data if it is COMDAT or has internal linkage only
    )
        string(APPEND _local_CXX_flags_CppCommon_CODE_COVERAGE_FALSE " ${_flag}")
    endforeach()
    
    # CppCommon_NO_DEBUG_INFO
    set(_local_CXX_flags_CppCommon_NO_DEBUG_INFO_FALSE_DEBUG "/ZI")
    set(_local_CXX_flags_CppCommon_NO_DEBUG_INFO_FALSE_RELEASE "/Zi")
    set(_local_CXX_flags_CppCommon_NO_DEBUG_INFO_FALSE_RELEASEMINSIZE "${_local_CXX_flags_CppCommon_NO_DEBUG_INFO_FALSE_RELEASE}")
    set(_local_CXX_flags_CppCommon_NO_DEBUG_INFO_FALSE_RELEASENOOPT "${_local_CXX_flags_CppCommon_NO_DEBUG_INFO_FALSE_RELEASE}")

    # CppCommon_PREPROCESSOR_OUTPUT
    set(_local_CXX_flags_CppCommon_PREPROCESSOR_OUTPUT_FALSE "")
    set(_local_CXX_flags_CppCommon_PREPROCESSOR_OUTPUT_TRUE "/P")

    # ----------------------------------------------------------------------
    # |
    # |  Linker
    # |
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # |  Static Flags
    set(_local_EXE_LINKER_flags "")
    foreach(_flag IN ITEMS
        /DYNAMICBASE                        # Randomized base address
        /MANIFEST                           # Creates a side-by-side manifest file and optionally embeds it in the binary.
        /NXCOMPAT                           # Data Execution Prevention 
        /MANIFESTUAC:"level='asInvoker' uiAccess='false'"   # Specifies whether User Account Control (UAC) information is embedded in the program manifest.
        /TLBID:1                            # Specifies the resource ID of the linker-generated type library.
    )
        string(APPEND _local_EXE_LINKER_flags " ${_flag}")
    endforeach()

    set(_local_EXE_LINKER_flags_debug "")
    foreach(_flag IN ITEMS
        /INCREMENTAL                        # Leverage incremental linking
    )
        string(APPEND _local_EXE_LINKER_flags_debug " ${_flag}")
    endforeach()

    set(_local_EXE_LINKER_flags_release "")
    foreach(_flag IN ITEMS 
        /LTCG                               # Link-time code generation
        /INCREMENTAL:NO                     # Do not leverage incremental linking
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
    set(_local_EXE_LINKER_flags_CppCommon_CODE_COVERAGE_TRUE "/PROFILE")

    # CppCommon_NO_DEBUG_INFO
    set(_local_EXE_LINKER_flags_CppCommon_NO_DEBUG_INFO_FALSE "/DEBUG")

else()
    message(FATAL_ERROR "The compiler '${CMAKE_CXX_COMPILER_ID}' is not supported.")
endif()

# ----------------------------------------------------------------------
# |
# |  Persist the static flags
# |
# ----------------------------------------------------------------------
if(DEFINED _local_CXX_flags AND (${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _CXX_FLAGS_UPDATED))
    set(CMAKE_CXX_FLAGS ${_local_CXX_flags} CACHE string "Flags used by the CXX compiler during all builds." FORCE)
    set(_CXX_FLAGS_UPDATED true CACHE bool "Indicates that CMAKE_CXX_FLAGS has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

if(DEFINED _local_CXX_flags_debug AND (${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _CXX_FLAGS_DEBUG_UPDATED))
    set(CMAKE_CXX_FLAGS_DEBUG ${_local_CXX_flags_debug} CACHE string "Flags used by the CXX compiler during Debug builds." FORCE)
    set(_CXX_FLAGS_DEBUG_UPDATED true CACHE bool "Indicates that CMAKE_CXX_FLAGS_DEBUG has already been updated and should not be updated during function configuration/generation cycles." FORCE)
endif()

if(DEFINED _local_CXX_flags_release AND (${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _CXX_FLAGS_RELEASE_UPDATED))
    set(CMAKE_CXX_FLAGS_RELEASE ${_local_CXX_flags_release} CACHE string "Flags used by the CXX compiler during Release builds." FORCE)
    set(_CXX_FLAGS_RELEASE_UPDATED true CACHE bool "Indicates that CMAKE_CXX_FLAGS_RELEASE has already been updated and should not be updated during function configuration/generation cycles." FORCE)
endif()

if(DEFINED _local_CXX_flags_release_min_size AND (${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _CXX_FLAGS_RELEASEMINSIZE_UPDATED))
    set(CMAKE_CXX_FLAGS_RELEASEMINSIZE ${_local_CXX_flags_release_min_size} CACHE string "Flags used by the CXX compiler during ReleaseMinSize builds." FORCE)
    set(_CXX_FLAGS_RELEASEMINSIZE_UPDATED true CACHE bool "Indicates that CMAKE_CXX_FLAGS_RELEASEMINSIZE has already been updated and should not be updated during function configuration/generation cycles." FORCE)
endif()

if(DEFINED _local_CXX_flags_release_no_opt AND (${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _CXX_FLAGS_RELEASENOOPT_UPDATED))
    set(CMAKE_CXX_FLAGS_RELEASENOOPT ${_local_CXX_flags_release_no_opt} CACHE string "Flags used by the CXX compiler during ReleaseNoOpt builds." FORCE)
    set(_CXX_FLAGS_RELEASENOOPT_UPDATED true CACHE bool "Indicates that CMAKE_CXX_FLAGS_RELEASENOOPT has already been updated and should not be updated during function configuration/generation cycles." FORCE)
endif()

if(DEFINED _local_EXE_LINKER_flags AND (${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _LINKER_FLAGS_UPDATED))
    set(CMAKE_EXE_LINKER_FLAGS ${_local_EXE_LINKER_flags} CACHE string "Flags used by the linker during all builds." FORCE)
    set(_LINKER_FLAGS_UPDATED true CACHE bool "Indicates that CMAKE_EXE_LINKER_FLAGS has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

if(DEFINED _local_EXE_LINKER_flags_debug AND (${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _LINKER_FLAGS_DEBUG_UPDATED))
    set(CMAKE_EXE_LINKER_FLAGS_DEBUG ${_local_EXE_LINKER_flags_debug} CACHE string "Flags used by the linker during Debug builds." FORCE)
    set(_LINKER_FLAGS_DEBUG_UPDATED true CACHE bool "Indicates that CMAKE_EXE_LINKER_FLAGS_DEBUG has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

if(DEFINED _local_EXE_LINKER_flags_release AND (${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _LINKER_FLAGS_RELEASE_UPDATED))
    set(CMAKE_EXE_LINKER_FLAGS_RELEASE ${_local_EXE_LINKER_flags_release} CACHE string "Flags used by the linker during Release builds." FORCE)
    set(_LINKER_FLAGS_RELEASE_UPDATED true CACHE bool "Indicates that CMAKE_EXE_LINKER_FLAGS_RELEASE has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

if(DEFINED _local_EXE_LINKER_flags_release_min_size AND (${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _LINKER_FLAGS_RELEASEMINSIZE_UPDATED))
    set(CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE ${_local_EXE_LINKER_flags_release_min_size} CACHE string "Flags used by the linker during ReleaseMinSize builds." FORCE)
    set(_LINKER_FLAGS_RELEASEMINSIZE_UPDATED true CACHE bool "Indicates that CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

if(DEFINED _local_EXE_LINKER_flags_release_no_opt AND (${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _LINKER_FLAGS_RELEASENOOPT_UPDATED))
    set(CMAKE_EXE_LINKER_FLAGS_RELEASENOOPT ${_local_EXE_LINKER_flags_release_no_opt} CACHE string "Flags used by the linker during ReleaseNoOpt builds." FORCE)
    set(_LINKER_FLAGS_RELEASENOOPT_UPDATED true CACHE bool "Indicates that CMAKE_EXE_LINKER_FLAGS_RELEASENOOPT has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

# ----------------------------------------------------------------------
# |
# |  Persist the dynamic flags
# |
# ----------------------------------------------------------------------
foreach(_flag_prefix IN ITEMS
    CXX
    EXE_LINKER
)
    foreach(_flag_type IN ITEMS 
        CppCommon_UNICODE
        CppCommon_STATIC_CRT
        CppCommon_CODE_COVERAGE
        CppCommon_NO_DEBUG_INFO
        CppCommon_PREPROCESSOR_OUTPUT
    )
        set(_local_flag_name "_local_${_flag_prefix}_flags_${_flag_type}")
        if(DEFINED "${_local_flag_name}")
            set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}")
            if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED ${_cached_flag_name})
                set("${_cached_flag_name}" "${${_local_flag_name}}" CACHE string "" FORCE)
            endif()
        endif()

        foreach(_boolean_type IN ITEMS
            TRUE
            FALSE
        )
            set(_local_flag_name "_local_${_flag_prefix}_flags_${_flag_type}_${_boolean_type}") 
            if(DEFINED "${_local_flag_name}")
                set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}_${_boolean_type}")
                if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED ${_cached_flag_name})
                    set("${_cached_flag_name}" "${${_local_flag_name}}" CACHE string "" FORCE)
                endif()
            endif()

            foreach(_configuration_type IN ITEMS
                DEBUG
                RELEASE
                RELEASEMINSIZE
                RELEASENOOPT
            )
                set(_local_flag_name "_local_${_flag_prefix}_flags_${_flag_type}_${_boolean_type}_${_configuration_type}")
                if(DEFINED "${_local_flag_name}")
                    set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}_${_boolean_type}_${_configuration_type}")
                    if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED ${_cached_flag_name})
                        set("${_cached_flag_name}" "${${_local_flag_name}}" CACHE string "" FORCE)
                    endif()
                endif()
            endforeach()
        endforeach()
    endforeach()
endforeach()

# ----------------------------------------------------------------------
# |
# |  Apply the dynamic flags
# |
# ----------------------------------------------------------------------
foreach(_flag_prefix IN ITEMS
    CXX
    EXE_LINKER
)
    foreach(_flag_type IN ITEMS 
        CppCommon_UNICODE
        CppCommon_STATIC_CRT
        CppCommon_CODE_COVERAGE
        CppCommon_NO_DEBUG_INFO
        CppCommon_PREPROCESSOR_OUTPUT
    )
        set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}")
        if(DEFINED "${_cached_flag_name}")
            string(APPEND CMAKE_${_flag_prefix}_FLAGS " ${${_cached_flag_name}}")
        endif()

        foreach(_boolean_type IN ITEMS 
            TRUE
            FALSE
        )
            if(
                ("${_boolean_type}" MATCHES "TRUE" AND "${${_flag_type}}") OR
                ("${_boolean_type}" MATCHES "FALSE" AND NOT "${${_flag_type}}")
            ) 
                set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}_${_boolean_type}")
                if(DEFINED "${_cached_flag_name}")
                    string(APPEND CMAKE_${_flag_prefix}_FLAGS " ${${_cached_flag_name}}")
                endif()

                foreach(_config_type IN ITEMS
                    DEBUG
                    RELEASE
                    RELEASEMINSIZE
                    RELEASENOOPT
                )
                    set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}_${_boolean_type}_${_config_type}")
                    if(DEFINED "${_cached_flag_name}")
                        string(APPEND CMAKE_${_flag_prefix}_FLAGS_${_config_type} " ${${_cached_flag_name}}")
                    endif()
                endforeach()
            endif()
        endforeach()
    endforeach()
endforeach()

# Handle the c flags
set(CMAKE_C_FLAGS "${CMAKE_CXX_FLAGS}")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE}")
set(CMAKE_C_FLAGS_RELEASEMINSIZE "${CMAKE_CXX_FLAGS_RELEASEMINSIZE}")
set(CMAKE_C_FLAGS_RELEASENOOPT "${CMAKE_CXX_FLAGS_RELEASENOOPT}")

# Handle the other linker flag types
set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS}")
set(CMAKE_MODULE_LINKER_FLAGS_DEBUG "${CMAKE_EXE_LINKER_FLAGS_DEBUG}")
set(CMAKE_MODULE_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE}")
set(CMAKE_MODULE_LINKER_FLAGS_RELEASEMINSIZE "${CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE}")
set(CMAKE_MODULE_LINKER_FLAGS_RELEASENOOPT "${CMAKE_EXE_LINKER_FLAGS_RELEASENOOPT}")

set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS}")
set(CMAKE_SHARED_LINKER_FLAGS_DEBUG "${CMAKE_EXE_LINKER_FLAGS_DEBUG}")
set(CMAKE_SHARED_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE}")
set(CMAKE_SHARED_LINKER_FLAGS_RELEASEMINSIZE "${CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE}")
set(CMAKE_SHARED_LINKER_FLAGS_RELEASENOOPT "${CMAKE_EXE_LINKER_FLAGS_RELEASENOOPT}")

set(CMAKE_STATIC_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS}")
set(CMAKE_STATIC_LINKER_FLAGS_DEBUG "${CMAKE_EXE_LINKER_FLAGS_DEBUG}")
set(CMAKE_STATIC_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE}")
set(CMAKE_STATIC_LINKER_FLAGS_RELEASEMINSIZE "${CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE}")
set(CMAKE_STATIC_LINKER_FLAGS_RELEASENOOPT "${CMAKE_EXE_LINKER_FLAGS_RELEASENOOPT}")

if(${CppCommon_CMAKE_DEBUG_OUTPUT})
    # Output the results
    message(STATUS "CMAKE_CXX_FLAGS:                    ${CMAKE_CXX_FLAGS}")
    message(STATUS "CMAKE_CXX_FLAGS_DEBUG:              ${CMAKE_CXX_FLAGS_DEBUG}")
    message(STATUS "CMAKE_CXX_FLAGS_RELEASE:            ${CMAKE_CXX_FLAGS_RELEASE}")
    message(STATUS "CMAKE_CXX_FLAGS_RELEASEMINSIZE:     ${CMAKE_CXX_FLAGS_RELEASEMINSIZE}")
    message(STATUS "CMAKE_CXX_FLAGS_RELEASENOOPT:       ${CMAKE_CXX_FLAGS_RELEASENOOPT}")
    message(STATUS "")
    message(STATUS "CMAKE_C_FLAGS:                      ${CMAKE_C_FLAGS}")
    message(STATUS "CMAKE_C_FLAGS_DEBUG:                ${CMAKE_C_FLAGS_DEBUG}")
    message(STATUS "CMAKE_C_FLAGS_RELEASE:              ${CMAKE_C_FLAGS_RELEASE}")
    message(STATUS "CMAKE_C_FLAGS_RELEASEMINSIZE:       ${CMAKE_C_FLAGS_RELEASEMINSIZE}")
    message(STATUS "CMAKE_C_FLAGS_RELEASENOOPT:         ${CMAKE_C_FLAGS_RELEASENOOPT}")
    message(STATUS "")
    message(STATUS "CMAKE_EXE_LINKER_FLAGS:                     ${CMAKE_EXE_LINKER_FLAGS}")
    message(STATUS "CMAKE_EXE_LINKER_FLAGS_DEBUG:               ${CMAKE_EXE_LINKER_FLAGS_DEBUG}")
    message(STATUS "CMAKE_EXE_LINKER_FLAGS_RELEASE:             ${CMAKE_EXE_LINKER_FLAGS_RELEASE}")
    message(STATUS "CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE:      ${CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE}")
    message(STATUS "CMAKE_EXE_LINKER_FLAGS_RELEASENOOPT:        ${CMAKE_EXE_LINKER_FLAGS_RELEASENOOPT}")
    message(STATUS "")
    message(STATUS "CMAKE_MODULE_LINKER_FLAGS:                  ${CMAKE_MODULE_LINKER_FLAGS}")
    message(STATUS "CMAKE_MODULE_LINKER_FLAGS_DEBUG:            ${CMAKE_MODULE_LINKER_FLAGS_DEBUG}")
    message(STATUS "CMAKE_MODULE_LINKER_FLAGS_RELEASE:          ${CMAKE_MODULE_LINKER_FLAGS_RELEASE}")
    message(STATUS "CMAKE_MODULE_LINKER_FLAGS_RELEASEMINSIZE:   ${CMAKE_MODULE_LINKER_FLAGS_RELEASEMINSIZE}")
    message(STATUS "CMAKE_MODULE_LINKER_FLAGS_RELEASENOOPT:     ${CMAKE_MODULE_LINKER_FLAGS_RELEASENOOPT}")
    message(STATUS "")
    message(STATUS "CMAKE_SHARED_LINKER_FLAGS:                  ${CMAKE_SHARED_LINKER_FLAGS}")
    message(STATUS "CMAKE_SHARED_LINKER_FLAGS_DEBUG:            ${CMAKE_SHARED_LINKER_FLAGS_DEBUG}")
    message(STATUS "CMAKE_SHARED_LINKER_FLAGS_RELEASE:          ${CMAKE_SHARED_LINKER_FLAGS_RELEASE}")
    message(STATUS "CMAKE_SHARED_LINKER_FLAGS_RELEASEMINSIZE:   ${CMAKE_SHARED_LINKER_FLAGS_RELEASEMINSIZE}")
    message(STATUS "CMAKE_SHARED_LINKER_FLAGS_RELEASENOOPT:     ${CMAKE_SHARED_LINKER_FLAGS_RELEASENOOPT}")
    message(STATUS "")
    message(STATUS "CMAKE_STATIC_LINKER_FLAGS:                  ${CMAKE_STATIC_LINKER_FLAGS}")
    message(STATUS "CMAKE_STATIC_LINKER_FLAGS_DEBUG:            ${CMAKE_STATIC_LINKER_FLAGS_DEBUG}")
    message(STATUS "CMAKE_STATIC_LINKER_FLAGS_RELEASE:          ${CMAKE_STATIC_LINKER_FLAGS_RELEASE}")
    message(STATUS "CMAKE_STATIC_LINKER_FLAGS_RELEASEMINSIZE:   ${CMAKE_STATIC_LINKER_FLAGS_RELEASEMINSIZE}")
    message(STATUS "CMAKE_STATIC_LINKER_FLAGS_RELEASENOOPT:     ${CMAKE_STATIC_LINKER_FLAGS_RELEASENOOPT}")
    message(STATUS "")
    message(STATUS "***** CMAKE_BUILD_TYPE: '${CMAKE_BUILD_TYPE}' *****")
    message(STATUS "")
endif()
