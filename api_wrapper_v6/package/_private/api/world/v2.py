from typing import Callable, Awaitable

from package._private.api.chunk import Chunkv1

from .abstract import AbstractWorld
from .factory import factory


# AsyncIO API
# This is a possible future version of the API
@factory.register
class Worldv2(AbstractWorld):
    __version__ = 2

    ChunkVersion = Chunkv1

    async def get_chunk(self, dimension: str, cx: int, cz: int):
        """
        Get a chunk from the world

        :param dimension: ...
        :param cx: ...
        :param cz: ...
        :return: The chunk object
        """
        return self.ChunkVersion(
            await self._core.get_chunk_core(
                dimension,
                cx,
                cz
            )
        )
    get_chunk: Callable[[str, int, int], Awaitable[Chunkv1]]
