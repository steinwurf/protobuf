#! /usr/bin/env python
# encoding: utf-8

import os
import shutil
import waflib

APPNAME = "protobuf"
VERSION = "2.0.10"


def options(ctx):
    ctx.load("cmake")

    # Add option whether to build protoc
    ctx.add_option(
        "--with-protoc",
        action="store_true",
        default=False,
        help="Build protoc (default: %default)",
    )


def configure(ctx):

    ctx.load("cmake")

    # Check if the user wants to build protoc
    if ctx.options.with_protoc:
        # Add flags to build protoc
        ctx.env.CMAKE_CONFIGURE_ARGS += [
            "-Dprotobuf_BUILD_PROTOBUF_BINARIES=ON",
            "-Dprotobuf_BUILD_PROTOC_BINARIES=ON",
        ]
    else:
        # Add flags to not build protoc
        ctx.env.CMAKE_CONFIGURE_ARGS += [
            "-Dprotobuf_BUILD_PROTOBUF_BINARIES=OFF",
            "-Dprotobuf_BUILD_PROTOC_BINARIES=OFF",
        ]

    if ctx.is_toplevel():

        ctx.env.CMAKE_CONFIGURE_ARGS += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5"]

        ctx.cmake_configure()


def build(ctx):

    ctx.load("cmake")

    if ctx.is_toplevel():
        ctx.cmake_build()


def protogen(ctx):
    """Generate C++ code from .proto files using protoc."""

    ctx.load_environment()
    protoc = ctx.search_executable("**/protoc", path_list=[ctx.env.CMAKE_BUILD_DIR])

    ctx.run_exectuable(f"{protoc} --cpp_out=cpp src.proto", cwd="./test")
