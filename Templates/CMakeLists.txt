# Template CMakeLists.txt file.
#
#   Replace the following when using this template:
#       - <project_name>
#       - <project_version_major>, <project_version_minor>, <project_version_patch>
#       - <project_files>
#       - <unit_test_file>
#

cmake_minimum_required(VERSION 3.5.0)

set(_project_name <project_name>)
set(_${_project_name}_version_major <project_version_major>)
set(_${_project_name}_version_minor <project_version_minor>)
set(_${_project_name}_version_patch <project_version_patch>)
set(_${_project_name}_version ${_${_project_name}_version_major}.${_${_project_name}_version_minor}.${_${_project_name}_version_patch})

project(${_project_name} VERSION ${_${_project_name}_version} LANGUAGES CXX)

set(_includes "$ENV{INCLUDE}")
set(_libs "$ENV{LIB}")

if(NOT WIN32)
    string(REPLACE ":" ";" CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}")
    string(REPLACE ":" ";" _includes "${_includes}")
    string(REPLACE ":" ";" _libs "${_libs}")
endif()

set(CMAKE_MODULE_PATH "$ENV{DEVELOPMENT_ENVIRONMENT_CMAKE_MODULE_PATH}")
include(CppCommon)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# All paths should be relative to `${_this_path}`
get_filename_component(_this_path ${CMAKE_CURRENT_LIST_FILE} DIRECTORY)

add_executable(
    ${_project_name}
    <project_files>
)

set_target_properties(
    ${_project_name} PROPERTIES
    VERSION ${_${_project_name}_version}
    SOVERSION ${_${_project_name}_version_major}
)

enable_testing()

foreach(_test_name IN ITEMS
    <unit_test_file>_UnitTest
)
    add_executable(
        ${_test_name}
        ${_test_name}.cpp
    )

    # target_link_libraries(
    #     ${_test_name}
    #     <library_name>
    # )

    target_include_directories(
        ${_test_name} PRIVATE
        ${_includes}
    )

    target_link_directories(
        ${_test_name} PRIVATE
        ${_libs}
    )

    add_test(NAME ${_test_name} COMMAND ${_test_name} --success)
endforeach()
