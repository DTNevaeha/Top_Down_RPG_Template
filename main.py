import pygame
import time

from game_files.pygame_util import SceneManager

from game_files.scenes.main_scene import MainScene
from game_files.scenes.menu import MenuScene


class Game:
    def __init__(self):
        # Initialize global game variables
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.running = True
        self.sprites = self.load_sprites()

        # Scene system
        self.scene_manager = SceneManager()

        # All possible scenes
        scenes = {
            "main": MainScene(self.scene_manager, self.screen, self.sprites),
            "menu": MenuScene(self.scene_manager, self.screen, self.sprites),
        }
        self.scene_manager.initialize(scenes, "menu")

    # Main Game Loop
    def run(self):
        self.previous_time = time.time()
        while self.running:
            self.scene_manager.current_scene.poll_events()
            self.scene_manager.current_scene.update()
            self.scene_manager.current_scene.render()

            if self.scene_manager.quit is True:
                self.running = False

        pygame.quit()

    # Load sprite textures into pygame as surfaces.
    # Returns a dictionary of names to surfaces.
    def load_sprites(self) -> dict:
        sprites = {}

        sprites["enemy_idle"] = pygame.image.load("gfx/enemy_idle.png").convert_alpha()
        sprites["player_walk"] = pygame.image.load(
            "gfx/player_animations.png"
        ).convert_alpha()
        sprites["player_attack"] = pygame.image.load("gfx/attack.png").convert_alpha()
        sprites["projectile"] = pygame.image.load("gfx/projectile.png").convert_alpha()

        return sprites


game = Game()
game.run()
