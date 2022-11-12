from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.management.scene import Scene

from pygame.locals import SRCALPHA, BLEND_RGB_SUB
from random import randint, choice
import pygame

from src.common.constants import FONTS, VEC, _pos, BULL_COLOR, BEAR_COLOR, WIDTH, HEIGHT, SHADOW_OFFSET
from src.management.sprite import VisibleSprite, Layers
from src.game.effects import Particle, Shockwave
from src.common.audio import point_pickup

class Point(VisibleSprite):
    class PointShadows(VisibleSprite):
        def __init__(self, scene: Scene) -> None:
            super().__init__(scene, Layers.PLAYER_SHADOW)
            self.surface = pygame.Surface((WIDTH, HEIGHT))

        def update(self) -> None:
            # Nothing to do in here
            pass

        def draw(self) -> None:
            self.manager.screen.blit(self.surface, (0, 0), special_flags=BLEND_RGB_SUB)
            self.surface = pygame.Surface((WIDTH, HEIGHT))

    def __init__(self, scene: Scene, val: int, pos: _pos) -> None:
        super().__init__(scene, Layers.POINTS)
        self.val = val
        self.color = BULL_COLOR if self.val > 0 else BEAR_COLOR
        self.pos = VEC(pos)
        self.surface = pygame.Surface((20, 20))

    def update(self) -> None:
        if self.pos.distance_to(self.scene.player.pos) < 10:
            self.scene.player.score += self.val
            self.kill()
            return
        screen_pos = self.pos - self.scene.player.camera.offset
        if screen_pos.x < -20:
            super().kill()

    def draw(self) -> None:
        draw_center = self.pos - self.scene.player.camera.offset
        r = 8

        shadow_surf = pygame.Surface((r * 2, r * 2))
        pygame.draw.circle(shadow_surf, (60, 60, 60), (r, r), r)
        self.manager.screen.blit(shadow_surf, draw_center - (r, r) + SHADOW_OFFSET, special_flags=BLEND_RGB_SUB)

        trans_surf = pygame.Surface((r * 2, r * 2), SRCALPHA)
        pygame.draw.circle(trans_surf, (*self.color, 100), (r, r), r)
        self.manager.screen.blit(trans_surf, draw_center - VEC(r, r))

        pygame.draw.circle(self.manager.screen, self.color, draw_center, r - 3)
        self.manager.screen.blit(FONTS[16].render(str(self.val), True, self.color), draw_center + VEC(3, 1))

    def kill(self) -> None:
        if self.scene.__class__.__name__ == "MainGame":
            choice(point_pickup).play()
        for _ in range(randint(60, 80)):
            Particle(self.scene, self.pos, self.color)
        Shockwave(self.scene, self.pos, self.color, 5, 50, 6)
        super().kill()