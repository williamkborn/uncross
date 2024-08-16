"""Pipeline that runs all tasks in series."""

from uncross.task.base_pipeline import BasePipeline
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


class SeriesPipeline(BasePipeline):
    """Pipeline that runs all tasks in series."""

    def run(self) -> None:
        """do the thing."""

        if "base" not in self.groups:
            raise RuntimeError

        if len(self.groups["base"]) != 0:
            for task in self.groups["base"]:
                LOGGER.info("running base task %s ...", task.name)
                task.run()

        for name, group in self.groups.items():
            if name == "base":
                continue
            for task in group:
                LOGGER.info("running group %s task %s ...", name, task.name)
                task.run()

        LOGGER.info("all tasks done")
