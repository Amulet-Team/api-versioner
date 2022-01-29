from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

from package._private.abstract import AbstractAPI
from .core import WorldCore

if TYPE_CHECKING:
    from . import WorldAPIs


class AbstractWorld(AbstractAPI, ABC):
    _core: WorldCore

    # No other logic should reside here expect for maybe a few getter methods and some (rare) common utility methods
    def __init__(self, core: WorldCore):
        assert isinstance(core, WorldCore)
        super().__init__(core)

    def cast_to(self, api_version: int) -> WorldAPIs:
        # Since the core data is private only the class can pass it to a new API wrapper
        # I can't think of any other way of doing this without making the private data public
        # Since the validator can only be created after all the classes are imported the validator cannot be directly imported
        # Personally I feel this is less than ideal
        from .factory import factory
        return factory.get_api(api_version, self._core)
