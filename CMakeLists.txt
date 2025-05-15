cmake_minimum_required(VERSION 3.12)
project(protobuf)

include_guard(GLOBAL)

find_package(Python COMPONENTS Interpreter)
include(FetchContent)

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
endif ()

# set(protobuf_BUILD_SHARED_LIBS OFF)
# set(protobuf_BUILD_TESTS OFF)


add_subdirectory(
    ${STEINWURF_RESOLVE}/protobuf-source
    ${CMAKE_CURRENT_BINARY_DIR}/protobuf-source 
    EXCLUDE_FROM_ALL
) 



# # Set PIE only for libprotobuf target
# set_target_properties(libprotobuf PROPERTIES POSITION_INDEPENDENT_CODE ON)
# target_compile_definitions(libprotobuf PUBLIC _LARGEFILE64_SOURCE)
# target_compile_features(libprotobuf PUBLIC cxx_std_17)

# Configure Protobuf options
# set(protobuf_BUILD_TESTS OFF CACHE BOOL "" FORCE)
# set(protobuf_BUILD_PROTOC_BINARIES ON CACHE BOOL "" FORCE)
# set(protobuf_BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
# set(protobuf_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)

# # FetchContent: protobuf
# FetchContent_Declare(
#     protobuf
#     SOURCE_DIR ${STEINWURF_RESOLVE}/protobuf-source
# )
# FetchContent_MakeAvailable(protobuf)

# #Now, add the path where protobuf installed itself
# list(APPEND CMAKE_PREFIX_PATH ${PROTOBUF_HOST_INSTALL_DIR})

# # Find the protobuf package
# find_package(protobuf REQUIRED)

# Make the steinwurf alias
add_library(nanoping::protobuf ALIAS libprotobuf)


# if(${PROJECT_NAME} STREQUAL ${CMAKE_PROJECT_NAME})

#   # Google Test dependency
#   add_subdirectory("${STEINWURF_RESOLVE}/gtest-source")

#   # Build test executable
#   file(GLOB_RECURSE protobuf_test_sources ./test/*.cpp)

#   # Add .cc files to the test sources
#   file(GLOB_RECURSE protobuf_test_sources_cc ./test/*.cc)
#   list(APPEND protobuf_test_sources ${protobuf_test_sources_cc})

#   add_executable(protobuf_tests ${protobuf_test_sources})
#   target_link_libraries(protobuf_tests gtest_main)
#   target_link_libraries(protobuf_tests steinwurf::protobuf)

#   add_test(protobuf_tests protobuf_tests)

# endif()


