import pygame, random, time
from pygame_util import SceneManager, Scene


class Tile:
    def __init__(self, x, y, sprite: pygame.Surface, sprite_id: int):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.sprite_id = sprite_id

    def update(self):
        pass

    def render(self):
        pass


class Tileset:
    def __init__(
        self, filename: str, original_tilesize: int, scale_factor: int = 1, sprites=None
    ):
        # If there is no sprite set then use filename else use sprites setting
        if sprites is None:
            self.tilesheet = pygame.image.load(filename).convert_alpha()
        else:
            self.tilesheet = sprites

        self.tileset = {}  # dict of tile ids to tile images
        self.tilesize = original_tilesize
        self.scale_factor = scale_factor
        self.scaled_size = self.tilesize * self.scale_factor

        tile_id = 0
        for y in range(int(self.tilesheet.get_height() / self.tilesize)):
            for x in range(int(self.tilesheet.get_width() / self.tilesize)):
                # Sets x, y, height, width cordinates
                tile_rect = pygame.Rect(
                    x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize
                )

                tile_image = self.tilesheet.subsurface(tile_rect)

                # Allows to scale the tile sizes.
                tile_image = pygame.transform.scale(
                    tile_image,
                    (
                        tile_image.get_width() * self.scale_factor,
                        tile_image.get_height() * self.scale_factor
                    ),
                )

                self.tileset[tile_id] = tile_image

                tile_id += 1

    def get_tileset(self) -> dict:
        return self.tileset

    def get_tile_sprite(self, id: int) -> pygame.Surface:
        return self.tileset[id]


class Tilemap:
    # list of lists that contain integer tiles that are an ID for a particular tile in a particular slot
    def __init__(self, map: list[list], tileset: Tileset):
        self.tileset = tileset
        self.map_spec = map
        # Default map is an empty list of lists filled to map specifications
        self.map = [[]]
        self.tilesize = self.tileset.scaled_size

        # Create map tiles from specifications
        x_coord = 0
        y_coord = 0
        for y in self.map_spec:
            row = []
            for x in y:
                sprite = self.tileset.get_tile_sprite(x)
                # x = whatever sprite id we are on, on the map.
                tile = Tile(x_coord, y_coord, sprite, x)
                row.append(tile)
                x_coord += self.tilesize
            # go down one row then reset x to 0 for the next row
            y_coord += self.tilesize
            x_coord = 0
            self.map.append(row)


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


class Button:
    def __init__(self, x, y, text: str):
        self.x = x
        self.y = y

        self.font = pygame.font.SysFont("Calibri", 36)
        # Having the color seperate from the font allows you to change the color when mouse hovers over text
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


class Player:
    def __init__(self, sprite_sheets: dict, x, y):
        self.x = x
        self.y = y
        self.velocity = 250
        self.direction = "down"
        self.moving = False
        # Character sheet, pixel count, and scale factor
        self.animations = AnimationManager(sprite_sheets, 16, 4)

        # Walking animations
        self.animations.register_animation("walking_right", [3, 7, 11, 15], "walking_animations")
        self.animations.register_animation("walking_left", [2, 6, 10, 14], "walking_animations")
        self.animations.register_animation("walking_up", [1, 5, 9, 13], "walking_animations")
        self.animations.register_animation("walking_down", [0, 4, 8, 12], "walking_animations")

        # Stationary sprites
        self.animations.register_animation("stationary_down", [0, 0, 0, 0], "walking_animations")
        self.animations.register_animation("stationary_up", [1, 1, 1, 1], "walking_animations")
        self.animations.register_animation("stationary_left", [2, 2, 2, 2], "walking_animations")
        self.animations.register_animation("stationary_right", [3, 3, 3, 3], "walking_animations")

        # Attacks
        self.animations.register_animation("attack_down", [0, 0, 0, 0], "attack_animation")
        self.animations.register_animation("attack_up", [1, 1, 1, 1], "attack_animation")
        self.animations.register_animation("attack_left", [2, 2, 2, 2], "attack_animation")
        self.animations.register_animation("attack_right", [3, 3, 3, 3], "attack_animation")

    def move(self, dt):
        if self.direction == "up":
            self.y -= self.velocity * dt
        elif self.direction == "down":
            self.y += self.velocity * dt
        elif self.direction == "left":
            self.x -= self.velocity * dt
        elif self.direction == "right":
            self.x += self.velocity * dt
    
    def attack(self):
        self.animations.activate_animation("attack_" + self.direction, 0.1, False)

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
        screen.blit(self.animations.get_current_sprite(), (self.x + camera_adjustment[0], self.y + camera_adjustment[1]))


class Enemy:
    def __init__(self, sprite_sheets: dict, x, y):
        self.sprite_sheets = sprite_sheets
        self.x = x
        self.y = y

        # Enemy sprite, pixil count, and size scale
        self.animations = AnimationManager(sprite_sheets, 50, 4)
        self.animations.register_animation("idle", [0, 1, 2 , 3, 4], "enemy_idle")
        self.animations.activate_animation("idle", 0.1, True)

    def update(self, dt):
        self.animations.update(dt)
    
    def render(self, screen: pygame.Surface, camera_adjustment: tuple):
        screen.blit(self.animations.get_current_sprite(), (self.x + camera_adjustment[0], self.y + camera_adjustment[1]))


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
            if button.hovered is False and button.rect.collidepoint(mouse_x, mouse_y):
                button.hovered = True
            
            # If mouse stops hovering over the button then set false
            if button.hovered is True and not button.rect.collidepoint(mouse_x, mouse_y):
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


class Projectile:
    def __init__(self, sprite_sheets: dict, x, y):
        self.sprite_sheets = sprite_sheets
        self.x = x
        self.y = y
        self.velocity = 500
        self.direction = "right"

        self.animations = AnimationManager(sprite_sheets, 16, 2)
        self.animations.register_animation("projectile", [0, 1, 2, 3, 4], "projectile")
        self.animations.activate_animation("projectile", 0.1, True)

    def move(self, dt):
        if self.direction == "up":
            self.y -= self.velocity * dt
        elif self.direction == "down":
            self.y += self.velocity * dt
        elif self.direction == "left":
            self.x -= self.velocity * dt
        elif self.direction == "right":
            self.x += self.velocity * dt

    def set_direction(self, new_direction: str):
        self.direction = new_direction

    def update(self, dt):
        self.animations.update(dt)
        self.move(dt)

    def render(self, screen: pygame.Surface, camera_adjustment: tuple):
        screen.blit(self.animations.get_current_sprite(),
                    (self.x + camera_adjustment[0], self.y + camera_adjustment[1]))

class Animation:
    def __init__(self,
                 name: str,
                 tileset: Tileset,
                 keyframes: list[int]):
        self.name = name
        self.tileset = tileset
        self.keyframes = keyframes

        self.current_sprite_id = 0
        self.loop_animation = False
        self.animation_frequency = 0
        self.current_keyframe = 0
        # This measure frame activity time and ensures animations dont mess up with game frames.
        self.keyframe_time = 0

    def get_current_sprite(self) -> pygame.Surface:
        return self.tileset.get_tile_sprite(self.current_sprite_id)
    
    def activate_animation(self, frequency: float, loop: bool):
        self.animation_frequency = frequency
        self.loop_animation = loop
    
    def deactivate_animation(self):
        self.animation_frequency = 0
        self.loop_animation = False

    def update(self, dt):
        self.keyframe_time += dt

        if self.keyframe_time >= self.animation_frequency:
            # Check to see if we are at the end of the animation loop
            if len(self.keyframes) - 1 <= self.current_keyframe:

                # if at the end of the animation then restart it
                if self.loop_animation is True:
                    self.current_keyframe = 0
                else:
                    self.deactivate_animation()

            # If at the beginning or middle of animation loop then continue loop
            else:
                self.current_keyframe += 1
                self.current_sprite_id = self.keyframes[self.current_keyframe]

            self.keyframe_time = 0


class AnimationManager:
    def __init__(self,
                 sprite_sheets: dict,
                 tile_size: int,
                 scale: int):
        self.tilesets = {}

        for sprite in sprite_sheets:
            tileset = Tileset("none", tile_size, scale, sprite_sheets[sprite])
            self.tilesets[sprite] = tileset

        self.animations = {}

        self.current_tileset = None

        # Get whatever is first set in our tileset, this dummy animation shouldnt ever actually be played.
        self.active_animation = Animation("dummy", self.tilesets[list(self.tilesets.keys())[0]], [0])

    def register_animation(self, name: str, sprite_ids: list[int], tileset: str):
        self.animations[name] = Animation(name, self.tilesets[tileset], sprite_ids)

    def get_current_sprite(self) -> pygame.Surface:
        # If there is an active animation then get the sprite for that
        if self.active_animation is not None:
            return self.active_animation.get_current_sprite()
        else:
            # if we have no animations happening return a dummy object
            return pygame.Surface((0,0))

    def update(self, dt):
        # if there is an active animation then run this
        if self.active_animation is not None:
            self.active_animation.update(dt)

    def activate_animation(self, animation: str, frequency: float, loop: bool):
        self.active_animation = self.animations[animation]
        self.active_animation.animation_frequency = frequency
        self.active_animation.loop_animation = loop

    def deactivate_animation(self):
        self.active_animation = None


class MainScene(Scene):
    def __init__(
        self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
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
            # First run through the loop needs a previous_time value to compute delta time
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
                self.screen.blit(x.sprite, (x.x + self.camera.get_camera_adjustments()[0],
                                            x.y + self.camera.get_camera_adjustments()[1]))

        self.enemy.render(self.screen, self.camera.get_camera_adjustments())
        self.player.render(self.screen, self.camera.get_camera_adjustments())

        for projectile in self.projectiles:
            projectile.render(self.screen, self.camera.get_camera_adjustments())

        # Update display
        pygame.display.update()

    def poll_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the window
                self.manager.quit_game()

            # Attack controls
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.attack()
                projectile = Projectile({"projectile": self.sprites["projectile"]}, self.player.x, self.player.y)
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
                    self.player.start_moving("walking_" + self.keybinds[event.key])
            
            # If keystack is empty, then player stops moving
            if len(self.keystack) == 0:
                self.current_key = None
                self.player.stop_moving()


class Game:
    def __init__(self) -> None:
        # Initialize global game variables
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.running = True
        self.sprites = self.load_sprites()

        # Scene system
        self.scene_manager = SceneManager()

        # All possible scenes
        scenes = {"main": MainScene(self.scene_manager, self.screen, self.sprites),
                  "menu": MenuScene(self.scene_manager, self.screen, self.sprites)}
        self.scene_manager.initialize(scenes, "menu")

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

        sprites["enemy_idle"] = pygame.image.load("gfx/enemy_idle.png").convert_alpha()
        sprites["player_walk"] = pygame.image.load("gfx/player_animations.png").convert_alpha()
        sprites["player_attack"] = pygame.image.load("gfx/attack.png").convert_alpha()
        sprites["projectile"] = pygame.image.load("gfx/projectile.png").convert_alpha()

        return sprites


g = Game()
g.run()
