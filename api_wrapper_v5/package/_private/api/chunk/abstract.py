from __future__ import annotations
from package._private.abstract import AbstractAPI

from .. import chunk as chunk_api
from .core import ChunkCore


class AbstractChunk(AbstractAPI):
    # No other logic should reside here expect for maybe a few getter methods and some (rare) common utility methods
    def __init__(self, core: ChunkCore):
        self.__core = core

    def cast_to(self, api: chunk_api.ChunkAPIsType) -> chunk_api.ChunkAPIs:
        # Since the core data is private only the class can pass it to a new API wrapper
        # I can't think of any other way of doing this without making the private data public
        # Since the validator can only be created after all the classes are imported the validator cannot be directly imported
        # Personally I feel this is less than ideal
        chunk_api.chunk_api_validator.check_api(api)
        return api(self.__core)
