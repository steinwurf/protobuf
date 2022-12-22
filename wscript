#! /usr/bin/env python
# encoding: utf-8

import os
from waflib.extras.wurf.directory import remove_directory

APPNAME = "protobuf"
VERSION = "3.20.2"


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

    abseil_root = protobuf_root.find_dir("third_party/abseil-cpp")

    abseil_all_sources = abseil_root.ant_glob("absl/**/*.cc")
    abseil_sources = []

    for source in abseil_all_sources:
        if "test" in os.path.basename(source.abspath()):
            continue

        if "benchmark" in os.path.basename(source.abspath()):
            continue

        abseil_sources.append(source)

    bld.stlib(
        target="abseil",
        source=abseil_sources,
        includes=[
            abseil_root.find_dir("absl"),
        ],
        use=use_flags,
        export_includes=[
            abseil_root.find_dir("absl"),
        ],
    )

    library_path = protobuf_root.find_dir("src/")
    include_path = protobuf_root.find_dir("src/")

    sources = library_path.ant_glob(
        "google/protobuf/**/*[!_lite][!_test]*.cc",
    )

    all_sources = library_path.ant_glob("google/protobuf/**/*.cc")
    sources = []

    for source in all_sources:
        if "test" in os.path.basename(source.abspath()):
            continue

        if "benchmark" in os.path.basename(source.abspath()):
            continue

        if "mock" in os.path.basename(source.abspath()):
            continue

        sources.append(source)

    bld.stlib(
        target="protobuf",
        source=sources,
        includes=[include_path],
        use=use_flags + ["abseil"],
        export_includes=[library_path.find_dir("google")],
    )
