from __future__ import annotations

import warnings

from package.api.world import WorldAPIsType, WorldAPIs, WorldAPIv1, world_api_factory
from package._private.api.world import WorldCore


def get_world(path: str, api: WorldAPIsType = None) -> WorldAPIs:
    if api is None:
        # We have added the api option to an existing function so we need to make it optional for now
        warnings.warn(
            "In the future get_world will require the api class as input. For now the v1 api will be used.",
            DeprecationWarning,
        )
        api = WorldAPIv1
    world_core = WorldCore(path)
    return world_api_factory.get_api(api)(world_core)
