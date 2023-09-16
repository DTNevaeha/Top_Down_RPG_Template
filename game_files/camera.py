import pygame


class Camera:
    def __init__(self, screen: pygame.Surface, subject):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        # Subject is whatever we want the camera to follow
        self.subject = subject
        self.camera_adjustment_x = 0
        self.camera_adjustment_y = 0

        # Initial camera adjustment
        self.camera_adjustment_x = (self.screen_width / 2) - self.subject.x
        self.camera_adjustment_y = (self.screen_height / 2) - self.subject.y

    def get_camera_adjustments(self) -> tuple:
        return (self.camera_adjustment_x, self.camera_adjustment_y)

    def update(self, dt):
        self.camera_adjustment_x = (self.screen_width / 2) - self.subject.x
        self.camera_adjustment_y = (self.screen_height / 2) - self.subject.y
