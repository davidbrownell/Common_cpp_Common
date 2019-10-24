# Template CMakeLists.txt file.
#
#   Replace the following when using this template:
#       - <project_name>
#       - <project_version_major>
#       - <project_version_minor>
#       - <project_version_patch>
#       - <project_files>
#       - <unit_test_file>
#       - <library_names>                   [optional]
#       - <company_name>                    [optional]
#

cmake_minimum_required(VERSION 3.5.0)

# If this template is being used as a module/.cmake file (rather than in CMakeLists.txt),
# do the following:
#
#   1) Change the `macro` below to a `function`
#   2) Instead of using the `_this_path` variable, uncomment the file-scoped var
#      and use that value instead.

# Uncomment the following line if this is a module:
#
# set(_<module_name>_this_path ${CMAKE_CURRENT_LIST_DIR} CACHE INTERNAL "")

macro(Impl)
    # Defining a function here to introduce a new scope for local variables
    set(_project_name <project_name>)
    set(_version_major <project_version_major>)         # '1' in the release 1.2.3-alpha1+201910161322
    set(_version_minor <project_version_minor>)         # '2' in the release 1.2.3-alpha1+201910161322
    set(_version_patch <project_version_patch>)         # '3' in the release 1.2.3-alpha1+201910161322
    set(_version_prerelease_info "")                    # Optional 'alpha1' in the release 1.2.3-alpha1+201910161322
    set(_version_build_info "")                         # Optional '201910161322' in the release 1.2.3-alpha1+201910161322

    set(_version ${_version_major}.${_version_minor}.${_version_patch})

    # Alpha version components (which are supported in SemVer) present problems
    # for cmake when the version is provided inline. However, things work as expected
    # when setting the version as a property.
    project(${_project_name} LANGUAGES CXX)
    set(PROJECT_VERSION ${_version})

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

    # include(GenerateFileAttributes)
    #
    # generate_file_attributes(
    #     _<project_name>_file_attribute_sources
    #     NAME ${_project_name}
    #     COMPANY_NAME <company_name>
    #     VERSION_MAJOR ${_version_major}
    #     VERSION_MINOR ${_version_minor}
    #     VERSION_PATCH ${_version_patch}
    #     VERSION_PRERELEASE_INFO ${_version_prerelease_info}
    #     VERSION_BUILD_INFO ${_version_build_info}
    # )

    # Do not use `_this_path` if this is a module.
    get_filename_component(_this_path ${CMAKE_CURRENT_LIST_FILE} DIRECTORY)

    add_executable(
        ${_project_name}
        <project_files>
        # _<project_name>_file_attribute_sources
    )

    set_target_properties(
        ${_project_name} PROPERTIES
        VERSION ${_version}
        SOVERSION ${_version_major}
    )

    target_include_directories(
        ${_project_name} PRIVATE
        ${_includes}
    )

    target_link_directories(
        ${_project_name} PRIVATE
        ${_libs}
    )

    # target_link_libraries(
    #     ${_project_name} PRIVATE
    #     <library_names>
    # )

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
        #     <library_names>
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
endmacro()

Impl()
