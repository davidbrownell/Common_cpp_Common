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


set(_cmake_paths "$ENV{DEVELOPMENT_ENVIRONMENT_CMAKE_MODULE_PATH}")

if(NOT WIN32)
    string(REPLACE ":" ";" ${_cmake_paths} ${_cmake_paths})
endif()

list(GET _cmake_paths 0 _last_cmake_path)

include("${_last_cmake_path}/cpp_common.cmake")

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
