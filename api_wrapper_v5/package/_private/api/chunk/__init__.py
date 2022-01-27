from typing import Union, Type

from package._private.abstract import AbstractAPIValidator

from .core import ChunkCore
from .abstract import AbstractChunk
from .v1 import Chunkv1


ChunkAPIs = Union[Chunkv1]
ChunkAPIsType = Union[Type[Chunkv1]]


class ChunkApiValidator(AbstractAPIValidator):
    APIBase = AbstractChunk


chunk_api_validator = ChunkApiValidator()
