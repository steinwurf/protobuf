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

    # abseil_root = protobuf_root.find_dir("third_party/abseil-cpp")

    # sources = abseil_root.ant_glob("absl/**/*[!_benchmark][!_test]*.cc")
    # sources_to_include = []
    # for source in sources:
    #     if "test" in os.path.basename(source.abspath()):
    #         continue

    #     if "benchmark" in os.path.basename(source.abspath()):
    #         continue

    #     sources_to_include.append(source)

    # for source in sources_to_include:
    #     print(os.path.basename(source.abspath()))

    # bld.stlib(
    #     target="abseil",
    #     source=sources_to_include,
    #     use=use_flags,
    #     export_includes=[abseil_root.find_dir("absl")],
    # )

    # print(protobuf_root.abspath())

    library_path = protobuf_root.find_dir("src/")

    sources = library_path.ant_glob(
        "google/protobuf/**/*[!_lite][!_test]*.cc",
    )

    sources_to_include = []
    for source in sources:
        if "test" in os.path.basename(source.abspath()):
            continue

        if "benchmark" in os.path.basename(source.abspath()):
            continue

        sources_to_include.append(source)

    includes = library_path.ant_glob(
        "google/protobuf/**/*[!_lite][!_test]*.h",
    )

    includes_to_include = []
    for include in includes:
        if "test" in os.path.basename(include.abspath()):
            continue

        if "benchmark" in os.path.basename(include.abspath()):
            continue

        includes_to_include.append(include)

    bld.stlib(
        target="protobuf",
        source=sources_to_include,
        includes=includes_to_include,
        use=use_flags,
        export_includes=[library_path.find_dir("google")],
    )
