from typing import Union, Type
import warnings

from package._private.abstract import AbstractAPIFactory

from .core import WorldCore
from .abstract import AbstractWorldAPI
from .v1 import WorldAPIv1
from .v2 import WorldAPIv2

WorldAPIs = Union[WorldAPIv1, WorldAPIv2]
WorldAPIsType = Union[Type[WorldAPIv1], Type[WorldAPIv2]]


class WorldApiFactory(AbstractAPIFactory):
    APIBase = AbstractWorldAPI


world_api_factory = WorldApiFactory()


def load_world(path: str, api: WorldAPIsType = None) -> WorldAPIs:
    if api is None:
        # We have added the api option to an existing function so we need to make it optional for now
        warnings.warn(
            "In the future get_world will require the api class as input. For now the v1 api will be used.",
            DeprecationWarning,
        )
        api = WorldAPIv1
    world_core = WorldCore(path)
    return world_api_factory.get_api(api)(world_core)
