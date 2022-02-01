from contextvars import ContextVar

from api_versioner import AbstractAPIManager, AbstractVersion

from demo_package import __version__

DemoPackageMajorVersion = ContextVar("PackageMajorVersion", default=__version__[0])


class DemoPackageAPIManager(AbstractAPIManager):
    LibraryMajorVersion = __version__[0]
    ContextMajorVersion = DemoPackageMajorVersion


api_version = DemoPackageAPIManager.api_version


class DemoPackageVersion(AbstractVersion):
    ContextMajorVersion = DemoPackageMajorVersion
