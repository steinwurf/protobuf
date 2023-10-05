#! /usr/bin/env python
# encoding: utf-8

import os
import shutil

APPNAME = "protobuf"
VERSION = "2.0.2"


def options(opt):
    opt.add_option(
        "--with_protoc",
        action="store_true",
        default=None,
        help="Add protoc to the build",
    )


def configure(conf):
    conf.set_cxx_std(14)
    if conf.is_mkspec_platform("linux") and not conf.env["LIB_PTHREAD"]:
        conf.check_cxx(lib="pthread")

    if conf.is_mkspec_platform("mac"):
        conf.env.append_value("LINKFLAGS", ["-framework", "CoreFoundation"])

    if not conf.has_tool_option("with_protoc"):
        conf.env.stored_options["with_protoc"] = False


def build(bld):
    # Following is a fix for the build of protobuf
    # to no print warnings its thousands of warnings
    compiler_binary = bld.env.get_flat("CXX").lower()
    cxxflags = []
    if "clang" in compiler_binary:
        cxxflags += ["-w"]
    elif "g++" in compiler_binary:
        cxxflags += ["-w"]
    elif "cl.exe" in compiler_binary:
        cxxflags += ["/W0"]

    _absl(bld, cxxflags)
    _utf8_range(bld, cxxflags)

    use_flags = ["absl", "utf8_range"]
    if bld.is_mkspec_platform("linux"):
        use_flags += ["PTHREAD"]

    # Path to the source repo
    protobuf_source = bld.dependency_node("protobuf-source")

    includes = [
        protobuf_source.find_dir("src/"),
    ]

    sources = protobuf_source.ant_glob(
        "src/google/protobuf/**/*.cc",
        excl=[
            "src/google/protobuf/compiler/**",
            "src/google/protobuf/testing/**",
            "src/google/protobuf/test_**",
            "src/google/protobuf/mock_**",
            "src/google/protobuf/benchmark_**",
            "src/google/protobuf/**/*_unittest.cc",
            "src/google/protobuf/**/*_test.cc",
            "src/google/protobuf/**/*_test_*.cc",
            "src/google/protobuf/**/*_tester.cc",
            "src/google/protobuf/lazy_field_heavy.cc",
        ],
    )

    bld.stlib(
        target="protobuf",
        source=sources,
        includes=includes,
        use=use_flags,
        export_includes=includes,
        cxxflags=cxxflags,
    )

    if bld.is_toplevel():
        bld.program(
            features="cxx test",
            source=bld.path.ant_glob("test/cpp/*.cc") + bld.path.ant_glob("test/cpp/*.cpp"),
            includes=["test/cpp/"],
            target="protobuf_tests",
            use=["protobuf", "gtest"],
        )

    if bld.get_tool_option("with_protoc"):
        _protoc(bld, cxxflags)


def _protoc(bld, cxxflags):
    # Path to the source repo
    protobuf_source = bld.dependency_node("protobuf-source")
    include_path = protobuf_source.find_dir("src/")

    sources = protobuf_source.ant_glob(
        "src/google/protobuf/compiler/**/*.cc",
        excl=[
            "src/google/protobuf/compiler/**/*_unittest.cc",
            "src/google/protobuf/compiler/**/mock_*.cc",
            "src/google/protobuf/compiler/**/unittest.cc",
            "src/google/protobuf/compiler/**/*_test_*.cc",
            "src/google/protobuf/compiler/**/*_test.cc",
            "src/google/protobuf/compiler/**/test_*.cc",
            "src/google/protobuf/compiler/**/*tester.cc",
            "src/google/protobuf/compiler/fake_plugin.cc",
        ],
    )

    bld.program(
        features=["cxx"],
        source=sources,
        includes=[include_path],
        target="protoc",
        use=["protobuf"],
        cxxflags=cxxflags,
    )


def _absl(bld, cxxflags):
    protobuf_source = bld.dependency_node("protobuf-source")

    includes = protobuf_source.ant_glob(
        "third_party/abseil-cpp/absl/*",
    )

    includes.append(protobuf_source.find_dir("third_party/abseil-cpp/"), )

    sources = protobuf_source.ant_glob(
        "third_party/abseil-cpp/absl/**/*.cc",
        excl=[
            "third_party/abseil-cpp/absl/**/*_test_*.cc",
            "third_party/abseil-cpp/absl/**/*_test.cc",
            "third_party/abseil-cpp/absl/**/test_*.cc",
            "third_party/abseil-cpp/absl/**/*testing*",
            "third_party/abseil-cpp/absl/**/*benchmark*",
            "third_party/abseil-cpp/absl/**/*mock*",
        ],
    )

    if bld.is_mkspec_platform("windows"):
        cxxflags += ["/DNOMINMAX"]

    bld.stlib(
        target="absl",
        source=sources,
        includes=includes,
        export_includes=includes,
        cxxflags=cxxflags,
    )


def _utf8_range(bld, cxxflags):
    protobuf_source = bld.dependency_node("protobuf-source")

    includes = [protobuf_source.find_dir("third_party/utf8_range")]

    sources = protobuf_source.ant_glob(
        "third_party/utf8_range/*.cc",
        "third_party/utf8_range/**/*.cc",
        excl=[
            "third_party/utf8_range/**/*test.cc",
        ]
    )

    bld.stlib(
        target="utf8_range",
        source=sources,
        includes=includes,
        export_includes=includes,
        cxxflags=cxxflags,
        use=["absl"],
    )


def protogen(ctx):
    # check if protec is available
    protoc_location = "build_current/protoc"
    if not os.path.isfile(protoc_location):
        ctx.fatal("protoc not found. Make sure to configure waf with `--with_protoc` to include protoc in build.")
        return
    try:
        shutil.rmtree("test/cpp")
    except:
        pass
    os.mkdir("test/cpp")

    ctx.exec_command(
        f"./{protoc_location} --cpp_out ./test/cpp --proto_path ./test test/*.proto"
    )

    ctx.exec_command(
        "echo 'DisableFormat: true\nSortIncludes: false' > ./test/cpp/.clang-format"
    )
