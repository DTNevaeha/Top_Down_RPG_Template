import pygame

from game_files.animations.animation_manager import AnimationManager
from game_files.config import map_width, map_height


class Player:
    def __init__(self, sprite_sheets: dict, x, y):
        self.x = x
        self.y = y
        self.velocity = 250
        self.direction = "down"
        self.moving = False
        # Character sheet, pixel count, and scale factor
        self.animations = AnimationManager(sprite_sheets, 16, 4)
        self.health = 100

        # Walking animations
        self.animations.register_animation("walking_right", [3, 7, 11, 15], "walking_animations")
        self.animations.register_animation("walking_left", [2, 6, 10, 14], "walking_animations")
        self.animations.register_animation("walking_up", [1, 5, 9, 13], "walking_animations")
        self.animations.register_animation("walking_down", [0, 4, 8, 12], "walking_animations")

        # Stationary sprites
        self.animations.register_animation("stationary_down", [0, 0, 0], "walking_animations")
        self.animations.register_animation("stationary_up", [1, 1, 1], "walking_animations")
        self.animations.register_animation("stationary_left", [2, 2, 2], "walking_animations")
        self.animations.register_animation("stationary_right", [3, 3, 3], "walking_animations")

        # Attacks
        self.animations.register_animation("attack_down", [0, 0, 0], "attack_animation")
        self.animations.register_animation("attack_up", [1, 1, 1], "attack_animation")
        self.animations.register_animation("attack_left", [2, 2, 2], "attack_animation")
        self.animations.register_animation("attack_right", [3, 3, 3], "attack_animation")

    def move(self, dt):
        self.height = 4
        self.width = 16

        # Prevent the player from leaving the set map. This only works if the map size never changes
        if self.y < 0:
            self.y = 0
        elif self.x < 0:
            self.x = 0
        elif self.y > map_height - self.height:
            self.y = map_height - self.height
        elif self.x > map_width - self.width:
            self.x = map_width - self.width

        if self.direction == "up":
            self.y -= self.velocity * dt
        elif self.direction == "down":
            self.y += self.velocity * dt
        elif self.direction == "left":
            self.x -= self.velocity * dt
        elif self.direction == "right":
            self.x += self.velocity * dt

    def attack(self):
        self.animations.activate_animation("attack_" + self.direction, 0.15, False)
    
    def set_direction(self, new_direction: str):
        self.direction = new_direction

    def start_moving(self, animation: str):
        self.moving = True
        self.animations.activate_animation(animation, 0.15, True)

    def stop_moving(self):
        self.moving = False
        self.animations.activate_animation("stationary_" + self.direction, 0.1, True)

    def update(self, dt):
        if self.moving:
            self.move(dt)

        self.animations.update(dt)

    def render(self, screen: pygame.Surface, camera_adjustment: tuple):
        screen.blit(
            self.animations.get_current_sprite(),
            (self.x + camera_adjustment[0], self.y + camera_adjustment[1]),
        )
