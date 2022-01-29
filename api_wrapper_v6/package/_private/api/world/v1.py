import asyncio

from package._private.api.chunk import Chunkv1

from .abstract import AbstractWorld
from .factory import factory


# Blocking IO API
# This emulates the current behaviour
@factory.register
class Worldv1(AbstractWorld):
    __version__ = 1

    def get_chunk(self, cx: int, cz: int, dimension: str) -> Chunkv1:
        return Chunkv1(
            asyncio.run(
                self._core.get_chunk_core(
                    dimension,
                    cx,
                    cz
                )
            )
        )
