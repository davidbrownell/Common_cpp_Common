# Template CMakeLists.txt file.
#
#   Replace the following when using this template:
#       - <project_name>
#       - <project_version>
#       - <project_files>
#

cmake_minimum_required(VERSION 3.5.0)

project(<project_name> VERSION <project_version> LANGUAGES CXX)

set(CMAKE_MODULE_PATH "$ENV{DEVELOPMENT_ENVIRONMENT_CMAKE_MODULE_PATH}")
set(_includes "$ENV{INCLUDE}")
set(_libs "$ENV{LIB}")

if(NOT WIN32)
    string(REPLACE ":" ";" CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}")
    string(REPLACE ":" ";" _includes "${_includes}")
    string(REPLACE ":" ";" _libs "${_libs}")
endif()

include(CppCommon)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable( <project_name>
    <project_files>
)

enable_testing()

foreach(_test_name IN ITEMS
    <file>_UnitTest
)
    add_executable(${_test_name} ${_test_name}.cpp)

    target_include_directories(${_test_name} PRIVATE ${_includes})
    target_link_directories(${_test_name} PRIVATE ${_libs})

    add_test(NAME ${_test_name} COMMAND ${_test_name} --success)
endforeach()
