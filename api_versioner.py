import functools
from abc import ABC, abstractmethod
import warnings
from typing import Dict, Callable
from contextvars import ContextVar
import inspect


class AbstractAPIManager(ABC):
    """
    A class to manage the API versions for a given API entry.
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

    __slots__ = ("__apis", "__last_version", "__doc_version")

    def __init__(self):
        self.__apis: Dict[int, Callable] = {}
        # track the last version that was defined so property setter decorators work
        self.__last_version: int = 0
        # track the version that update_wrapper was called with
        self.__doc_version: int = 0

    @classmethod
    def api_version(cls, version: int):
        if not isinstance(version, int):
            raise TypeError("version must be an int")
        if not (1 <= version <= cls.LibraryMajorVersion + 1):
            raise ValueError(
                f"version must be between 1 and {cls.LibraryMajorVersion + 1}"
            )

        def wrap(func):
            self = cls._get_self(func, version)

            if version in self.__apis:
                raise ValueError(f"API version {version} has already been registered.")
            self.__last_version = version
            self.__apis[version] = func
            return self

        return wrap

    @classmethod
    def _get_self(cls, func, version: int):
        """Stash the manager instance in a module variable for easy accessing."""
        # See if an API manager exists for this qualname
        # If it does use that if not create a new one
        module = inspect.getmodule(func)
        qualname = getattr(func, "__qualname__", None)
        func_ = func
        if module is None or qualname is None:
            # If we cannot find the module or qualified name then try our best to find them
            if isinstance(func, property):
                func_ = func.fget
                module = inspect.getmodule(func.fget)
                qualname = getattr(func.fget, "__qualname__", None)
            elif hasattr(func, "__func__"):
                func_ = func.__func__
                module = inspect.getmodule(func.__func__)
                qualname = getattr(func.__func__, "__qualname__", None)
            if module is None or qualname is None:
                # If all else fails there is nothing we can do
                raise TypeError(
                    f"Cannot find module or qualified name for {func}. If you are using a custom decorator you will need to use functools.update_wrapper"
                )
        api_managers = getattr(module, "__api_managers__", None)
        if api_managers is None:
            api_managers = {}
            setattr(module, "__api_managers__", api_managers)
        if qualname in api_managers:
            self = api_managers[qualname]
            if self.__class__ is not cls:
                raise ValueError("Cannot mix different API managers for the same API.")
        else:
            self = api_managers[qualname] = cls()
        if self.__doc_version < version <= self.LibraryMajorVersion:
            functools.update_wrapper(self, func_)
            self.__doc_version = version
        return self

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

    # If the object is a loose function this will get called
    def __call__(self, *args, **kwargs):
        return self._get_implementation()(*args, **kwargs)

    # If the function is attached to a class these will get called on object access which will pass control to the active implementation
    def __get__(self, instance, instancetype):
        # Without this the reference to self is lost
        return self._get_implementation().__get__(instance, instancetype)

    def __set__(self, instance, value):
        try:
            return self._get_implementation().__set__(instance, value)
        except AttributeError:
            raise AttributeError(f"Cannot set attribute {self.__name__}")

    def __getattr__(self, item: str):
        if isinstance(self.__apis[self.__last_version], property):
            if item in {"getter", "setter", "deleter"}:

                def wrap(func):
                    self.__apis[self.__last_version] = getattr(
                        self.__apis[self.__last_version], item
                    )(func)
                    return self

                return wrap
        # I would like to support more here but the result returned from the final decorator must be self
        # It is unknown weather the function is the decorator or a function that returns the decorator
        raise AttributeError(
            f"{self.__class__.__name__} object has no attribute {item}"
        )


class AbstractVersion(ABC):
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
