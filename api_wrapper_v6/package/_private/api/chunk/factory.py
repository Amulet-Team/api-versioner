from __future__ import annotations
from typing import Callable, Type

from package._private.abstract import AbstractAPIFactory

from .abstract import AbstractChunk
from .core import ChunkCore


class ChunkApiFactory(AbstractAPIFactory):
    APIBase = AbstractChunk
    Core = ChunkCore

    register: Callable[[Type[AbstractChunk]], Type[AbstractChunk]]
    get_api: Callable[[int, ChunkCore], AbstractChunk]


factory = ChunkApiFactory()
