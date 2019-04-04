# Template CMakeLists.txt file.
#
#   Replace the following when using this template:
#       - <project_name>
#       - <project_version>
#       - <project_files>
#
#   [OPTIONAL]
#       - CMAKE_CXX_STANDARD is set to C++14
#

# TODO: This needs refinement

cmake_minimum_required(VERSION 3.5.0)

project(<project_name> VERSION <project_version>)

set(CMAKE_MODULE_PATH "$ENV{DEVELOPMENT_ENVIRONMENT_CMAKE_MODULE_PATH}")

if(NOT WIN32)
    string(REPLACE ":" ";" ${CMAKE_MODULE_PATH} ${CMAKE_MODULE_PATH})
endif()

include(CppCommon)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable( <project_name>
    <project_files>
)

enable_testing()

foreach(_test_name IN ITEMS
    <file>_UnitTest
)
    add_executable(${_name ${_name}.cpp)

    add_test(NAME ${_name} COMMAND ${_name} --success)
endforeach()
