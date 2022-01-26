import asyncio

from package._private.api.chunk.core import ChunkCore

from package._private.api.chunk import ChunkAPIv1, chunk_factory

from .core import WorldCore
from .abstract import AbstractWorldAPI


# Blocking IO API
# This emulates the current behaviour
class WorldAPIv1(AbstractWorldAPI):
    def __init__(self, core: WorldCore):
        self.__core = core

    def get_chunk(self, cx: int, cz: int, dimension: str) -> ChunkAPIv1:
        return asyncio.run(
            self.__core.get_chunk(
                ChunkAPIv1,
                dimension,
                cx,
                cz
            )
        )
