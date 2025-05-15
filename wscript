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

    # Add flags before loading cmake to include in the CMake configure
    # command.
    #
    # The ABSL_PROPAGATE_CXX_STD flag is used to ensure that the C++ standard
    # used by the C++ standard is consistent with the one used by the
    # application.
    ctx.env.append_value("CMAKE_ARGS", "-DABSL_PROPAGATE_CXX_STD=ON")

    # Check if the user wants to build protoc
    if ctx.options.with_protoc:
        # Add flags to build protoc
        ctx.env.append_value("CMAKE_ARGS", "-Dprotobuf_BUILD_PROTOC_BINARIES=ON")
    else:
        # Add flags to not build protoc
        ctx.env.append_value("CMAKE_ARGS", "-Dprotobuf_BUILD_PROTOC_BINARIES=OFF")

    ctx.load("cmake")


def build(ctx):

    ctx.load("cmake")


def clean(ctx):

    ctx.load("cmake")

    # Set the default clean paths
    ctx.clean_paths = ["build", "build_current"]
