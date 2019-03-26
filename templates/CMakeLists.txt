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

# include(CTest)
# enable_testing()

# set(CPACK_PROJECT_NAME ${PROJECT_NAME})
# set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
# include(CPack)
