from abc import ABC, abstractmethod
import warnings
from typing import Dict, Callable
from contextvars import ContextVar


class AbstractAPI(ABC):
    """
    A decorator to store the implementation for each API version.
    Based on the ContextMajorVersion attribute the implementation can be switched.
    For functions the switching is done in __call__ at runtime.
    For class methods the switching is done at the point __get__ is called to support properties.
    This allows the actual method or function to only contain the implementation and none of the switching logic.
    This should make writing the actual code a lot easier.
    """

    @property
    @classmethod
    @abstractmethod
    def LibraryMajorVersion(cls) -> int:
        """
        The major version for the library.
        This should be a fixed int.
        """
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def ContextMajorVersion(cls) -> ContextVar:
        """
        The context local major version.
        A ContextVar has a local value for each context.
        This allows threading and asyncio code to each set a local library version.
        """
        raise NotImplementedError

    __slots__ = "__apis"

    def __init__(self):
        self.__apis: Dict[int, Callable] = {}

    @classmethod
    def new(cls, version: int):
        return cls().version(version)

    def version(self, version: int):
        if not (1 <= version <= self.LibraryMajorVersion + 1):
            raise ValueError(
                f"version must be between 1 and {self.LibraryMajorVersion + 1}"
            )

        def wrap(func):
            self.__apis[version] = func
            return self

        return wrap

    def _get_implementation(self):
        """Get the implementation for the callable"""
        lib_ver = self.ContextMajorVersion.get()
        if lib_ver in self.__apis:
            # Use the cached version if it exists
            if lib_ver < self.LibraryMajorVersion:
                warnings.warn(
                    f"API version {lib_ver} is depreciated. Consider updating the code to the new version",
                    DeprecationWarning,
                )
            return self.__apis[lib_ver]
        elif isinstance(lib_ver, int):
            if 1 <= lib_ver <= self.LibraryMajorVersion + 1:
                # Find the next lowest version
                lib_ver_ = next(
                    (v for v in sorted(self.__apis, reverse=True) if v < lib_ver), None
                )
                if lib_ver_ is None:
                    raise ValueError(
                        f"API version {lib_ver} is too low. This API version may have been removed."
                    )
                else:
                    func = self.__apis[lib_ver_]
                    for v in range(lib_ver_ + 1, lib_ver + 1):
                        self.__apis[v] = func
                    return func
            else:
                raise ValueError(
                    f"API version {lib_ver} is too high. It must be at most {self.LibraryMajorVersion + 1}"
                )
        else:
            raise TypeError("The version set in MajorVersion must be an int.")

    def __call__(self, *args, **kwargs):
        return self._get_implementation()(*args, **kwargs)

    def __get__(self, instance, instancetype):
        # Without this the reference to self is lost
        return self._get_implementation().__get__(instance, instancetype)


class AbstractLibraryVersion(ABC):
    @property
    @classmethod
    @abstractmethod
    def ContextMajorVersion(cls) -> ContextVar:
        raise NotImplementedError

    def __init__(self, version: int):
        self.__version = version
        self.__token = None

    def __enter__(self):
        self.__token = self.ContextMajorVersion.set(self.__version)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ContextMajorVersion.reset(self.__token)
