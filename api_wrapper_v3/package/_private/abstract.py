from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Set, Type
import inspect


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
