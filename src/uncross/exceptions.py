"""Uncross exceptions"""


class FailedSubTaskError(Exception):
    """Raise if a subtask/subprocess fails"""


class ProgramMissingError(Exception):
    """Raise if a missing program"""

    def __init__(self, program: str) -> None:
        super().__init__(f"missing program: {program}")


class ToolchainMissingError(Exception):
    """Raise if a missing program"""

    def __init__(self, toolchain: str) -> None:
        super().__init__(f"missing toolchain: {toolchain}")
