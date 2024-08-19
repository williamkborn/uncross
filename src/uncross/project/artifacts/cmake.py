"""Create cmake C Example Project Structure"""

import os

from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def drop_root_cmakelists_txt(name: str, path: str) -> None:
    """Create C Source file"""

    root_cmakelists_txt_content = f"""
cmake_minimum_required(VERSION 3.13)

project({name} C)

add_subdirectory(src)

"""

    with open(path, "w", encoding="utf-8") as root_cmakelists_txt_file:
        root_cmakelists_txt_file.write(root_cmakelists_txt_content)


def drop_src_cmakelists_txt(name: str, path: str) -> None:
    """Create project header file"""

    src_cmakelists_txt_content = f"""
set(TARGET_NAME {name}_${{CMAKE_SYSTEM_NAME}}_${{CMAKE_SYSTEM_PROCESSOR}})

add_executable(${{TARGET_NAME}} main.c)
target_include_directories(${{TARGET_NAME}} PRIVATE ${{CMAKE_CURRENT_SOURCE_DIR}}/../include)

if (CMAKE_BUILD_TYPE STREQUAL "Debug")
  set_target_properties(
    ${{TARGET_NAME}}
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_SOURCE_DIR}}/debug/bin
  )
  target_compile_options(${{TARGET_NAME}} PRIVATE -O3 -g -Wall -Wextra -Wpedantic)
  if (${{CMAKE_SYSTEM_PROCESSOR}} STREQUAL "x86_64")
    target_compile_options(${{TARGET_NAME}} PRIVATE -fsanitize=address)
    target_link_options(${{TARGET_NAME}} PRIVATE -fsanitize=address)
  endif()
endif()

if (CMAKE_BUILD_TYPE STREQUAL "Release")
  set_target_properties(
    ${{TARGET_NAME}}
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_SOURCE_DIR}}/release/bin
  )
  target_compile_options(${{TARGET_NAME}} PRIVATE -O3 -Wall -Wextra -Wpedantic -s)
  target_link_options(${{TARGET_NAME}} PRIVATE -s)
endif()

"""

    with open(path, "w", encoding="utf-8") as src_cmakelists_txt_file:
        src_cmakelists_txt_file.write(src_cmakelists_txt_content)


def create_cmakelists_txt(name: str, root: str) -> None:
    """Create an example cmake C project dir structure"""
    LOGGER.debug("creating cmake C project structure at %s ...", root)
    os.makedirs(f"{root}/src", exist_ok=True)
    drop_root_cmakelists_txt(name, f"{root}/CMakeLists.txt")
    drop_src_cmakelists_txt(name, f"{root}/src/CMakeLists.txt")
