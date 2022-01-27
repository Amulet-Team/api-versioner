from typing import Union, Type
import warnings

from package._private.abstract import AbstractAPIValidator

from .core import WorldCore
from .abstract import AbstractWorld
from .v1 import Worldv1
from .v2 import Worldv2

WorldAPIs = Union[Worldv1, Worldv2]
WorldAPIsType = Union[Type[Worldv1], Type[Worldv2]]


class WorldApiValidator(AbstractAPIValidator):
    APIBase = AbstractWorld


world_api_validator = WorldApiValidator()


def load_world(path: str, api: WorldAPIsType = None) -> WorldAPIs:
    if api is None:
        # We have added the api option to an existing function so we need to make it optional for now
        warnings.warn(
            "In the future get_world will require the api class as input. For now the v1 api will be used.",
            DeprecationWarning,
        )
        api = Worldv1
    world_api_validator.check_api(api)
    world_core = WorldCore(path)
    return api(world_core)
