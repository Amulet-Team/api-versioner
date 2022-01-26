from typing import Union, Type

from package._private.abstract import AbstractAPIValidator

from .core import ChunkCore
from .abstract import AbstractChunkAPI
from .v1 import ChunkAPIv1


ChunkAPIs = Union[ChunkAPIv1]
ChunkAPIsType = Union[Type[ChunkAPIv1]]


class ChunkApiValidator(AbstractAPIValidator):
    APIBase = AbstractChunkAPI


chunk_factory = ChunkApiValidator()
