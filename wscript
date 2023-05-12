#! /usr/bin/env python
# encoding: utf-8

import os
import pathlib

from waflib.extras.wurf.directory import remove_directory

APPNAME = "protobuf"
VERSION = "v21.12"


def configure(conf):
    if conf.is_mkspec_platform("linux") and not conf.env["LIB_PTHREAD"]:
        conf.check_cxx(lib="pthread")


def build(bld):
    use_flags = []
    if bld.is_mkspec_platform("linux"):
        use_flags += ["PTHREAD"]

    bld.env.append_unique(
        "DEFINES_STEINWURF_VERSION", 'STEINWURF_PROTOBUF_VERSION="{}"'.format(VERSION)
    )

    # Path to the source repo
    protobuf_source = bld.dependency_node("protobuf-source")

    include_path = protobuf_source.find_dir("src/")

    sources = protobuf_source.ant_glob(
        "src/google/protobuf/**/*.cc", excl=["src/google/protobuf/compiler/**",
                                             "src/google/protobuf/testing/**",
                                             "src/google/protobuf/test_**",
                                             "src/google/protobuf/mock_**",
                                             "src/google/protobuf/benchmark_**",
                                             "src/google/protobuf/**/*_unittest.cc",
                                             "src/google/protobuf/**/*_test.cc",
                                             "src/google/protobuf/**/*_test_*.cc",
                                             "src/google/protobuf/**/*_tester.cc",
                                             ])

    bld.stlib(
        target="protobuf",
        source=sources,
        includes=[include_path],
        use=use_flags,
        export_includes=[include_path],
    )
