# `uncross clean`

The clean command removes the `./build`, `./debug`, `./release`, and `release.tar.gz` by default. When the project directory is a git repository, this will always occur at the project root, regardless of the current working directory (as long as the current working directory is under the project root). When the project directory is not a git repository, this occurs in the working directory.

For options, run `uncross clean --help`.
