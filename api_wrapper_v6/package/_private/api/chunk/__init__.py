from typing import Union, Type

from .core import ChunkCore
from .abstract import AbstractChunk
from .factory import factory
from .v1 import Chunkv1
from .v3 import Chunkv3

factory.lock()

ChunkAPIs = Union[Chunkv1]
ChunkAPIsType = Union[Type[Chunkv1]]

