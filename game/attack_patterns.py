import pygame

from game.projectiles import BaseProjectile, StandardProjectile
from utils.my_timer import Timer, TimeSource
from typing import Callable, Generator, Any

CoroutineFunction = Callable[..., Generator]

class AttackPattern:
    def __init__(self, coroutine : CoroutineFunction|None = None):
        self.initialized : bool = False
        self.is_over : bool = False
        self.coro_func : CoroutineFunction = coroutine or self.corou
        self.coroutine : Generator = None
        self.coro_attributes : list[str] = []

    def type_hints(self):
        self.coro_attributes = []
    
    def initialize(self, *args, **kwargs):
        self.coroutine = self.coro_func(*args, **kwargs)
        next(self.coroutine)
        self.initialized = True

    def process_frame(self, values = None):
        if not self.initialized: self.initialize()
        try:
            return self.coroutine.send(values)
        except StopIteration as e:
            self.is_over = True
            return e.value
    
    def __getattr__(self, name : str):
        if name not in self.coro_attributes: raise AttributeError
        return self.coroutine.gi_frame.f_locals[name]
    
    @staticmethod
    def corou(*args, **kwargs) -> Generator:
        raise NotImplementedError

class TestPattern(AttackPattern):
    def initialize(self, time_source : TimeSource):
        return super().initialize(time_source)
    
    def type_hints(self):
        self.coro_attributes = ['timer', 'cooldown', 'curr_angle']
        self.timer : Timer
        self.cooldown : Timer
        self.curr_angle : float
    
    @staticmethod
    def corou(time_source : TimeSource) -> Generator[None, None, str]:
        timer : Timer = Timer(5, time_source)
        cooldown : Timer = Timer(0.1, time_source)
        curr_angle : float = 0
        yield
        while not timer.isover():
            if cooldown.isover():
                cooldown.restart()
                curr_angle = pygame.math.lerp(0, 360, timer.get_time() / timer.duration)
                StandardProjectile.spawn(pygame.Vector2(0, -270).rotate(-curr_angle) + (480, 270), velocity=pygame.Vector2(0, 10).rotate(-curr_angle))
            yield
        timer.set_duration(3, restart=True)
        while not timer.isover():
            yield
        return 'Done'

class Patterns:
    TestPattern = TestPattern