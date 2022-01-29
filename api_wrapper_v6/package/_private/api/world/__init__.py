from typing import Union, Type
import warnings

from .core import WorldCore
from .abstract import AbstractWorld
from .factory import factory
from .v1 import Worldv1
from .v2 import Worldv2
from .v3 import Worldv3

factory.lock()

WorldAPIs = Union[Worldv1, Worldv2, Worldv3]
WorldAPIsType = Union[Type[Worldv1], Type[Worldv2], Type[Worldv3]]


def load_world(path: str, api_version: int = None) -> WorldAPIs:
    if api_version is None:
        # We have added the api option to an existing function so we need to make it optional for now
        warnings.warn(
            "In the future get_world will require the api class as input. For now the v1 api will be used.",
            DeprecationWarning,
        )
        api_version = 1
    return factory.get_api(api_version, WorldCore(path))
