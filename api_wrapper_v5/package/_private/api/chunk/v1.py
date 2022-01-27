from package._private.api.chunk.core import ChunkCore

from .abstract import AbstractChunk


class Chunkv1(AbstractChunk):
    def __init__(self, core: ChunkCore):
        super().__init__(core)
        self.__core = core

    @property
    def cx(self) -> int:
        return self.__core.cx

    @property
    def cz(self) -> int:
        return self.__core.cz
