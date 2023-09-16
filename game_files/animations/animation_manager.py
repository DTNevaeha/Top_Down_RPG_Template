import pygame

from game_files.animations.animation import Animation
from game_files.tiles.tileset import Tileset


class AnimationManager:
    def __init__(self,
                 sprite_sheets: dict,
                 tile_size: int,
                 scale: int):
        self.tilesets = {}

        for sprite in sprite_sheets:
            tileset = Tileset("none", tile_size, scale, sprite_sheets[sprite])
            self.tilesets[sprite] = tileset

        self.animations = {}

        self.current_tileset = None

        # Get whatever is first set in our tileset, this dummy animation
        # shouldnt ever actually be played.
        self.active_animation = Animation("dummy",
                                          self.tilesets[list(
                                              self.tilesets.keys())[0]], [0])

    def register_animation(self,
                           name: str,
                           sprite_ids: list[int],
                           tileset: str
                           ):
        self.animations[name] = Animation(
            name,
            self.tilesets[tileset],
            sprite_ids
        )

    def get_current_sprite(self) -> pygame.Surface:
        # If there is an active animation then get the sprite for that
        if self.active_animation is not None:
            return self.active_animation.get_current_sprite()
        else:
            # if we have no animations happening return a dummy object
            return pygame.Surface((0, 0))

    def update(self, dt):
        # if there is an active animation then run this
        if self.active_animation is not None:
            self.active_animation.update(dt)

    def activate_animation(self, animation: str, frequency: float, loop: bool):
        self.active_animation = self.animations[animation]
        self.active_animation.animation_frequency = frequency
        self.active_animation.loop_animation = loop

    def deactivate_animation(self):
        self.active_animation = None
