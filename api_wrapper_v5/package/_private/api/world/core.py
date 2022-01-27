import asyncio
from dataclasses import dataclass, field
from typing import List

from package._private.api.chunk import ChunkCore, chunk_api_validator, ChunkAPIs, ChunkAPIsType


@dataclass
class WorldCore:
    path: str
    chunks: List[ChunkCore] = field(default_factory=list)
    # More world data

    # Any methods here make up the private API
    # They should only be used by the public API
    # Where possible the actual implementation should be here and the public API should exist just to handle API differences
    async def get_chunk(
        self,
        chunk_api: ChunkAPIsType,
        dimension: str,
        cx: int,
        cz: int
    ) -> ChunkAPIs:
        await asyncio.sleep(1)
        chunk_api_validator.check_api(chunk_api)
        chunk_core = ChunkCore(cx, cz)
        return chunk_api(chunk_core)
