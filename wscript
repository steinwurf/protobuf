#! /usr/bin/env python
# encoding: utf-8

import os
import shutil
import waflib

APPNAME = "protobuf"
VERSION = "2.0.10"


def options(opt):

    if not opt.is_toplevel():
        return

    opt.add_option(
        "--cmake-build-type",
        default="Release",
        help="CMake build type (Release, Debug, RelWithDebInfo, etc.)",
    )
    opt.add_option("--cmake-toolchain", default="", help="Path to CMake toolchain file")

    opt.add_option(
        "--cmake-verbose",
        action="store_true",
        default=False,
        help="Enable verbose output for CMake configure and build",
    )


def configure(cfg):

    if not cfg.is_toplevel():
        return

    cfg.env.BUILD_DIR = cfg.path.get_bld().abspath()

    cmake_cmd = [
        "cmake",
        "-S",
        cfg.path.abspath(),
        "-B",
        cfg.env.BUILD_DIR,
        f"-DCMAKE_BUILD_TYPE={cfg.options.cmake_build_type}",
    ]

    if cfg.options.cmake_toolchain:
        cmake_cmd.append(f"-DCMAKE_TOOLCHAIN_FILE={cfg.options.cmake_toolchain}")

    if cfg.options.cmake_verbose:
        cmake_cmd.append("-DCMAKE_VERBOSE_MAKEFILE=ON")

    ret = cfg.exec_command(cmake_cmd, stdout=None, stderr=None)
    if ret != 0:
        cfg.fatal(f"CMake configuration {cmake_cmd} failed with exit code {ret}")


def build(bld):

    if not bld.is_toplevel():
        return

    jobs = str(bld.options.jobs) if hasattr(bld.options, "jobs") else "1"
    cmake_build_cmd = [
        "cmake",
        "--build",
        bld.env.BUILD_DIR,
        "--parallel",
        jobs,
    ]

    if bld.options.cmake_verbose:
        cmake_build_cmd.append("--verbose")

    ret = bld.exec_command(cmake_build_cmd, stdout=None, stderr=None)
    if ret != 0:
        bld.fatal(f"CMake build failed with exit code {ret}")


class Clean(waflib.Context.Context):
    cmd = "clean"
    fun = "clean"


def clean(ctx):
    ctx.logger = waflib.Logs.make_logger("/tmp/waf_clean.log", "cfg")

    build_dir = os.path.join(ctx.path.abspath(), "build")
    build_symlink = os.path.join(ctx.path.abspath(), "build_current")

    # Remove the "build" folder if it exists, with start and end messages
    ctx.start_msg("\nChecking and removing build directory")
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)
        ctx.end_msg("Removed")
    else:
        ctx.end_msg("Not found", color="YELLOW")

    # Remove the "build_current" symlink if it exists, with start and end messages
    ctx.start_msg("Checking and removing build_current symlink")
    if os.path.islink(build_symlink):
        os.unlink(build_symlink)
        ctx.end_msg("Removed")
    else:
        ctx.end_msg("Not found", color="YELLOW")
