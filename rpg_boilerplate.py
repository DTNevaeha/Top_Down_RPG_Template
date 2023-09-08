import pygame, random, time
from pygame_util import SceneManager, Scene

class MainScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict, debug: bool) -> None:
        super().__init__(manager, screen, sprites, debug)

        self.previous_time = None	

    def update(self) -> None:

        if self.previous_time is None: # First run through the loop needs a previous_time value to compute delta time
            self.previous_time = time.time()
        # Delta time
        now = time.time()
        dt = now - self.previous_time
        self.previous_time = now

    def render(self) -> None:
        # Clear screen
        self.screen.fill("black")

        # Update display
        pygame.display.update()

    def poll_events(self) -> None:
        for event in pygame.event.get():

            if event.type == pygame.QUIT: # If the user closes the window
                self.manager.quit_game()         

class Game:
    def __init__(self) -> None:
        # Initialize global game variables
        pygame.init() 
        self.screen = pygame.display.set_mode((1280, 720))
        self.running = True
        self.sprites = self.load_sprites()

        # Scene system
        self.scene_manager = SceneManager()

        scenes = {}



    # MAIN GAME LOOP #
    def run(self) -> None:
        self.previous_time = time.time()
        while self.running:

            self.scene_manager.current_scene.poll_events()
            self.scene_manager.current_scene.update()
            self.scene_manager.current_scene.render()

            if self.scene_manager.quit == True:
                self.running = False    

        pygame.quit()

    # Load sprite textures into pygame as surfaces. 
    # Returns a dictionary of names to surfaces.
    def load_sprites(self) -> dict: 
        sprites = {}

        return sprites

g = Game()
g.run()