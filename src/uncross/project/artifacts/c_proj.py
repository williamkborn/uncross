"""Create C Example Project Structure"""

import os

from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def drop_c_source_file(name: str, path: str) -> None:
    """Create C Source file"""

    source_content = f"""
#include <stdio.h>

#include "{name.lower()}.h"

int main(void)
{{
    DPRINTF("Project %s, debug mode\\n", "{name}");
    puts("Hello, {name}!");
    return 0;
}}

"""

    with open(path, "w", encoding="utf-8") as source_file:
        source_file.write(source_content)


def drop_c_header(name: str, path: str) -> None:
    """Create project header file"""

    header_guard = f"{name.upper()}_H_"
    header_content = f"""
#ifndef {header_guard}
#define {header_guard}

#include <stdio.h>

#ifndef NDEBUG
#define DPRINTF(fmt, ...) \
        do \
        {{ \
                printf("[DEBUG] "fmt, __VA_ARGS__); \
        }} while (0)
#define DEPUTS(str) DPRINTF("%s", str)
#else

#define DPRINTF(fmt, ...) do {{}} while(0)
#define DPUTS(str) do {{}} while(0)

#endif /* NDEBUG */

#endif  /* {header_guard} */

"""

    with open(path, "w", encoding="utf-8") as header_file:
        header_file.write(header_content)


def create_c_project(name: str, root: str) -> None:
    """Create an example C project dir structure"""
    LOGGER.debug("creating C project structure at %s ...", root)
    os.makedirs(f"{root}/src", exist_ok=True)
    os.makedirs(f"{root}/include", exist_ok=True)
    drop_c_header(name, f"{root}/include/{name.lower()}.h")
    drop_c_source_file(name, f"{root}/src/main.c")
