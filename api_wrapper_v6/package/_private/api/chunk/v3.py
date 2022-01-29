from .factory import factory
from .v1 import Chunkv1


@factory.register
class Chunkv3(Chunkv1):
    __version__ = 3

    # Lets pretend something here changed to require a new version
