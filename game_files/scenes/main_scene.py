import json
import pygame
import time

from game_files.animations.projectile import Projectile

from game_files.camera import Camera

from game_files.pygame_util import SceneManager
from game_files.pygame_util import Scene

from game_files.players.player import Player
from game_files.players.enemy import Enemy

from game_files.tiles.tileset import Tileset
from game_files.tiles.tilemap import Tilemap


class MainScene(Scene):
    def __init__(
            self, manager: SceneManager, screen: pygame.Surface, sprites: dict
    ):
        super().__init__(manager, screen, sprites)

        self.previous_time = None

        MAP  =  [[101,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,102], 
                 [81,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 79], 
                 [81,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,79], 
                 [81,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,71, 0, 0, 0, 0, 0, 0, 0, 0, 0,79], 
                 [81, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,79],
                 [81, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,79],
                 [81, 0, 0, 0, 0, 0, 0, 0, 0,71, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,79],
                 [81, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,79],
                 [81, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,79],
                 [81, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,71, 0, 0, 0, 0, 0, 0, 0, 0, 0,79],
                 [81, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,79],
                 [112,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,113]]

        # Where the graphics are location, pixel size, and scale factor
        self.tileset = Tileset("gfx/rpg_sprites.png", 16, 4)
        # Create our tilemap
        self.tilemap = Tilemap(MAP, self.tileset)

        enemy_animations = {"enemy_idle": self.sprites["enemy_idle"]}
        self.enemy = Enemy(enemy_animations, 500, 500)

        player_animations = {
            "walking_animations": self.sprites["player_walk"],
            "attack_animation": self.sprites["player_attack"]
        }
        # Spawn the player with animations and what location
        self.player = Player(player_animations, 100, 100)

        self.camera = Camera(self.screen, self.player)

        # User input system
        self.keybinds = {pygame.K_w: "up",
                         pygame.K_s: "down",
                         pygame.K_a: "left",
                         pygame.K_d: "right"}
        self.keystack = []
        self.current_key = None

        self.projectiles = []

    def update(self) -> None:
        if self.previous_time is None:
            # First run through the loop needs a previous_time value to compute
            #  delta time to ensure everything is on the same time
            self.previous_time = time.time()
        # Delta time
        now = time.time()
        dt = now - self.previous_time
        self.previous_time = now

        self.enemy.update(dt)
        self.player.update(dt)

        for projectile in self.projectiles:
            projectile.update(dt)

        self.camera.update(dt)

    def render(self) -> None:
        # Clear screen
        self.screen.fill((30, 124, 184))

        # Go through our map and render the map
        for y in self.tilemap.map:
            for x in y:
                self.screen.blit(x.sprite, (
                    x.x + self.camera.get_camera_adjustments()[0],
                    x.y + self.camera.get_camera_adjustments()[1]
                    )
                )

        self.enemy.render(self.screen, self.camera.get_camera_adjustments())
        self.player.render(self.screen, self.camera.get_camera_adjustments())

        for projectile in self.projectiles:
            projectile.render(
                self.screen, self.camera.get_camera_adjustments()
            )

        # Update display
        pygame.display.update()

    def poll_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the window
                self.manager.quit_game()

            # Attack controls
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.attack()
                projectile = Projectile(
                    {
                        "projectile": self.sprites["projectile"]
                    },
                    self.player.x, self.player.y
                )
                projectile.set_direction(self.player.direction)
                self.projectiles.append(projectile)

            if event.type == pygame.KEYDOWN and event.key in self.keybinds:
                self.keystack.append(event.key)

            if event.type == pygame.KEYUP and event.key in self.keybinds:
                self.keystack.remove(event.key)

            # If keystack has keys inside it
            if len(self.keystack) > 0:
                if self.current_key != self.keystack[-1]:
                    self.current_key = self.keystack[-1]

                    self.player.set_direction(self.keybinds[self.current_key])
                    self.player.start_moving("walking_" + self.keybinds[event.key])  # noqa: E501

            # If keystack is empty, then player stops moving
            if len(self.keystack) == 0:
                self.current_key = None
                self.player.stop_moving()