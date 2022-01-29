from __future__ import annotations

from package.api.v1 import load_world


def main():
    world_api = load_world(r"C:\Minecraft\World")
    chunk = world_api.get_chunk(0, 0, "minecraft:overworld")
    print("Old API:", chunk)


if __name__ == '__main__':
    main()
