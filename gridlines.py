from random import randint, choices

from utils import *
from constants import *
from points import Points
from barrier_powers import barrier_powers
from effects import Particle, Shockwave

class HorizontalGridline(Sprite):
    instances = {}

    @classmethod
    def tick(cls, player, dt, screen):
        on_screen_lines = set()
        for y in range(int(player.pos.y / GRID_SPACE.y - WIDTH / GRID_SPACE.y / 2 - 1), int(player.pos.y / GRID_SPACE.y + WIDTH / GRID_SPACE.y / 2 + 2)):
            on_screen_lines.add(y)
            if y not in cls.instances:
                cls(player, y)
        for y, line in cls.instances.copy().items():
            if y in on_screen_lines:
                line.update(dt)
                line.draw(screen)
            else:
                del cls.instances[y]

    def __init__(self, player, y):
        __class__.instances[y] = self
        self.player = player
        self.y = y
        for _ in range(randint(1, 3)):
            Points(self.player, randint(-10, 10), (GRID_SPACE.x * randint(int(self.player.pos.x / GRID_SPACE.x - HEIGHT / GRID_SPACE.x - 10), int(self.player.pos.x / GRID_SPACE.x + HEIGHT / GRID_SPACE.x + 10)), GRID_SPACE.y * self.y))

    def update(self, dt):
        self.on_screen_start = VEC(0, self.y * GRID_SPACE.y - self.player.camera.offset.y)
        self.on_screen_end = VEC(WIDTH, self.y * GRID_SPACE.y - self.player.camera.offset.y)

    def draw(self, screen):
        pygame.draw.line(screen, (150, 150, 150), self.on_screen_start, self.on_screen_end)

class VerticalGridline(Sprite):
    instances = {}

    @classmethod
    def tick(cls, player, dt, screen):
        on_screen_lines = set()
        for x in range(int(player.pos.x / GRID_SPACE.x - WIDTH / GRID_SPACE.x / 2 - 1), int(player.pos.x / GRID_SPACE.x + WIDTH / GRID_SPACE.x / 2 + 2)):
            on_screen_lines.add(x)
            if x not in cls.instances:
                cls(player, x)
                if randint(0, 24) == 0 and not Barrier.instance:
                    Barrier(player, x, choices(list(barrier_powers.keys()), list(barrier_powers.values()))[0])
        for x, line in cls.instances.copy().items():
            if x in on_screen_lines:
                line.update(dt)
                line.draw(screen)
            else:
                del cls.instances[x]

    def __init__(self, player, x):
        __class__.instances[x] = self
        self.player = player
        self.x = x
        for _ in range(randint(1, 4)):
            Points(self.player, randint(-10, 10), (GRID_SPACE.x * self.x, GRID_SPACE.y * randint(int(self.player.pos.y / GRID_SPACE.y - HEIGHT / GRID_SPACE.y / 2 - 10), int(self.player.pos.y / GRID_SPACE.y + HEIGHT / GRID_SPACE.y / 2 + 10))))
        self.on_screen_start = VEC(0, 0)
        self.on_screen_end = VEC(0, 0)

    def update(self, dt):
        self.on_screen_start = VEC(self.x * GRID_SPACE.x - self.player.camera.offset.x, 0)
        self.on_screen_end = VEC(self.x * GRID_SPACE.x - self.player.camera.offset.x, HEIGHT)
        if self.on_screen_start.x < -100:
            del __class__.instances[self.x]
            del self

    def draw(self, screen):
        pygame.draw.line(screen, (150, 150, 150), self.on_screen_start, self.on_screen_end)

class Barrier(VerticalGridline):
    instance = None

    @classmethod
    def tick(cls, dt, screen):
        if cls.instance:
            cls.instance.update(dt)
        if cls.instance:
            cls.instance.draw(screen)

    def __init__(self, player, x, power):
        self.__class__.instance = self
        self.player = player
        self.x = x
        self.power = power

    def update(self, dt):
        if self.x * GRID_SPACE.x < self.player.pos.x < self.x * GRID_SPACE.x + 25:
            self.power(player=self.player)
            for _ in range(400):
                Particle(self.player, (self.x * GRID_SPACE.x, randint(self.on_screen_start.y - 100, self.on_screen_end.y + 100) + self.player.camera.offset.y), (180, 180, 180))
            Shockwave(self.player, self.player.pos, (180, 180, 180), 10, 160, 14)
            self.__class__.instance = None
            del self
            return
        if self.x * GRID_SPACE.x < -100:
            self.__class__.instance = None
            del self
            return
        super().update(dt)

    def draw(self, screen):
        pygame.draw.line(screen, (180, 180, 180), self.on_screen_start, self.on_screen_end, 4)