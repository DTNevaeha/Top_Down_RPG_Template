import pygame, time, random

class Entity:
    def __init__(self) -> None:
        pass

    def update(self, dt) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass

# Handles switching between scenes
class SceneManager:
    def __init__(self) -> None:
        self.scenes = {}
        self.quit = False

    def initialize(self, scenes: dict, starting_scene: str) -> None:
        self.scenes = scenes
        self.current_scene = self.scenes[starting_scene]

    def set_scene(self, new_scene: str) -> None:
        self.current_scene = self.scenes[new_scene]

    def get_scene(self) -> None:
        return self.current_scene

    def quit_game(self) -> None:
        self.quit = True

# A scene is a collection of objects that are set to be updated and rendered
# in any given frame. It allows us to quickly switch between, for instance, a start menu
# and the main game scene, or different areas in an RPG.
class Scene:
    def __init__(self, manager: SceneManager, 
                 screen: pygame.Surface, 
                 sprites: dict) -> None:
        self.manager = manager
        self.screen = screen
        self.sprites = sprites

    def update(self) -> None:
        pass

    def render(self) -> None:
        pass

    def poll_events(self) -> None:
        pass

