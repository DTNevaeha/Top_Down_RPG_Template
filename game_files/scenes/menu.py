import pygame
import time

from game_files.button import Button

from game_files.pygame_util import SceneManager
from game_files.pygame_util import Scene


class MenuScene(Scene):
    def __init__(self,
                 manager: SceneManager,
                 screen: pygame.Surface,
                 sprites: dict):
        super().__init__(manager, screen, sprites)

        self.previous_time = None

        # Create buttons
        self.quit_button = Button(500, 400, "Quit Game")
        self.start_button = Button(500, 300, "Start Game")

        # Create button events
        def quit_button():
            self.manager.quit = True

        def start_button():
            self.manager.set_scene("main")

        self.quit_button.register_event(quit_button)
        self.start_button.register_event(start_button)

        self.buttons = [self.quit_button, self.start_button]

    def update(self):
        if self.previous_time is None:
            self.previous_time = time.time()

        # Delta time
        now = time.time()
        dt = now - self.previous_time
        self.previous_time = now

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for button in self.buttons:
            # If mouse pointer is hovering over a button then set true
            if button.hovered is False and button.rect.collidepoint(mouse_x,
                                                                    mouse_y):
                button.hovered = True

            # If mouse stops hovering over the button then set false
            if button.hovered is True and not button.rect.collidepoint(
                mouse_x, mouse_y
            ):
                button.hovered = False

        self.quit_button.update(dt)
        self.start_button.update(dt)

    def render(self):
        self.screen.fill("black")

        self.quit_button.render(self.screen)
        self.start_button.render(self.screen)

        pygame.display.update()

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.quit_game()

            # Mouse detection
            # If the mouse left clicks on a button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.hovered:
                        button.event()
