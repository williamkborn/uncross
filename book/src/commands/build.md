# `uncross build`

The build command invokes CMake for each provided preset and toolchain.

With no options, the build command will invoke the system toolchain. If `uncross.toml` is present, it will build for each toolchain listed in `uncross.toml`.

For options, run `uncross build --help`.
