import asyncio
from dataclasses import dataclass, field
from typing import List
from package._private.api.chunk.core import ChunkCore


@dataclass
class WorldCore:
    path: str
    chunks: List[ChunkCore] = field(default_factory=list)
    # More world data

    # Any methods here make up the private API
    # They should only be used by the public API
    # Where possible the actual implementation should be here and the public API should exist just to handle API differences
    async def get_chunk(self, dimension: str, cx: int, cz: int) -> ChunkCore:
        await asyncio.sleep(1)
        return ChunkCore(cx, cz)
