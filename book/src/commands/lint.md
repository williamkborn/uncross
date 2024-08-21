# `uncross lint`

The lint command invokes `clang-format --dry-run` on every .c and .h file in the project. This is intended to be used in CI or as a sanity check.

This feature will not work as expected without a `.clang-format` file committed into the root of the project.

If the project directory is a git repository, this will run on every file/path that ends in .c or .h that is *staged or committed*. It will not run on new files that are not yet staged for commit.

If the project directory is a git repository, a behavior similar to `find . -name "*.c" -exec ...` will occur. This can be undesirable if directories under the project root contain temporary or external .c and .h files. For this reason, `build`, `debug`, and `release` are ignored.

For options, run `uncross lint --help`.
