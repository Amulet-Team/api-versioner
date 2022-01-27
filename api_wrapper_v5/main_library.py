from __future__ import annotations

import asyncio

from package import load_world
from package.api.chunk import Chunkv1
from package.api.world import Worldv1, Worldv2


def main_v1():
    world_api = load_world(r"C:\Minecraft\World", Worldv1)
    chunk = world_api.get_chunk(0, 0, "minecraft:overworld")
    print("Old API:", chunk)


async def main_v2():
    world_api = load_world(r"C:\Minecraft\World", Worldv2)
    chunk = await world_api.get_chunk(Chunkv1, "minecraft:overworld", 0, 0)
    print("New API:", chunk)
    chunks = await asyncio.gather(
        world_api.get_chunk(Chunkv1, "minecraft:overworld", 0, 0),
        world_api.get_chunk(Chunkv1, "minecraft:overworld", 0, 1),
        world_api.get_chunk(Chunkv1, "minecraft:overworld", 0, 2),
    )
    print("New API:", chunks)


def main():
    main_v1()
    asyncio.run(main_v2())


if __name__ == '__main__':
    main()
