News for protobuf waf build script
==================================

This file lists the major changes between versions. For a more detailed list of
every change, see the Git log.

Latest
------
* Patch: Fixed wrong includes for abseil in waf.

2.0.6
-----
* Patch: Ignore -Wattribute warnings for GCC and Clang.

2.0.5
-----
* Patch: Cleaned CMake remove unneeded CXX_EXTENSIONS flags and a debug message.

2.0.4
-----
* Patch: Force CMake targets to use c++ std 14.

2.0.3
-----
* Patch: Fixed some issues and added test for building of actually generated protobuf files.

2.0.2
-----
* Patch: Custom cmake to prevent target name collisions.

2.0.1
-----
* Patch: Fix problems with CMake and Waf on Windows and Mac OS.

2.0.0
-----
* Major: Upgraded to protobuf 24.3.

1.1.0
-----
* Patch: Suppress warnings when building protoc and protobuf.
* Minor: Added option for building protoc with `--with_protoc`.

1.0.1
-----
* Patch: Added global include guard.

1.0.0
-----
* Major: Initial release.
