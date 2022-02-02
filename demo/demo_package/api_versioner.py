from contextvars import ContextVar
import re

from api_versioner import AbstractAPIManager, AbstractVersion

from demo_package import __version__ as version_string


# It would be better to do this with the packaging library
# from packaging.version import Version
# MajorVersion = Version(version_string).major
# but that may not be installed so find it with regex
MajorVersion = int(
    re.fullmatch(r"(?P<MajorVersion>\d+)\..*", version_string).group("MajorVersion")
)

DemoPackageMajorVersion = ContextVar("PackageMajorVersion", default=MajorVersion)


class DemoPackageAPIManager(AbstractAPIManager):
    LibraryMajorVersion = MajorVersion
    ContextMajorVersion = DemoPackageMajorVersion


api_version = DemoPackageAPIManager.api_version


class DemoPackageVersion(AbstractVersion):
    ContextMajorVersion = DemoPackageMajorVersion
