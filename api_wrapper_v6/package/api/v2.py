from package._private.api.chunk import Chunkv1 as Chunk
from package._private.api.world import Worldv2 as World, load_world as _load_world


def load_world(path: str) -> World:
    return _load_world(path, 2)
