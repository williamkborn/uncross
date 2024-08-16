"""Base pipeline class"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uncross.task.task import BuildTask


class BasePipeline:
    """Base pipeline class"""

    def __init__(self, name: str = "pipeline") -> None:
        self._name: str = name
        self.groups: dict[str, list[BuildTask]] = {}
        self.groups["base"] = []

    @property
    def name(self) -> str:
        """Get name"""
        return self._name

    def add_group(self, name: str, tasks: list[BuildTask]) -> None:
        """Register a build group"""
        if name in self.groups:
            raise RuntimeError
        self.groups[name] = tasks

    def add_task(self, task: BuildTask) -> None:
        """Add a base task"""
        self.groups["base"].append(task)

    def run(self) -> None:
        """Run the pipeline"""
        raise NotImplementedError
