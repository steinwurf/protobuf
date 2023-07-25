#! /usr/bin/env python
# encoding: utf-8

APPNAME = "protobuf"
VERSION = "1.0.1"

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
    if not conf.has_tool_option("with_protoc"):
        conf.env.stored_options["with_protoc"] = False


def build(bld):
    use_flags = []
    if bld.is_mkspec_platform("linux"):
        use_flags += ["PTHREAD"]

    # Path to the source repo
    protobuf_source = bld.dependency_node("protobuf-source")

    include_path = protobuf_source.find_dir("src/")

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
        ],
    )

    # Following is a fix for the build of protobuf
    # to no print warnings its thousands of warnings
    compiler_binary = bld.env.get_flat("CXX").lower()
    cxxflags = ""
    if "clang" in compiler_binary:
        cxxflags += "-w"
    elif "g++" in compiler_binary:
        cxxflags += "-w"
    elif "cl.exe" in compiler_binary:
        cxxflags += "/W0"


    bld.stlib(
        target="protobuf",
        source=sources,
        includes=[include_path],
        use=use_flags,
        export_includes=[include_path],
        cxxflags=cxxflags,
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
