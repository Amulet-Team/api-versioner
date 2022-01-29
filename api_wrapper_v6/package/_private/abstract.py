from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type, Dict, List
import inspect
import warnings

from package import __version__ as library_version
from package._private.api import manager

MajorVersion = library_version[0]


class AbstractCore:
    pass


class AbstractAPI(ABC):
    __slots__ = ("_core",)

    @property
    @classmethod
    @abstractmethod
    def __version__(cls) -> int:
        # The library version this class was added in
        raise NotImplementedError

    def __init__(self, core: AbstractCore):
        self._core = core

    @abstractmethod
    def cast_to(self, api: Type[AbstractAPI]) -> AbstractAPI:
        raise NotImplementedError


class RemovedAPI:
    """Subclassed to indicate the API is removed"""
    pass


class AbstractAPIFactory(ABC):
    __slots__ = ("__lock", "__apis")

    @property
    @classmethod
    @abstractmethod
    def APIBase(cls) -> Type[AbstractAPI]:
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def Core(cls) -> Type[AbstractCore]:
        raise NotImplementedError

    def __init__(self):
        self.__lock = False
        self.__apis: Dict[int, Type[AbstractAPI]] = {}
        manager.api_manager.register(self)

    def register(self, api: Type[AbstractAPI]) -> Type[AbstractAPI]:
        """Register an API version."""
        if self.__lock:
            raise Exception("The validator has been locked. Cannot register any new APIs.")
        if not issubclass(api, self.APIBase):
            raise Exception(f"{api} is not a subclass of {self.APIBase}")
        if inspect.isabstract(api):
            raise TypeError(f"Cannot register abstract class {api}")
        if api.__version__ in self.__apis:
            raise Exception(f"{api} is registered twice")
        self.__apis[api.__version__] = api
        return api

    def lock(self):
        """Lock the validator from accepting any new APIs"""
        if self.__lock:
            raise Exception(f"{self} has already been locked.")
        for version in range(min(self.__apis), max(MajorVersion, max(self.__apis))):
            if version not in self.__apis:
                # If the object has not been given a new version then use the previous version
                self.__apis[version] = self.__apis[version-1]
        self.__lock = True

    @property
    def api_versions(self) -> List[int]:
        return list(self.__apis)

    def get_api_cls(self, api_version: int) -> Type[AbstractAPI]:
        if not self.__lock:
            raise Exception(f"{self} has not been locked.")
        if api_version in self.__apis:
            api = self.__apis[api_version]
            if api_version != MajorVersion:
                if issubclass(api, RemovedAPI):
                    raise Exception(f"API version {api_version} has been removed.")
                else:
                    warnings.warn(
                        "BaseLevel.selection_bounds is depreciated and will be removed in the future. Please use BaseLevel.bounds(dimension) instead",
                        DeprecationWarning,
                    )
            return api
        else:
            raise TypeError(f"API Version {api_version} is not recognised. It must be an int from 1 to {MajorVersion}.")

    def get_api(self, api_version: int, core: AbstractCore) -> AbstractAPI:
        return self.get_api_cls(api_version)(core)
