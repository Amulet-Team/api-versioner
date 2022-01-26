import asyncio

from package.api.chunk import ChunkAPIv1, chunk_factory
from package._private.api.chunk import ChunkCore
from package._private.api.world import WorldCore

from .abstract import AbstractWorldAPI

# Blocking IO API
# This emulates the current behaviour
class WorldAPIv1(AbstractWorldAPI):
    def __init__(self, core: WorldCore):
        self.__core = core

    def get_chunk(self, cx: int, cz: int, dimension: str) -> ChunkAPIv1:
        api_cls = chunk_factory.get_api(ChunkAPIv1)
        chunk_core: ChunkCore = asyncio.run(self.__core.get_chunk(dimension, cx, cz))
        return api_cls(chunk_core)
