import pygame


class Button:
    def __init__(self, x, y, text: str):
        self.x = x
        self.y = y

        self.font = pygame.font.SysFont("Calibri", 36)
        # Having the color seperate from the font allows you to change the
        # color when mouse hovers over text
        self.color = "white"
        self.text = text

        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # If the mouse is hovering above text
        self.hovered = False

        self.event = lambda: print("Default button")

    def update(self, dt):
        if self.hovered is True:
            self.color = "blue"
        else:
            self.color = "white"

        self.text_surface = self.font.render(self.text, True, self.color)

    def set_hover(self, hovered: bool):
        self.hovered = hovered

    def register_event(self, function):
        self.event = function

    def render(self, screen: pygame.Surface):
        screen.blit(self.text_surface, (self.x, self.y))
