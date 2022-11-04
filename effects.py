from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager import GameManager
    from elements import PowerTimer

from numpy import cos, radians, sin
from random import uniform, randint
import pygame

from utils import Sprite, inttup, pygame_draw_pie
from constants import VEC, _pos, _color

class Particle(Sprite):
    instances = []
    
    @classmethod
    def update_all(cls) -> None:
        for instance in cls.instances:
            instance.update()
            
    @classmethod
    def draw_all(cls) -> None:
        for instance in cls.instances:
            instance.draw()

    def __init__(self, manager: GameManager, pos: _pos, color: _color):
        super().__init__(manager)
        __class__.instances.append(self)
        self.pos = VEC(pos)
        self.vel = VEC(uniform(-30, 30), uniform(-30, 30))
        while self.vel.x == 0 and self.vel.y == 0:
            self.vel = VEC(uniform(-160, 160), uniform(-160, 160))
        self.size = randint(1, 2)
        self.color = color

    def update(self) -> None:
        if self.vel.x <= 2 and self.vel.y < 2:
            self.__class__.instances.remove(self)
            return
        self.vel -= self.vel.normalize() * 30 * self.manager.dt
        self.pos += self.vel * self.manager.dt

    def draw(self) -> None:
        pygame.draw.circle(self.manager.screen, self.color, inttup(self.pos - self.scene.player.camera.offset), self.size)

class Shockwave(Sprite):
    instances = []
    
    @classmethod
    def update_all(cls) -> None:
        for instance in cls.instances:
            instance.update()

    @classmethod
    def draw_all(cls) -> None:
        for instance in cls.instances:
            instance.draw()

    def __init__(self, manager: GameManager, pos: _pos, color: _color, start_width: int, expansion_speed: float, thinnen_speed: float) -> None:
        super().__init__(manager)
        __class__.instances.append(self)
        self.pos = VEC(pos)
        self.color = color
        self.radius = 0
        self.width = start_width
        self.expansion_speed = expansion_speed
        self.thinnen_speed = thinnen_speed

    def update(self) -> None:
        self.radius += self.expansion_speed * self.manager.dt
        self.width -= self.thinnen_speed * self.manager.dt
        if self.width <= 0.6:
            self.__class__.instances.remove(self)

    def draw(self) -> None:
        pygame.draw.circle(self.manager.screen, self.color, self.pos - self.scene.player.camera.offset, self.radius, round(self.width))

class PowerTimerPlayerDisplay(Sprite):
    instances = []

    @classmethod
    def draw_all(cls) -> None:
        for instance in cls.instances:
            instance.draw()

    def __init__(self, manager: GameManager, master: PowerTimer) -> None:
        super().__init__(manager)
        __class__.instances.append(self)
        self.master = master

    def update(self) -> None:
        # Nothing to do here lol
        pass

    def draw(self) -> None:
        center = self.scene.player.pos - self.scene.player.camera.offset
        angle = int(self.master.current_time / self.master.max_time * 360) + 180
        rad = 35
        pygame_draw_pie(self.manager.screen, (255, 255, 255, 70), center, rad, 180, angle)
        pygame.draw.line(self.manager.screen, (150, 150, 150), center, center + VEC(sin(radians(180)), -cos(radians(180))) * rad, 1)
        pygame.draw.line(self.manager.screen, (150, 150, 150), center, center + VEC(sin(radians(angle)), -cos(radians(angle))) * rad, 1)