import pygame

from game_files.tiles.tileset import Tileset


class Tile:
    def __init__(self, x, y, sprite: pygame.Surface, sprite_id: int):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.sprite_id = sprite_id

    def update(self):
        pass

    def render(self):
        pass


class Tilemap:
    # list of lists that contain integer tiles that are an ID for a particular
    # tile in a particular slot
    def __init__(self, map: list[list], tileset: Tileset):
        self.tileset = tileset
        self.map_spec = map
        # Default map is an empty list of lists filled to map specifications
        self.map = [[]]
        self.tilesize = self.tileset.scaled_size

        # Create map tiles from specifications
        x_coord = 0
        y_coord = 0
        for y in self.map_spec:
            row = []
            for x in y:
                sprite = self.tileset.get_tile_sprite(x)
                # x = whatever sprite id we are on, on the map.
                tile = Tile(x_coord, y_coord, sprite, x)
                row.append(tile)
                x_coord += self.tilesize
            # go down one row then reset x to 0 for the next row
            y_coord += self.tilesize
            x_coord = 0
            self.map.append(row)
