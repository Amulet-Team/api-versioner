"""
This is the second version of the API system that was based upon the version Podshot wrote
Original
https://github.com/Amulet-Team/Amulet-Map-Editor/issues/548#issuecomment-1020784077
Modified
https://github.com/Amulet-Team/Amulet-Map-Editor/issues/548#issuecomment-1021370241
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Set, Type, Union
import inspect
from dataclasses import dataclass, field
import warnings

import asyncio


# --- Start Private API ---
# These classes make up the private API.
# Only the public API is able to interact with these classes
# We should be able to modify these however we like as long as we update the public APIs to behave the same.
# I have added "Core" to the end to make it more clear that they are not public classes

@dataclass
class ChunkCore:
    cx: int
    cz: int
    # More chunk data


@dataclass
class WorldCore:
    path: str
    chunks: List[ChunkCore] = field(default_factory=list)
    # More world data

    # Any methods here make up the private API
    # They should only be used by the public API
    # Where possible the actual implementation should be here and the public API should exist just to handle API differences
    async def get_chunk(self, dimension: str, cx: int, cz: int) -> ChunkCore:
        await asyncio.sleep(1)
        return ChunkCore(cx, cz)


# More data classes...
# --- End Private API ---


# --- Start Abstract Base Classes ---
class AbstractAPI:
    pass


class DepreciatedAPI:
    """Subclassed to indicate the API is depreciated"""
    pass


class RemovedAPI:
    """Subclassed to indicate the API is removed"""
    pass


class AbstractAPIFactory(ABC):
    @property
    @classmethod
    @abstractmethod
    def APIBase(cls) -> Type[AbstractAPI]:
        # From what I can see this is the best way to define an abstract ClassVar
        raise NotImplementedError

    def __init__(self):
        self.__world_apis: Set[Type[AbstractAPI]] = set()

        for sub_class in self.APIBase.__subclasses__():
            if not inspect.isabstract(sub_class):
                self.__world_apis.add(sub_class)

    @property
    def apis(self) -> List[Type[AbstractAPI]]:
        return list(self.__world_apis)

    def get_api(self, api: Type[AbstractAPI]) -> Type[AbstractAPI]:
        if api in self.__world_apis:
            if issubclass(api, DepreciatedAPI):
                print(f"[WARN] API {api} is deprecated and is no longer maintained and not recommended for new development")
            elif issubclass(api, RemovedAPI):
                raise Exception(f"API {api} has been removed.")
            return api
        else:
            raise TypeError(f"Class {api} is not a valid API for {self.APIBase}.")


class AbstractChunkAPI(AbstractAPI):
    # No other logic should reside here expect for maybe a few getter methods and some (rare) common utility methods
    pass


class AbstractWorldAPI(AbstractAPI):
    # No other logic should reside here expect for maybe a few getter methods and some (rare) common utility methods
    pass
# --- End Abstract Base Classes ---


# --- Start Factory Classes ---
class WorldApiFactory(AbstractAPIFactory):
    APIBase = AbstractWorldAPI


class ChunkApiFactory(AbstractAPIFactory):
    APIBase = AbstractChunkAPI
# --- End Factory Classes ---


# --- Start Public API ---
# --- Start Public Chunk Classes ---
class ChunkAPIv1(AbstractChunkAPI):
    def __init__(self, core: ChunkCore):
        self.__core = core

    @property
    def cx(self) -> int:
        return self.__core.cx

    @property
    def cz(self) -> int:
        return self.__core.cz


ChunkAPIs = Union[ChunkAPIv1]
ChunkAPIsType = Union[Type[ChunkAPIv1]]
# Other versions added here as required
# --- End Public Chunk Classes ---


# --- Start Public World Classes ---
# Blocking IO API
# This emulates the current behaviour
class WorldAPIv1(AbstractWorldAPI):
    def __init__(self, core: WorldCore):
        self.__core = core

    def get_chunk(self, cx: int, cz: int, dimension: str) -> ChunkAPIv1:
        api_cls = chunk_factory.get_api(ChunkAPIv1)
        chunk_core: ChunkCore = asyncio.run(self.__core.get_chunk(dimension, cx, cz))
        return api_cls(chunk_core)


# AsyncIO API
# This is a possible future version of the API
class WorldAPIv2(AbstractWorldAPI):
    def __init__(self, core: WorldCore):
        self.__core = core

    async def get_chunk(self, chunk_api: ChunkAPIsType, dimension: str, cx: int, cz: int) -> ChunkAPIs:
        """
        Get a chunk from the world

        :param chunk_api: The API to expose the chunk data
        :param dimension: ...
        :param cx: ...
        :param cz: ...
        :return: The chunk in the requested API
        """
        api_cls: ChunkAPIsType = chunk_factory.get_api(chunk_api)
        chunk_core: ChunkCore = await self.__core.get_chunk(dimension, cx, cz)
        return api_cls(chunk_core)


WorldAPIs = Union[WorldAPIv1, WorldAPIv2]
WorldAPIsType = Union[Type[WorldAPIv1], Type[WorldAPIv2]]
# --- End Public World Classes ---
# --- End Public Classes ---


# --- Start Factory Instances ---
# These would be stored in a module somewhere
chunk_factory = ChunkApiFactory()
world_api_factory = WorldApiFactory()
# --- End Factory Instances ---


def get_world(path: str, api: WorldAPIsType = None) -> WorldAPIs:
    if api is None:
        # We have added the api option to an existing function so we need to make it optional for now
        warnings.warn(
            "In the future get_world will require the api class as input. For now the v1 api will be used.",
            DeprecationWarning,
        )
        api = WorldAPIv1
    world_core = WorldCore(path)
    return world_api_factory.get_api(api)(world_core)


# --- Start "external" code ---
def main_v1():
    world_api = get_world("C:\Minecraft\World", WorldAPIv1)
    chunk = world_api.get_chunk(0, 0, "minecraft:overworld")
    print("Old API:", chunk)


async def main_v2():
    world_api = get_world("C:\Minecraft\World", WorldAPIv2)
    chunk = await world_api.get_chunk(ChunkAPIv1, "minecraft:overworld", 0, 0)
    print("New API:", chunk)
    chunks = await asyncio.gather(
        world_api.get_chunk(ChunkAPIv1, "minecraft:overworld", 0, 0),
        world_api.get_chunk(ChunkAPIv1, "minecraft:overworld", 0, 1),
        world_api.get_chunk(ChunkAPIv1, "minecraft:overworld", 0, 2),
    )
    print("New API:", chunks)


def main():
    main_v1()
    asyncio.run(main_v2())


if __name__ == '__main__':
    main()
