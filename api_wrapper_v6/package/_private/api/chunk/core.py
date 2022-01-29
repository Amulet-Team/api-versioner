from __future__ import annotations
from dataclasses import dataclass

from package._private.abstract import AbstractCore


@dataclass
class ChunkCore(AbstractCore):
    cx: int
    cz: int
    # More chunk data
