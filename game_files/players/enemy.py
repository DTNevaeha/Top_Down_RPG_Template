import pygame

from game_files.animations.animation_manager import AnimationManager


class Enemy:
    def __init__(self, sprite_sheets: dict, x, y):
        self.sprite_sheets = sprite_sheets
        self.x = x
        self.y = y
        self.health = 30
        self.width = 200
        self.height = 200

        # Enemy sprite, pixil count, and size scale
        self.animations = AnimationManager(sprite_sheets, 50, 4)
        self.animations.register_animation("idle",
                                           [0, 1, 2, 3, 4],
                                           "enemy_idle"
                                           )
        self.animations.activate_animation("idle", 0.1, True)
    
    def take_damage(self, damage: int): 
        self.health -= damage
        # This is entirely for debugging purposes
        print(self.health)

    def update(self, dt):
        self.animations.update(dt)

    def render(self, screen: pygame.Surface, camera_adjustment: tuple):
        screen.blit(
            self.animations.get_current_sprite(),
            (
                self.x + camera_adjustment[0],
                self.y + camera_adjustment[1]
            )
        )
