cmake_minimum_required(VERSION 3.5.0)

# If this is being invoked within a .cmake file (rather than in CMakeLists.txt),
# change this `macro` to a `function`.
function(Impl)
    # Defining a function here to introduce a new scope for local variables
    set(_project_name Shared)
    set(_${_project_name}_version_major 1)
    set(_${_project_name}_version_minor 2)
    set(_${_project_name}_version_patch 3)
    set(_${_project_name}_version ${_${_project_name}_version_major}.${_${_project_name}_version_minor}.${_${_project_name}_version_patch})

    # Alpha version components (which are supported in SemVer) present problems
    # for cmake when the version is provided inline. However, things work as expected
    # when setting the version as a property.
    project(${_project_name} LANGUAGES CXX)
    set(PROJECT_VERSION ${_${_project_name}_version})

    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    set(CMAKE_CXX_EXTENSIONS OFF)

    set(_includes "$ENV{INCLUDE}")
    set(_libs "$ENV{LIB}")
    set(CMAKE_MODULE_PATH "$ENV{DEVELOPMENT_ENVIRONMENT_CMAKE_MODULE_PATH}")

    if(NOT WIN32)
        string(REPLACE ":" ";" CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}")
        string(REPLACE ":" ";" _includes "${_includes}")
        string(REPLACE ":" ";" _libs "${_libs}")
    endif()

    include(CppCommon)

    # All paths should be relative to `${_this_path}`.
    get_filename_component(_this_path ${CMAKE_CURRENT_LIST_FILE} DIRECTORY)

    include(${_this_path}/../lib/lib.cmake)

    add_library(
        ${_project_name}
        SHARED
        ${_this_path}/shared.cpp
        ${_this_path}/shared.h
    )

    set_target_properties(
        ${_project_name} PROPERTIES
        VERSION ${_${_project_name}_version}
        SOVERSION ${_${_project_name}_version_major}
    )

    target_link_libraries(
        ${_project_name}
        Lib
    )

    target_include_directories(
        ${_project_name}
        INTERFACE
        ${_this_path}
    )
endfunction()

Impl()
