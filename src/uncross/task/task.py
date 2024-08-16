"""A build task to complete"""

from collections.abc import Callable


class BuildTask:
    """A build task"""

    def __init__(self, name: str, work: Callable) -> None:
        if not isinstance(name, str):
            raise TypeError
        if not isinstance(work, Callable):
            raise TypeError
        self._name = name
        self.work = work

    @property
    def name(self) -> str:
        """Get name"""
        return self._name

    def run(self) -> None:
        """Invoke work"""
        self.work()
