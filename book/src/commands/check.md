# `uncross check`

The check command invokes CodeChecker for each provided preset and toolchain.

NOTE: The project must first be build. Under the hood, CodeChecker is given a path to `compile_commands.json`, which is provided by the CMake configure step.

With no options, the check command will invoke the system toolchain. If `uncross.toml` is present, it will check each toolchain listed in `uncross.toml`.

For options, run `uncross check --help`.
