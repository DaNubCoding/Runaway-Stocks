from pygame.locals import K_SPACE
import pytweening as tween
import pygame

from src.game.gridlines import GridManager, Barrier
from src.common.constants import BOLD_FONTS, WIDTH
from src.game.background import BGGridManager
from src.gui.elements import Label, Button
from src.management.scene import Scene
from src.common.utils import blur_surf
from src.common.tween import Tween
from src.game.player import Player

class MainMenuBG(Scene):
    def setup(self) -> None:
        super().setup()

        self.slowdown_tween = Tween(self, 0, 1, 0.5, tween.easeOutCirc)
        self.slowdown_tween.reset()
        self.blur_tween = Tween(self, 0.03, 0.25, -0.2, tween.easeInExpo, cutoff=0.031)
        self.blur_tween.reset()
        self.ending = False

        self.grid_manager = GridManager(self)
        self.bg_grid_manager = BGGridManager(self)
        self.player = Player(self)
        Barrier.reset()

    def update(self) -> None:
        super().update()

        self.slowdown_tween()
        self.dt *= self.slowdown_tween.value

        self.grid_manager.update()
        self.bg_grid_manager.update()

        if self.super_scene.ending:
            self.blur_tween()

        if self.blur_tween.ended:
            self.manager.new_scene("MainGame")

    def pre_sprite(self) -> None:
        self.surface.fill((30, 30, 30))

    def post_sprite(self) -> None:
        self.surface.blit(blur_surf(self.surface, self.blur_tween.value), (0, 0))

class MainMenuGUI(Scene):
    def setup(self) -> None:
        super().setup()

        self.surface.set_colorkey((0, 0, 0))

        Label(self, (WIDTH // 2, 140), "Runaway Stocks", BOLD_FONTS[90], (230, 230, 230)),
        Button(self, (WIDTH // 2, 360), "Start Game", BOLD_FONTS[20], (230, 230, 230), self.end, K_SPACE)

    def update(self) -> None:
        super().update()

    def pre_sprite(self) -> None:
        self.surface.fill((0, 0, 0, 0) if self.super_scene.ending else (0, 0, 0))

    def post_sprite(self) -> None:
        if not self.super_scene.ending: return
        self.alpha_tween()
        self.surface.set_alpha(self.alpha_tween.value)

    def end(self) -> None:
        self.super_scene.ending = True
        self.alpha_tween = Tween(self, 0, 255, -200, tween.easeInSine)
        self.alpha_tween.reset()
        self.surface = self.surface.convert_alpha()

class MainMenu(Scene):
    def setup(self) -> None:
        super().setup()

        self.background = MainMenuBG(self.manager, self.previous_scene, self)
        self.background.setup()
        self.gui = MainMenuGUI(self.manager, self.previous_scene, self)
        self.gui.setup()

        self.ending = False

    def update(self) -> None:
        super().update()

        self.background.update()
        self.gui.update()

    def pre_sprite(self) -> None:
        self.background.draw()
        self.gui.draw()