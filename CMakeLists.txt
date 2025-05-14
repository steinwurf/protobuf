cmake_minimum_required(VERSION 3.12)
project(protobuf)

include_guard(GLOBAL)

find_package(Python COMPONENTS Interpreter)

# Use waf to resolve dependencies
if (NOT DEFINED STEINWURF_RESOLVE)
    message(STATUS "Resolving dependencies...")
    execute_process(
            COMMAND ${Python_EXECUTABLE} waf resolve ${STEINWURF_RESOLVE_OPTIONS}
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
            RESULT_VARIABLE STATUS)
    if (STATUS AND NOT STATUS EQUAL 0)
        message(FATAL_ERROR "Failed: ${STATUS}")
    endif ()
    set(STEINWURF_RESOLVE "${CMAKE_CURRENT_SOURCE_DIR}/resolve_symlinks")
    set(STEINWURF_TOP_NAME ${PROJECT_NAME})
endif ()

set(protobuf_BUILD_SHARED_LIBS OFF)
set(protobuf_BUILD_TESTS OFF)

add_subdirectory(${STEINWURF_RESOLVE}/protobuf-source)

# Set PIE only for libprotobuf target
set_target_properties(libprotobuf PROPERTIES POSITION_INDEPENDENT_CODE ON)
target_compile_definitions(libprotobuf PUBLIC _LARGEFILE64_SOURCE)
target_compile_features(libprotobuf PUBLIC cxx_std_17)


# Make the steinwurf alias
add_library(steinwurf::protobuf ALIAS libprotobuf)