from __future__ import annotations
from typing import List
import asyncio
from dataclasses import dataclass, field

from package._private.abstract import AbstractCore
from package._private.api.chunk import ChunkCore


@dataclass
class WorldCore(AbstractCore):
    path: str
    chunks: List[ChunkCore] = field(default_factory=list)
    # More world data

    # Any methods here make up the private API
    # They should only be used by the public API
    # Where possible the actual implementation should be here and the public API should exist just to handle API differences
    async def get_chunk_core(
            self,
            dimension: str,
            cx: int,
            cz: int
    ) -> ChunkCore:
        await asyncio.sleep(1)
        return ChunkCore(cx, cz)
