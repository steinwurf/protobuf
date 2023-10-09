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

# Abseil
file(GLOB_RECURSE sw_protobuf_abseil_sources ${STEINWURF_RESOLVE}/protobuf-source/third_party/abseil-cpp/absl/**/*.cc)
list(FILTER sw_protobuf_abseil_sources EXCLUDE REGEX .*absl\/.*\/.*_benchmark.*)
list(FILTER sw_protobuf_abseil_sources EXCLUDE REGEX .*absl\/.*\/.*benchmark.*)
list(FILTER sw_protobuf_abseil_sources EXCLUDE REGEX .*absl\/.*\/.*test_.*)
list(FILTER sw_protobuf_abseil_sources EXCLUDE REGEX .*absl\/.*\/.*_test.*)
list(FILTER sw_protobuf_abseil_sources EXCLUDE REGEX .*absl\/.*\/.*mock_.*)
list(FILTER sw_protobuf_abseil_sources EXCLUDE REGEX .*absl\/.*\/.*_mock_.*)

add_library(sw_protobuf_abseil STATIC ${sw_protobuf_abseil_sources})
target_compile_features(sw_protobuf_abseil PUBLIC cxx_std_17)
target_include_directories(sw_protobuf_abseil PUBLIC ${STEINWURF_RESOLVE}/protobuf-source/third_party/abseil-cpp)

if (APPLE)
    target_link_libraries(sw_protobuf_abseil "-framework CoreFoundation")
endif ()

# utf8_range
file(GLOB_RECURSE sw_protobuf_utf8_range_sources
        ${STEINWURF_RESOLVE}/protobuf-source/third_party/utf8_range/*.cc
        ${STEINWURF_RESOLVE}/protobuf-source/third_party/utf8_range/**/*.cc)
list(FILTER sw_protobuf_utf8_range_sources EXCLUDE REGEX .*test\.cc)

add_library(sw_protobuf_utf8_range STATIC ${sw_protobuf_utf8_range_sources})
target_compile_features(sw_protobuf_utf8_range PUBLIC cxx_std_17)
target_link_libraries(sw_protobuf_utf8_range PRIVATE sw_protobuf_abseil)
target_include_directories(sw_protobuf_utf8_range PUBLIC ${STEINWURF_RESOLVE}/protobuf-source/third_party/utf8_range)

if (DEFINED MSVC)
    target_compile_options(sw_protobuf_abseil PRIVATE "/DNOMINMAX")
endif ()

file(GLOB_RECURSE sw_protobuf_sources ${STEINWURF_RESOLVE}/protobuf-source/src/google/**/*.cc)
list(FILTER sw_protobuf_sources EXCLUDE REGEX .*src/google/protobuf\/compiler\/.*)
list(FILTER sw_protobuf_sources EXCLUDE REGEX .*src/google/protobuf\/.*test.*)

add_library(sw_protobuf STATIC ${sw_protobuf_sources})
target_compile_features(sw_protobuf PUBLIC cxx_std_17)
target_link_libraries(sw_protobuf PUBLIC sw_protobuf_abseil sw_protobuf_utf8_range)
target_include_directories(sw_protobuf PUBLIC ${STEINWURF_RESOLVE}/protobuf-source/src)

# Ignore -Wattribute warnings for GCC and Clang
if (CMAKE_C_COMPILER_ID STREQUAL "GNU" OR CMAKE_C_COMPILER_ID STREQUAL "Clang")
    target_compile_options(sw_protobuf PRIVATE -Wno-attributes)
endif ()

add_library(steinwurf::protobuf ALIAS sw_protobuf)

# Is top level project?
if (${CMAKE_PROJECT_NAME} STREQUAL ${PROJECT_NAME})
    enable_testing()

    if (CMAKE_C_COMPILER_ID MATCHES "MSVC")
        # For Windows: Prevent overriding the parent project's compiler/linker
        # settings
        set(gtest_force_shared_crt
                ON
                CACHE BOOL "" FORCE)
    endif ()

    # Google Test dependency
    add_subdirectory("${STEINWURF_RESOLVE}/gtest-source")

    file(GLOB_RECURSE sw_protobuf_test_sources ./test/cpp/*.cc ./test/cpp/*.cpp)
    add_executable(sw_protobuf_test ${sw_protobuf_test_sources})
    target_include_directories(sw_protobuf_test PRIVATE ${STEINWURF_RESOLVE}/test/cpp)
    target_link_libraries(sw_protobuf_test PUBLIC gtest_main sw_protobuf)

    add_test(sw_protobuf_test sw_protobuf_test)
endif ()
