from typing import Union, Type

from package._private.abstract import AbstractAPIFactory

from .abstract import AbstractChunkAPI
from .v1 import ChunkAPIv1


ChunkAPIs = Union[ChunkAPIv1]
ChunkAPIsType = Union[Type[ChunkAPIv1]]


class ChunkApiFactory(AbstractAPIFactory):
    APIBase = AbstractChunkAPI


chunk_factory = ChunkApiFactory()
