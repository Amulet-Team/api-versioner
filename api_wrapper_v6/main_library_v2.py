from __future__ import annotations

import asyncio

from package.api.v2 import load_world


async def main_v2():
    world_api = load_world(r"C:\Minecraft\World")
    chunk = await world_api.get_chunk("minecraft:overworld", 0, 0)
    print("New API:", chunk)
    chunks = await asyncio.gather(
        world_api.get_chunk("minecraft:overworld", 0, 0),
        world_api.get_chunk("minecraft:overworld", 0, 1),
        world_api.get_chunk("minecraft:overworld", 0, 2),
    )
    print("New API:", chunks)


def main():
    asyncio.run(main_v2())


if __name__ == '__main__':
    main()
