from .core import ChunkCore
from .abstract import AbstractChunk
from .factory import factory


@factory.register
class Chunkv1(AbstractChunk):
    __version__ = 1

    def __init__(self, core: ChunkCore):
        super().__init__(core)
        self.__core = core

    @property
    def cx(self) -> int:
        return self.__core.cx

    @property
    def cz(self) -> int:
        return self.__core.cz
