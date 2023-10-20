import pygame


class Tileset:
    def __init__(
        self, filename: str, original_tilesize: int, scale_factor: int = 1, sprites=None
    ):
        # If there is no sprite set then use filename else use sprites setting
        if sprites is None:
            self.tilesheet = pygame.image.load(filename).convert_alpha()
        else:
            self.tilesheet = sprites

        self.tileset = {}  # dict of tile ids to tile images
        self.tilesize = original_tilesize
        self.scale_factor = scale_factor
        self.scaled_size = self.tilesize * self.scale_factor

        tile_id = 0
        for y in range(int(self.tilesheet.get_height() / self.tilesize)):
            for x in range(int(self.tilesheet.get_width() / self.tilesize)):
                # Sets x, y, height, width cordinates
                tile_rect = pygame.Rect(
                    x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize
                )

                tile_image = self.tilesheet.subsurface(tile_rect)

                # Allows to scale the tile sizes.
                tile_image = pygame.transform.scale(
                    tile_image,
                    (
                        tile_image.get_width() * self.scale_factor,
                        tile_image.get_height() * self.scale_factor,
                    ),
                )

                self.tileset[tile_id] = tile_image

                tile_id += 1

    def get_tileset(self) -> dict:
        return self.tileset

    def get_tile_sprite(self, id: int) -> pygame.Surface:
        return self.tileset[id]
