from __future__ import annotations
from typing import TYPE_CHECKING, Callable

from package._private.abstract import AbstractAPIFactory
from .core import WorldCore
from .abstract import AbstractWorld


if TYPE_CHECKING:
    from . import WorldAPIs, WorldAPIsType


class WorldApiFactory(AbstractAPIFactory):
    APIBase = AbstractWorld
    Core = WorldCore

    register: Callable[[WorldAPIsType], WorldAPIsType]
    get_api: Callable[[int, WorldCore], WorldAPIs]


factory = WorldApiFactory()
