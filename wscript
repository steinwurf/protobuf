#! /usr/bin/env python
# encoding: utf-8

import os
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
    protobuf_root = bld.dependency_node("protobuf-source")

    library_path = protobuf_root.find_dir("src/")
    include_path = protobuf_root.find_dir("src/")

    sources = library_path.ant_glob(
        "google/protobuf/**/*[!_lite][!_test]*.cc",
    )

    all_sources = library_path.ant_glob("google/protobuf/**/*.cc")
    sources = []

    for source in all_sources:
        if "test." in source.abspath():
            continue

        if "testing" in source.abspath():
            continue

        if "test_" in source.abspath():
            continue

        if "tester" in source.abspath():
            continue

        if "benchmark" in source.abspath():
            continue

        if "mock" in source.abspath():
            continue

        sources.append(source)

    bld.stlib(
        target="protobuf",
        source=sources,
        includes=[include_path],
        use=use_flags,
        export_includes=[include_path],
    )
