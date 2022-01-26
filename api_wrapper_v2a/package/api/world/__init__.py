from typing import Union, Type

from package._private.abstract import AbstractAPIFactory

from .abstract import AbstractWorldAPI
from .v1 import WorldAPIv1
from .v2 import WorldAPIv2

WorldAPIs = Union[WorldAPIv1, WorldAPIv2]
WorldAPIsType = Union[Type[WorldAPIv1], Type[WorldAPIv2]]


class WorldApiFactory(AbstractAPIFactory):
    APIBase = AbstractWorldAPI


world_api_factory = WorldApiFactory()
