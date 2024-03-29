from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.management.scene import Scene

from random import randint, uniform

class Power:
    init = False
    @staticmethod
    def reset(scene: Scene):
        # Must-have method so that .reset() can be called for all powers
        ...

class Flip(Power):
    stackable = False
    max_time = 5

class Angle(Power):
    stackable = False
    max_time = 5
    angle = randint(20, 30) if randint(0, 1) else randint(50, 60)
    @staticmethod
    def reset(scene: Scene):
        __class__.angle = randint(20, 30) if randint(0, 1) else randint(50, 60)
        
class Speed(Power):
    stackable = True
    max_time = 10
    speed = uniform(1.2, 1.5)
    @staticmethod
    def reset(scene: Scene):
        __class__.speed = scene.player.speed * uniform(1.2, 1.5)

# Values are weights
barrier_powers = {
    Flip: 1,
    Angle: 1,
    Speed: 1
}