import asyncio

from package._private.api.chunk import Chunkv1

from .core import WorldCore
from .abstract import AbstractWorld


# Blocking IO API
# This emulates the current behaviour
class Worldv1(AbstractWorld):
    def __init__(self, core: WorldCore):
        super().__init__(core)
        self.__core = core

    def get_chunk(self, cx: int, cz: int, dimension: str) -> Chunkv1:
        return asyncio.run(
            self.__core.get_chunk(
                Chunkv1,
                dimension,
                cx,
                cz
            )
        )
