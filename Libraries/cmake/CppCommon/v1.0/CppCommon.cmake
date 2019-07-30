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

cmake_policy(SET CMP0056 NEW)               # Honor link flags
cmake_policy(SET CMP0057 NEW)               # Support IN_LIST
cmake_policy(SET CMP0066 NEW)               # Honor compile flags

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
    "Use the unicode character set (default is multi-byte (best practice is to leverage UTF-8))."
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
    CppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION
    "Do not generate code with Address Space Layout Randomization (ASLR). This should not be enabled unless it is possible to compile dependencies with ASLR."
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

# Set the local flags to empty values
foreach(_flag_prefix IN ITEMS
    CXX
    EXE_LINKER
)
    set("_local_${_flag_prefix}_flags" "")

    set("_local_${_flag_prefix}_flags_DEBUG" "")
    set("_local_${_flag_prefix}_flags_RELEASE" "")
    set("_local_${_flag_prefix}_flags_RELEASEMINSIZE" "")
    set("_local_${_flag_prefix}_flags_RELEASENOOPT" "")

    foreach(_flag_type IN ITEMS
        CppCommon_UNICODE
        CppCommon_STATIC_CRT
        CppCommon_CODE_COVERAGE
        CppCommon_NO_DEBUG_INFO
        CppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION
        CppCommon_PREPROCESSOR_OUTPUT
    )
        foreach(_boolean_type IN ITEMS
            TRUE
            FALSE
        )
            set("_local_${_flag_prefix}_flags_${_flag_type}" "")

            foreach(_configuration_type IN ITEMS
                DEBUG
                RELEASE
                RELEASEMINSIZE
                RELEASENOOPT
            )
                set("_local_${_flag_prefix}_flags_${_flag_type}_${_configuration_type}" "")

            endforeach()
        endforeach()
    endforeach()
endforeach()

get_filename_component(_compiler_basename "${CMAKE_CXX_COMPILER}" NAME)

# ----------------------------------------------------------------------
# |
# |  Compiler- and Linker-specific Flags
# |
# ----------------------------------------------------------------------
if(CMAKE_CXX_COMPILER_ID MATCHES Clang)
    include(${CMAKE_CURRENT_LIST_DIR}/Compilers/Clang_compiler_common.cmake)
    include(${CMAKE_CURRENT_LIST_DIR}/Compilers/Clang_linker_common.cmake)
endif()

if(CMAKE_CXX_COMPILER_ID MATCHES MSVC OR (CMAKE_CXX_COMPILER_ID MATCHES Clang AND _compiler_basename MATCHES "clang-cl.exe"))
    include(${CMAKE_CURRENT_LIST_DIR}/Compilers/MSVC_compiler.cmake)
    include(${CMAKE_CURRENT_LIST_DIR}/Compilers/MSVC_linker.cmake)

elseif(CMAKE_CXX_COMPILER_ID MATCHES Clang)
    include(${CMAKE_CURRENT_LIST_DIR}/Compilers/Clang_compiler.cmake)
    include(${CMAKE_CURRENT_LIST_DIR}/Compilers/Clang_linker.cmake)

else()
    message(FATAL_ERROR "The compiler '${CMAKE_CXX_COMPILER_ID}' is not supported.")

endif()

# ----------------------------------------------------------------------
# |
# |  Persist the static flags
# |
# ----------------------------------------------------------------------
if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _CXX_FLAGS_UPDATED)
    set(CMAKE_CXX_FLAGS ${_local_CXX_flags} CACHE string "Flags used by the CXX compiler during all builds." FORCE)
    set(_CXX_FLAGS_UPDATED true CACHE bool "Indicates that CMAKE_CXX_FLAGS has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _CXX_FLAGS_DEBUG_UPDATED)
    set(CMAKE_CXX_FLAGS_DEBUG ${_local_CXX_flags_DEBUG} CACHE string "Flags used by the CXX compiler during Debug builds." FORCE)
    set(_CXX_FLAGS_DEBUG_UPDATED true CACHE bool "Indicates that CMAKE_CXX_FLAGS_DEBUG has already been updated and should not be updated during function configuration/generation cycles." FORCE)
endif()

if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _CXX_FLAGS_RELEASE_UPDATED)
    set(CMAKE_CXX_FLAGS_RELEASE ${_local_CXX_flags_RELEASE} CACHE string "Flags used by the CXX compiler during Release builds." FORCE)
    set(_CXX_FLAGS_RELEASE_UPDATED true CACHE bool "Indicates that CMAKE_CXX_FLAGS_RELEASE has already been updated and should not be updated during function configuration/generation cycles." FORCE)
endif()

if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _CXX_FLAGS_RELEASEMINSIZE_UPDATED)
    set(CMAKE_CXX_FLAGS_RELEASEMINSIZE ${_local_CXX_flags_RELEASEMINSIZE} CACHE string "Flags used by the CXX compiler during ReleaseMinSize builds." FORCE)
    set(_CXX_FLAGS_RELEASEMINSIZE_UPDATED true CACHE bool "Indicates that CMAKE_CXX_FLAGS_RELEASEMINSIZE has already been updated and should not be updated during function configuration/generation cycles." FORCE)
endif()

if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _CXX_FLAGS_RELEASENOOPT_UPDATED)
    set(CMAKE_CXX_FLAGS_RELEASENOOPT ${_local_CXX_flags_RELEASENOOPT} CACHE string "Flags used by the CXX compiler during ReleaseNoOpt builds." FORCE)
    set(_CXX_FLAGS_RELEASENOOPT_UPDATED true CACHE bool "Indicates that CMAKE_CXX_FLAGS_RELEASENOOPT has already been updated and should not be updated during function configuration/generation cycles." FORCE)
endif()

if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _LINKER_FLAGS_UPDATED)
    set(CMAKE_EXE_LINKER_FLAGS ${_local_EXE_LINKER_flags} CACHE string "Flags used by the linker during all builds." FORCE)
    set(_LINKER_FLAGS_UPDATED true CACHE bool "Indicates that CMAKE_EXE_LINKER_FLAGS has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _LINKER_FLAGS_DEBUG_UPDATED)
    set(CMAKE_EXE_LINKER_FLAGS_DEBUG ${_local_EXE_LINKER_flags_DEBUG} CACHE string "Flags used by the linker during Debug builds." FORCE)
    set(_LINKER_FLAGS_DEBUG_UPDATED true CACHE bool "Indicates that CMAKE_EXE_LINKER_FLAGS_DEBUG has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _LINKER_FLAGS_RELEASE_UPDATED)
    set(CMAKE_EXE_LINKER_FLAGS_RELEASE ${_local_EXE_LINKER_flags_RELEASE} CACHE string "Flags used by the linker during Release builds." FORCE)
    set(_LINKER_FLAGS_RELEASE_UPDATED true CACHE bool "Indicates that CMAKE_EXE_LINKER_FLAGS_RELEASE has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _LINKER_FLAGS_RELEASEMINSIZE_UPDATED)
    set(CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE ${_local_EXE_LINKER_flags_RELEASEMINSIZE} CACHE string "Flags used by the linker during ReleaseMinSize builds." FORCE)
    set(_LINKER_FLAGS_RELEASEMINSIZE_UPDATED true CACHE bool "Indicates that CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE has already been updated and should not be updated during future configuration/generation cycles." FORCE)
endif()

if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED _LINKER_FLAGS_RELEASENOOPT_UPDATED)
    set(CMAKE_EXE_LINKER_FLAGS_RELEASENOOPT ${_local_EXE_LINKER_flags_RELEASENOOPT} CACHE string "Flags used by the linker during ReleaseNoOpt builds." FORCE)
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
        CppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION
        CppCommon_PREPROCESSOR_OUTPUT
    )
        set(_local_flag_name "_local_${_flag_prefix}_flags_${_flag_type}")
        set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}")
        if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED ${_cached_flag_name})
            set("${_cached_flag_name}" "${${_local_flag_name}}" CACHE string "" FORCE)
        endif()

        foreach(_boolean_type IN ITEMS
            TRUE
            FALSE
        )
            set(_local_flag_name "_local_${_flag_prefix}_flags_${_flag_type}_${_boolean_type}")
            set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}_${_boolean_type}")
            if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED ${_cached_flag_name})
                set("${_cached_flag_name}" "${${_local_flag_name}}" CACHE string "" FORCE)
            endif()

            foreach(_configuration_type IN ITEMS
                DEBUG
                RELEASE
                RELEASEMINSIZE
                RELEASENOOPT
            )
                set(_local_flag_name "_local_${_flag_prefix}_flags_${_flag_type}_${_boolean_type}_${_configuration_type}")
                set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}_${_boolean_type}_${_configuration_type}")
                if(${CppCommon_CMAKE_FORCE_FLAG_GENERATION} OR NOT DEFINED ${_cached_flag_name})
                    set("${_cached_flag_name}" "${${_local_flag_name}}" CACHE string "" FORCE)
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
        CppCommon_NO_ADDRESS_SPACE_LAYOUT_RANDOMIZATION
        CppCommon_PREPROCESSOR_OUTPUT
    )
        set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}")
        if(NOT "${_cached_flag_name}" STREQUAL "")
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
                if(NOT "${_cached_flag_name}" STREQUAL "")
                    string(APPEND CMAKE_${_flag_prefix}_FLAGS " ${${_cached_flag_name}}")
                endif()

                foreach(_config_type IN ITEMS
                    DEBUG
                    RELEASE
                    RELEASEMINSIZE
                    RELEASENOOPT
                )
                    set(_cached_flag_name "_${_flag_prefix}_FLAGS_${_flag_type}_${_boolean_type}_${_config_type}")
                    if(NOT "${_cached_flag_name}" STREQUAL "")
                        string(APPEND CMAKE_${_flag_prefix}_FLAGS_${_config_type} " ${${_cached_flag_name}}")
                    endif()
                endforeach()
            endif()
        endforeach()
    endforeach()
endforeach()

# ----------------------------------------------------------------------
# |  C Flags
set(CMAKE_C_FLAGS "${CMAKE_CXX_FLAGS}")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE}")
set(CMAKE_C_FLAGS_RELEASEMINSIZE "${CMAKE_CXX_FLAGS_RELEASEMINSIZE}")
set(CMAKE_C_FLAGS_RELEASENOOPT "${CMAKE_CXX_FLAGS_RELEASENOOPT}")

# TODO: Verify Static Linker flags (GCC)
# TODO: Verify Shared Linker flags (GCC)
# TODO: Verify Module Linker flags (GCC)

# Flags have been verified for:
#   - MSVC
#   - Clang (Windows using MSVC)
#   - Clang (Linux)

# ----------------------------------------------------------------------
# |  Linker Flags

# No linker settings for static libs
set(CMAKE_STATIC_LINKER_FLAGS "")
set(CMAKE_STATIC_LINKER_FLAGS_DEBUG "")
set(CMAKE_STATIC_LINKER_FLAGS_RELEASE "")
set(CMAKE_STATIC_LINKER_FLAGS_RELEASEMINSIZE "")
set(CMAKE_STATIC_LINKER_FLAGS_RELEASENOOPT "")

set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS}")
set(CMAKE_SHARED_LINKER_FLAGS_DEBUG "${CMAKE_EXE_LINKER_FLAGS_DEBUG}")
set(CMAKE_SHARED_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE}")
set(CMAKE_SHARED_LINKER_FLAGS_RELEASEMINSIZE "${CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE}")
set(CMAKE_SHARED_LINKER_FLAGS_RELEASENOOPT "${CMAKE_EXE_LINKER_FLAGS_RELEASENOOPT}")

set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS}")
set(CMAKE_MODULE_LINKER_FLAGS_DEBUG "${CMAKE_EXE_LINKER_FLAGS_DEBUG}")
set(CMAKE_MODULE_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE}")
set(CMAKE_MODULE_LINKER_FLAGS_RELEASEMINSIZE "${CMAKE_EXE_LINKER_FLAGS_RELEASEMINSIZE}")
set(CMAKE_MODULE_LINKER_FLAGS_RELEASENOOPT "${CMAKE_EXE_LINKER_FLAGS_RELEASENOOPT}")

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
    message(STATUS "CMAKE_STATIC_LINKER_FLAGS:                  ${CMAKE_STATIC_LINKER_FLAGS}")
    message(STATUS "CMAKE_STATIC_LINKER_FLAGS_DEBUG:            ${CMAKE_STATIC_LINKER_FLAGS_DEBUG}")
    message(STATUS "CMAKE_STATIC_LINKER_FLAGS_RELEASE:          ${CMAKE_STATIC_LINKER_FLAGS_RELEASE}")
    message(STATUS "CMAKE_STATIC_LINKER_FLAGS_RELEASEMINSIZE:   ${CMAKE_STATIC_LINKER_FLAGS_RELEASEMINSIZE}")
    message(STATUS "CMAKE_STATIC_LINKER_FLAGS_RELEASENOOPT:     ${CMAKE_STATIC_LINKER_FLAGS_RELEASENOOPT}")
    message(STATUS "")
    message(STATUS "CMAKE_SHARED_LINKER_FLAGS:                  ${CMAKE_SHARED_LINKER_FLAGS}")
    message(STATUS "CMAKE_SHARED_LINKER_FLAGS_DEBUG:            ${CMAKE_SHARED_LINKER_FLAGS_DEBUG}")
    message(STATUS "CMAKE_SHARED_LINKER_FLAGS_RELEASE:          ${CMAKE_SHARED_LINKER_FLAGS_RELEASE}")
    message(STATUS "CMAKE_SHARED_LINKER_FLAGS_RELEASEMINSIZE:   ${CMAKE_SHARED_LINKER_FLAGS_RELEASEMINSIZE}")
    message(STATUS "CMAKE_SHARED_LINKER_FLAGS_RELEASENOOPT:     ${CMAKE_SHARED_LINKER_FLAGS_RELEASENOOPT}")
    message(STATUS "")
    message(STATUS "CMAKE_MODULE_LINKER_FLAGS:                  ${CMAKE_MODULE_LINKER_FLAGS}")
    message(STATUS "CMAKE_MODULE_LINKER_FLAGS_DEBUG:            ${CMAKE_MODULE_LINKER_FLAGS_DEBUG}")
    message(STATUS "CMAKE_MODULE_LINKER_FLAGS_RELEASE:          ${CMAKE_MODULE_LINKER_FLAGS_RELEASE}")
    message(STATUS "CMAKE_MODULE_LINKER_FLAGS_RELEASEMINSIZE:   ${CMAKE_MODULE_LINKER_FLAGS_RELEASEMINSIZE}")
    message(STATUS "CMAKE_MODULE_LINKER_FLAGS_RELEASENOOPT:     ${CMAKE_MODULE_LINKER_FLAGS_RELEASENOOPT}")
    message(STATUS "")
    message(STATUS "***** CMAKE_BUILD_TYPE: '${CMAKE_BUILD_TYPE}' *****")
    message(STATUS "")
endif()
