import pygame
from game.sprite import Sprite
from core.core import core_object

from utils.helpers import load_alpha_to_colorkey
from utils.my_timer import Timer

class BaseProjectile(Sprite):
    active_elements : list['BaseProjectile'] = []
    inactive_elements : list['BaseProjectile'] = []
    linked_classes : list['Sprite'] = [Sprite]
    
    test_radius : int = 8
    test_image : pygame.Surface = pygame.surface.Surface((test_radius * 2, test_radius * 2))
    test_image.set_colorkey((0, 255, 0))
    test_image.fill((0, 255, 0))
    pygame.draw.circle(test_image, "Red", (test_radius, test_radius), test_radius)

    bounding_box = pygame.Rect(0, 0, *core_object.main_display.get_size())

    def __init__(self):
        super().__init__()
        self.velocity : pygame.Vector2
        self.acceleration : pygame.Vector2
        self.drag : float
        self.lifetime_timer : Timer
        self.kill_offscreen : bool
        self.was_onscreen : bool
        BaseProjectile.inactive_elements.append(self)
    
    @classmethod
    def spawn(cls,  pos : pygame.Vector2, surf : pygame.Vector2|None = None, velocity : pygame.Vector2|None = None, 
              accel : pygame.Vector2|None = None, drag : float = 0, lifetime : float = -1, kill_offscreen : bool = True):
        element = cls.inactive_elements[0]

        element.image = surf or cls.test_image
        element.rect = element.image.get_rect()
        element.position = pos
        element.align_rect()
        element.zindex = 0

        element.velocity = velocity or pygame.Vector2(0,0)
        element.acceleration = accel or pygame.Vector2(0,0)
        element.drag = drag
        element.lifetime_timer = Timer(lifetime, time_source=core_object.game.game_timer.get_time)


        element.kill_offscreen = kill_offscreen
        element.was_onscreen = False
        
        element.check_bounding()
        cls.unpool(element)
        return element
    
    def do_movement(self, delta : float):
        self.velocity *=  ((1 - self.drag) ** delta) ** 0.5

        self.velocity += self.acceleration * 0.5 * delta
        self.position += self.velocity * delta
        self.velocity += self.acceleration * 0.5 * delta

        self.velocity *=  ((1 - self.drag) ** delta) ** 0.5
        self.rect.center = self.position

    def update(self, delta : float):
        self.do_movement()
        if self.rect.colliderect(self.bounding_box):
            self.was_onscreen = True
    
    def check_bounding(self):
        onscreen : bool = self.rect.colliderect(self.bounding_box)
        if onscreen:
            self.was_onscreen = True
        else:
            if self.was_onscreen and self.kill_offscreen:
                self.kill_instance_safe()
    
    def clean_instance(self):
        super().clean_instance()
        self.velocity = None
        self.acceleration = None
        self.drag = None
        self.lifetime_timer = None
        self.kill_offscreen = None
        self.was_onscreen = None


class StandardProjectile(BaseProjectile):
    active_elements : list['StandardProjectile'] = []
    inactive_elements : list['StandardProjectile'] = []
    linked_classes : list['Sprite'] = [Sprite, BaseProjectile]

    def __init__(self):
        super().__init__()
        StandardProjectile.inactive_elements.append(self)
    
    @classmethod
    def spawn(cls, pos : pygame.Vector2, surf : pygame.Vector2|None = None, velocity : pygame.Vector2|None = None, 
              accel : pygame.Vector2|None = None, drag : float = 0, lifetime : float = -1, kill_offscreen : bool = True):
        element = cls.inactive_elements[0]

        element.image = surf or cls.test_image
        element.rect = element.image.get_rect()
        element.position = pos
        element.align_rect()
        element.zindex = 0

        element.velocity = velocity or pygame.Vector2(0,0)
        element.acceleration = accel or pygame.Vector2(0,0)
        element.drag = drag
        element.lifetime_timer = Timer(lifetime, time_source=core_object.game.game_timer.get_time)


        element.kill_offscreen = kill_offscreen
        element.was_onscreen = False
        
        element.check_bounding()
        cls.unpool(element)
        return element
    
    def update(self, delta : float):
        super().update(delta)
    
    def clean_instance(self):
        super().clean_instance()

for _ in range(100):
    StandardProjectile()

Sprite.register_class(BaseProjectile)
Sprite.register_class(StandardProjectile)

def runtime_imports():
    global game, Player
    import game.player
    from game.player import Player

def make_connections():
    pass

def remove_connections():
    pass