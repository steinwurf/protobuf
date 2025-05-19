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
endif ()

# Configure Protobuf options
set(protobuf_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(protobuf_BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(protobuf_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)

# Abseil dependency
if(NOT TARGET absl::base)
  add_subdirectory("${STEINWURF_RESOLVE}/abseil" abseil EXCLUDE_FROM_ALL)
endif()

# Build Protobuf
add_subdirectory(
    ${STEINWURF_RESOLVE}/protobuf-source
    ${CMAKE_CURRENT_BINARY_DIR}/protobuf-source
)

# Set PIE only for libprotobuf target
set_target_properties(libprotobuf PROPERTIES POSITION_INDEPENDENT_CODE ON)


if(${PROJECT_NAME} STREQUAL ${CMAKE_PROJECT_NAME})

  # Google Test dependency
  add_subdirectory("${STEINWURF_RESOLVE}/gtest-source")

  # Build test executable
  file(GLOB_RECURSE protobuf_test_sources ./test/*.cpp)

  # Add .cc files to the test sources
  file(GLOB_RECURSE protobuf_test_sources_cc ./test/*.cc)
  list(APPEND protobuf_test_sources ${protobuf_test_sources_cc})

  add_executable(protobuf_tests ${protobuf_test_sources})
  target_link_libraries(protobuf_tests gtest_main)
  target_link_libraries(protobuf_tests protobuf::libprotobuf)

  enable_testing()
  add_test(protobuf_tests protobuf_tests)

endif()


