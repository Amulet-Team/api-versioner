from package._private.api.chunk import ChunkCore, chunk_factory, ChunkAPIs, ChunkAPIsType
from .core import WorldCore

from .abstract import AbstractWorldAPI


# AsyncIO API
# This is a possible future version of the API
class WorldAPIv2(AbstractWorldAPI):
    def __init__(self, core: WorldCore):
        self.__core = core

    async def get_chunk(self, chunk_api: ChunkAPIsType, dimension: str, cx: int, cz: int) -> ChunkAPIs:
        """
        Get a chunk from the world

        :param chunk_api: The API to expose the chunk data
        :param dimension: ...
        :param cx: ...
        :param cz: ...
        :return: The chunk in the requested API
        """
        return await self.__core.get_chunk(
            chunk_api,
            dimension,
            cx,
            cz
        )
