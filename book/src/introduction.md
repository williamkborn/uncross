# Introduction

## What is uncross?

`uncross` is a meta build system for C/C++ cmake projects implemented as a python3 command-line interface. The aim is to automate and simplify cross compilation for cmake projects. Currently, it most readily supports Linux cross compilation from an x86_64 host system.

`uncross` is highly opinionated, supporting a small suite of C and C++ tools that the author has used across several projects.

The core intent is rapid prototyping and rapid delivery of small embedded systems projects. The use case for the author is compiling small test targets for cybersecurity research on embedded Linux networking appliances and IoT devices.

## Why uncross?

A project that uses uncross should largely look like any CMake project. Currently, the only intended deviation at the source level is a configuration file, `uncross.toml`, at the root of a project. In the future, and source level plugin and caching directory will be supported. In most circumstances, `uncross` should be drop-in compatible with existing projects that use CMake. `uncross` is not intended to adopt a large amount of logic for sake of compatibility with every edge-case use of CMake. However, failure to build an existing CMake project is considered a bug when the unsupported behavior is a reasonable "base case" feature of CMake.

Connecting various toolchains to a build system is a core task for embedded systems programing. CMake is a popular build system for defining builds in a portable manner. While CMake itself solves a large majority of problems in this space, it is still common to observe numerous utility scripts and scaffolding in large embedded projects. Each team will solve the same task in many different ways. These scripts take developer time and energy to implement and maintain.

`uncross` is a collection of a few select tools to accomplish the tasks of static analysis, cross compilation, and linting/formatting. These repositories should only need to include source files and build system files to instruct CMake on how to build the project. All other tasks should be completed by the meta build system. Improvements to the meta system should apply to all projects in this format, removing the need to maintain a collection of build, analysis, test, and packaging scripts.

New members of the team should not have to memorize large CMake commands or parse a collection of scripts and Makefiles. These tasks should be automated in a sane, memorable set of commands.

There are a variety of projects that provide toolchains for cross compiling Linux binaries from an x86_64 host to a variety of target architectures. `toolchains.bootlin.com` was selected as an initial toolchain source, with others to follow. Downloading and connecting these toolchains to the project build system should be an easy task, provided by the meta build system.

## What isn't uncross?

`uncross` does not aim to be a generic build system for all C/C++ projects. It does not support the larger body of C/C++ build systems (meson, bazel, msbuild, autotools, etc). It does not solve the problem of ensuring portability to all possible FOSS targets. It is narrowly tailored to an opinionated layout and employment of a select suite of widely used tooling as the default.

`uncross` is also not a build system on its own. CMake provides all of the heavy lifting. `uncross` automates and simplifies the rapid employment of CMake.

The long term plan is to enable extensions/plugins to enable support for a more diverse set of tools.

## What is this book?

This documentation is intended to introduce a seasoned C and CMake developer to the options and basic usage of `uncross`. By design,  CMake does a majority of the lifting. For an intoduction to CMake, we recommend [Professional CMake: A Practical Guide - 19th Edition](https://crascit.com/professional-cmake/).


## Contributing

We welcome source contributions and pull requests. 

We do ask that any feature work is supported by a firm justification of how the addition will apply to a larger body of projects and use cases. We are happy to look at your C/C++ project source if you are willing to share it to support these additions.

Bug fixes are greatly appreciated and will always be rapidly reviewed and merged as time allows.

This book and the website at uncross.dev are part of the project git repository. Any feature work will be expected to update corresponding documentation prior to merge.
