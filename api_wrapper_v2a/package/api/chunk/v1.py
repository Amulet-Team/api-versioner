from package._private.api.chunk import ChunkCore

from .abstract import AbstractChunkAPI


class ChunkAPIv1(AbstractChunkAPI):
    def __init__(self, core: ChunkCore):
        self.__core = core

    @property
    def cx(self) -> int:
        return self.__core.cx

    @property
    def cz(self) -> int:
        return self.__core.cz
