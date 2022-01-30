from contextvars import ContextVar

from api_version import AbstractAPI, AbstractLibraryVersion

from demo_package import __version__

DemoPackageMajorVersion = ContextVar("PackageMajorVersion", default=__version__[0])


class DemoPackageAPI(AbstractAPI):
    LibraryMajorVersion = __version__[0]
    ContextMajorVersion = DemoPackageMajorVersion


class DemoPackageLibraryVersion(AbstractLibraryVersion):
    ContextMajorVersion = DemoPackageMajorVersion
