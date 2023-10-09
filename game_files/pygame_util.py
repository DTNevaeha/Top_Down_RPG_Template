import pygame
import random
import time


class Entity:
    def __init__(self):
        pass

    def update(self, dt):
        pass

    def render(self, screen: pygame.Surface):
        pass


# Switching between scenes
class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.quit = False

    def initialize(self, scenes: dict, starting_scene: str):
        self.scenes = scenes
        self.current_scene = self.scenes[starting_scene]

    def set_scene(self, new_scene: str):
        self.current_scene = self.scenes[new_scene]

    def get_scene(self):
        return self.current_scene

    def quit_game(self):
        self.quit = True


# A scene is a collection of objects that are set to be updated and rendered
# in any given frame. It allows us to quickly switch between, for instance, a
# start menu and the main game scene, or different areas in an RPG.
class Scene:
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
        self.manager = manager
        self.screen = screen
        self.sprites = sprites

    def update(self):
        pass

    def render(self):
        pass

    def poll_events(self):
        pass
