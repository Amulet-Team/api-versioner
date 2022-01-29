from typing import Callable, Awaitable

from package._private.api.chunk import Chunkv3

from .abstract import AbstractWorld
from .factory import factory


# AsyncIO API
# This is a possible future version of the API
@factory.register
class Worldv3(AbstractWorld):
    __version__ = 3

    ChunkVersion = Chunkv3

    get_chunk: Callable[[str, int, int], Awaitable[Chunkv3]]
