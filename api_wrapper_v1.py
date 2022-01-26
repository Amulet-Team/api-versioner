"""
This is the first version of the API system that was proposed here
https://github.com/Amulet-Team/Amulet-Map-Editor/issues/548#issue-1111873319
"""

class Chunk:
    pass


Dimension = str


class APIDoesNotExist(Exception):
    pass


class APIManager:
    """A class to manage multiple API versions of a class"""
    def __init__(self, base_class):
        self.__base_class = base_class
        self.__api_versions = {}

    def get_api(self, api_version: int):
        """
        Get the class for the given API version.

        :param api_version: The API version
        :return:
        """
        try:
            return self.__api_versions[api_version]
        except KeyError:
            raise APIDoesNotExist(f"API V{api_version} does not exist for {self.__base_class}")

    def register_api(self, cls, api_version: int):
        """Register an API version. Must only be used by first party code."""
        assert issubclass(cls, self.__base_class) and isinstance(api_version, int), "cls must be a subclass of the base class and api_version must be an int."
        if api_version in self.__api_versions:
            raise ValueError(f"API version {api_version} has been registered twice.")
        self.__api_versions[api_version] = cls

    def register_api_decorator(self, api_version: int):
        """A decorator version of register_api. Must only be used by first party code."""
        def wrap_cls(cls):
            self.register_api(cls, api_version)
            return cls
        return wrap_cls


class WorldCore:
    """This class is private and stores the world state."""
    def __init__(self, path: str):
        self.chunks = {}


class BaseWorldAPI:
    """
    This is the base API for the world.
    It only stores one class which is what actually holds the world data which can be held my multiple API versions.
    """
    __slots__ = ("__world_core",)

    def __init__(self, world_core: WorldCore):
        self.__world_core = world_core

    def get_api(self, api_version: int):
        """
        Get a specific API version for the world.
        This allows switching API version so old operations can still run.
        """
        return world_api_manager.get_api(api_version)(self.__world_core)


world_api_manager = APIManager(BaseWorldAPI)


@world_api_manager.register_api_decorator(1)
class WorldAPI1(BaseWorldAPI):
    """This is the current API which is the default for backwards compatability."""
    def get_chunk(self, cx: int, cz: int, dimension: Dimension):
        print(f"dimension={dimension}, cx={cx}, cz={cz}")


@world_api_manager.register_api_decorator(2)
class WorldAPI2(BaseWorldAPI):
    """A new incompatible API."""
    def get_chunk(self, dimension: Dimension, cx: int, cz: int):
        """Dimension is now specified first."""
        print(f"dimension={dimension}, cx={cx}, cz={cz}")


def get_world(path: str, *, api_version: int = 1) -> BaseWorldAPI:
    """
    Get the world

    :param path: The path to the world.
    :param api_version: The API version for the world
    :return:
    """
    # set up the world core
    return world_api_manager.get_api(api_version)(WorldCore(path))


def main():
    # Get the V1 API
    api_v1: WorldAPI1 = get_world("test_world")
    api_v1.get_chunk(0, 0, "minecraft:overworld")

    # Get the V2 API
    api_v2: WorldAPI2 = get_world("test_world", api_version=2)
    api_v2.get_chunk("minecraft:overworld", 0, 0)

    # Get the V2 API from the V1 API
    api_v2_2: WorldAPI2 = api_v1.get_api(2)
    api_v2_2.get_chunk("minecraft:overworld", 0, 0)


if __name__ == '__main__':
    main()
