from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type, Dict, Callable
import inspect


class AbstractAPI:
    pass


class DepreciatedAPI:
    """Subclassed to indicate the API is depreciated"""
    pass


class RemovedAPI:
    """Subclassed to indicate the API is removed"""
    pass


class AbstractAPIValidator(ABC):
    @property
    @classmethod
    @abstractmethod
    def APIBase(cls) -> Type[AbstractAPI]:
        # From what I can see this is the best way to define an abstract ClassVar
        raise NotImplementedError

    def __init__(self):
        self.__world_apis: Dict[Type[AbstractAPI], Callable[[], None]] = {}

        for sub_class in self.APIBase.__subclasses__():
            if not inspect.isabstract(sub_class):
                self.__world_apis[sub_class] = self._get_func(sub_class)

    @staticmethod
    def _get_func(api: Type[AbstractAPI]):
        """Precompute the outcome rather than doing it at runtime."""
        if issubclass(api, DepreciatedAPI):
            warn = True
            def func():
                nonlocal warn
                if warn:
                    print(f"[WARN] API {api} is deprecated and is no longer maintained and not recommended for new development")
                    warn = False
        elif issubclass(api, RemovedAPI):
            def func():
                raise Exception(f"API {api} has been removed.")
        else:
            def func():
                pass
        return func

    def check_api(self, api: Type[AbstractAPI]):
        if api in self.__world_apis:
            self.__world_apis[api]()
        else:
            raise TypeError(f"Class {api} is not a valid API for {self.APIBase}.")
