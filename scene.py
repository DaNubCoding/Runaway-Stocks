from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from manager import GameManager

from pygame.locals import KEYDOWN, K_SPACE, K_ESCAPE
import pygame

from constants import HEIGHT, HIGHSCORE_FILE, CENTER, BOLD_FONTS, WIDTH, Anchors
from hud import Image, Label, MainGameTimer, Timer
from gridlines import GridManager, Barrier
from barrier_powers import barrier_powers
from images import title_1, title_2
from sprite import SpriteManager, Layers
from player import Player

def blur_surf(surf: pygame.Surface) -> pygame.Surface:
    """Smooth scale it down and up, then normal scale it down and up, to create a blur effect plus a pixelated effect"""
    surf = pygame.transform.smoothscale_by(surf, 0.25)
    surf = pygame.transform.smoothscale_by(surf, 4)
    surf = pygame.transform.scale_by(surf, 0.25)
    surf = pygame.transform.scale_by(surf, 4)
    return surf

def create_blurred_bg(manager: GameManager) -> Image:
    """
    - Blur screen as surface
    - Create a custom Image object that will be displayed
    - Also return the object for accessibility
    """

    blurred_img_surf = blur_surf(manager.screen)
    blurred_img_obj = Image(manager, (0, 0), blurred_img_surf, anchor=Anchors.TOPLEFT)
    return blurred_img_obj

class Scene:
    def __init__(self, manager: GameManager, previous_scene: Scene) -> None:
        self.manager = manager
        self.previous_scene = previous_scene

    def setup(self) -> None:
        self.sprite_manager = SpriteManager(self.manager)
        self.running = True

    def update(self) -> None:
        self.sprite_manager.update()

    def draw(self) -> None:
        self.sprite_manager.draw()

class MainMenu(Scene):
    def __init__(self, manager: GameManager, previous_scene: Scene) -> None:
        super().__init__(manager, previous_scene)

    def setup(self) -> None:
        super().setup()

        self.grid_manager = GridManager(self.manager)

        Image(self.manager, (WIDTH // 2, HEIGHT // 2 - 100), title_1)
        Image(self.manager, (WIDTH // 2, HEIGHT // 2 - 100), title_2)
        self.player = Player(self.manager)
        Barrier.instance = None
        Barrier.last_position = 0
        for power in barrier_powers:
            power.init = False

    def update(self) -> None:
        super().update()

        self.grid_manager.update()

        if KEYDOWN in self.manager.events and self.manager.events[KEYDOWN].key == K_SPACE:
            self.manager.new_scene("MainGame")

    def draw(self) -> None:
        self.manager.screen.fill((30, 30, 30))

        super().draw()
        self.manager.screen.blit(blur_surf(self.manager.screen), (0, 0))

class MainGame(Scene):
    def __init__(self, manager: GameManager, previous_scene: Scene) -> None:
        super().__init__(manager, previous_scene)

    def setup(self) -> None:
        super().setup()

        self.grid_manager = GridManager(self.manager)

        MainGameTimer(self.manager)

        self.player = Player(self.manager)
        Barrier.instance = None
        Barrier.last_position = 0
        for power in barrier_powers:
            power.init = False

    def update(self) -> None:
        super().update()

        self.grid_manager.update()

        
        if KEYDOWN in self.manager.events and self.manager.events[KEYDOWN].key == K_ESCAPE:
            self.manager.new_scene("PauseMenu")

    def draw(self) -> None:
        self.manager.screen.fill((30, 30, 30))

        super().draw()

class PauseMenu(Scene):
    def __init__(self, manager: GameManager, previous_scene: Scene) -> None:
        super().__init__(manager, previous_scene)

    def setup(self) -> None:
        super().setup()

        Timer.pause_all()

        create_blurred_bg(self.manager)
        Label(self.manager, (WIDTH // 2, HEIGHT // 2), "Game Paused", BOLD_FONTS[80], (230, 230, 230))

    def update(self) -> None:
        super().update()

        if KEYDOWN in self.manager.events and self.manager.events[KEYDOWN].key == K_ESCAPE:
            self.manager.switch_scene(self.previous_scene)

class EndMenu(Scene):
    def __init__(self, manager: GameManager, previous_scene: Scene) -> None:
        super().__init__(manager, previous_scene)

    def setup(self) -> None:
        super().setup()

        create_blurred_bg(self.manager)

        try: # Try to open the highscore file and read the highscore
            with open(HIGHSCORE_FILE, "r") as f:
                self.highscore = int(f.read())
        except FileNotFoundError: # If the file isn't found, create the file
            f = open(HIGHSCORE_FILE, "x")
            f.close()
            self.highscore = 0
        except ValueError: # If file contains invalid format, set it to 0
            self.highscore = 0

        # If it is a new highscore, display "New Highscore!"
        if self.previous_scene.player.score > self.highscore:
            Label(self.manager, CENTER, "New Highscore!", BOLD_FONTS[64], (230, 230, 230))
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(self.previous_scene.player.score)) # Update the highscore in the file
        else: # If it is not a new highscore, display the current highscore
            Label(self.manager, CENTER, f"Highscore: {self.highscore}", BOLD_FONTS[64], (230, 230, 230))

        # Create labels to display the score and a prompt
        Label(self.manager, CENTER - (0, 100), f"Score: {self.previous_scene.player.score}", BOLD_FONTS[64], (230, 230, 230))
        Label(self.manager, CENTER + (0, 100), "Press space to restart", BOLD_FONTS[18], (230, 230, 230))

    def update(self) -> None:
        super().update()

        if KEYDOWN in self.manager.events and self.manager.events[KEYDOWN].key == K_SPACE:
            # Start new game
            self.manager.new_scene("MainGame")