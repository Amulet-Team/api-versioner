from __future__ import annotations
from package._private.abstract import AbstractAPI

from .. import world as world_api
from .core import WorldCore


class AbstractWorld(AbstractAPI):
    # No other logic should reside here expect for maybe a few getter methods and some (rare) common utility methods
    def __init__(self, core: WorldCore):
        self.__core = core

    def cast_to(self, api: world_api.WorldAPIsType) -> world_api.WorldAPIs:
        # Since the core data is private only the class can pass it to a new API wrapper
        # I can't think of any other way of doing this without making the private data public
        # Since the validator can only be created after all the classes are imported the validator cannot be directly imported
        # Personally I feel this is less than ideal
        world_api.world_api_validator.check_api(api)
        return api(self.__core)
