# Quick Start

This guide is meant to show basic usage of `uncross` for a new project.

## Project Creation

To begin, create a project with the `uncross new` command:

```
uncross new project
```

This will create a new directory in the current working directory with the structure:

```
project
├── .git
│   └── <git files>
├── include
│   └── project.h
├── src
│   ├── CMakeLists.txt
│   └── main.c
├── .clang-format
├── .clang-tidy
├── .gitignore
├── CMakeLists.txt
├── Makefile
└── uncross.toml
```

This project structure has a very small C program that will compile to print "Hello, <project name>!" to stdout.

## Build Project

To build in debug mode:

```
uncross build
```

To build in release mode:

```
uncross build --release
```

To build both:

```
uncross build --all
```

After building, observe the following directory structure:

```
project
├── .git
│   └── <git files>
├── build
│   ├── Debug
│   │   └── <debug build files>
│   └── Release
│       └── <release build files>
├── debug
│   └── bin
│       └── project_Linux_x86_64
├── include
│   └── project.h
├── release
│   └── bin
│       └── project_Linux_x86_64
├── src
│   ├── CMakeLists.txt
│   └── main.c
├── .clang-format
├── .clang-tidy
├── .gitignore
├── CMakeLists.txt
├── Makefile
└── uncross.toml
```

The `debug` and `release` directories are a creation of `uncross`. The behavior of building the debug and release binaries in implemented in the default CMakeLists.txt, and must be reimplemented in existing projects if this behavior is desired.

## CodeChecker

`uncross` automates the creation of HTML reports with `CodeChecker` using a compilation database from CMake. To run the report and automatically open it in a browser, run:

```
uncross check --open
```

Running the above command without the `--open` flag will not open a browser window, and the files will be available under the `release` or `debug` directories. The `check` command takes the same flags as `build` to choose the build mode.

## Linting and Formatting

`uncross` enables checking for lint, and automatically formatting source files, via `clang-format`. `uncross lint` will check all .c and .h files in the project for lint, and `uncross fmt` will automatically format them. `uncross` will pass an argument to `clang-format` to have it use a `.clang-format` file in the project root.
