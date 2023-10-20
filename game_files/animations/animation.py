import pygame

from game_files.tiles.tileset import Tileset


class Animation:
    def __init__(self, name: str, tileset: Tileset, keyframes: list[int]):
        self.name = name
        self.tileset = tileset
        self.keyframes = keyframes

        self.current_sprite_id = 0
        self.loop_animation = False
        self.animation_frequency = 0
        self.current_keyframe = 0
        # This measure frame activity time and ensures animations dont mess up
        # with game frames.
        self.keyframe_time = 0

    def get_current_sprite(self) -> pygame.Surface:
        return self.tileset.get_tile_sprite(self.current_sprite_id)

    def activate_animation(self, frequency: float, loop: bool):
        self.animation_frequency = frequency
        self.loop_animation = loop

    def deactivate_animation(self):
        self.animation_frequency = 0
        self.loop_animation = False

    def update(self, dt):
        self.keyframe_time += dt

        if self.keyframe_time >= self.animation_frequency:
            # Check to see if we are at the end of the animation loop
            if len(self.keyframes) - 1 <= self.current_keyframe:
                # if at the end of the animation then restart it
                if self.loop_animation is True:
                    self.current_keyframe = 0
                else:
                    self.deactivate_animation()

            # If at the beginning or middle of animation loop then continue
            # loop until reaching the end
            else:
                self.current_keyframe += 1
                self.current_sprite_id = self.keyframes[self.current_keyframe]

            self.keyframe_time = 0
