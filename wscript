#! /usr/bin/env python
# encoding: utf-8

APPNAME = "protobuf"
VERSION = "1.0.1"


def configure(conf):
    conf.set_cxx_std(14)
    if conf.is_mkspec_platform("linux") and not conf.env["LIB_PTHREAD"]:
        conf.check_cxx(lib="pthread")


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

    bld.stlib(
        target="protobuf",
        source=sources,
        includes=[include_path],
        use=use_flags,
        export_includes=[include_path],
    )
