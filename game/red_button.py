import pygame
from game.sprite import Sprite
from core.core import core_object

from utils.helpers import load_alpha_to_colorkey

class RedButton(Sprite):
    active_elements : list['RedButton'] = []
    inactive_elements : list['RedButton'] = []
    linked_classes : list['Sprite'] = [Sprite]
    SCALE_FACTOR = 2
    unpressed_image : pygame.Surface = pygame.transform.scale_by(
        load_alpha_to_colorkey('assets/graphics/red_button_stage/red_button_unpressed_final.png', (0, 255, 0)), SCALE_FACTOR)
    pressed_image : pygame.Surface = pygame.transform.scale_by(
    load_alpha_to_colorkey('assets/graphics/red_button_stage/red_button_pressed_final.png', (0, 255, 0)), SCALE_FACTOR)
    bounding_box : pygame.Rect = pygame.Rect(0,0, *core_object.main_display.get_size())
    def __init__(self):
        super().__init__()
        self.pressed : bool
        self.velocity : pygame.Vector2
        self.accel : pygame.Vector2
        self.anchored : bool = False
        RedButton.inactive_elements.append(self)
    
    @classmethod
    def spawn(cls, pos : pygame.Vector2):
        element = cls.inactive_elements[0]

        element.image = cls.unpressed_image
        element.rect = element.image.get_rect()
        element.position = pos
        element.align_rect()
        element.zindex = -5
        element.pressed = False
        element.velocity = pygame.Vector2()
        element.accel = pygame.Vector2()

        cls.unpool(element)
        return element
    
    def do_movement(self, delta : float):
        self.velocity += self.accel * 0.5 * delta
        self.position += self.velocity * delta
        self.velocity += self.accel * 0.5 * delta
    
    def update(self, delta : float):
        if self.pressed:
            if (not self.rect.collidepoint(*pygame.mouse.get_pos())) or (not pygame.mouse.get_pressed()[0]):
                self.unpress()
        if not self.anchored:
            self.do_movement(delta)
        if not self.rect.colliderect(self.bounding_box):
            self.kill_instance_safe()
    
    def press(self):
        self.pressed = True
        if self.image != self.pressed_image:
            self.image = self.pressed_image
            self.rect = self.image.get_rect()
            self.align_rect()

    
    def unpress(self):
        self.pressed = False
        if self.image != self.unpressed_image:
            self.image = self.unpressed_image
            self.rect = self.image.get_rect()
            self.align_rect()
    
    def jump(self):
        self.anchored = False
        self.velocity = pygame.Vector2(0, -12)
        self.accel = pygame.Vector2(0,38 / 60)
    
    def handle_mouse_event(self, event : pygame.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*event.pos):
                self.press()

    def clean_instance(self):
        super().clean_instance()
        self.pressed = None
        self.velocity = None
        self.accel = None
        self.anchored = None
    
    @classmethod
    def receive_event(cls, event : pygame.Event):
        for element in cls.active_elements:
            if event.type in {pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION}:
                element.handle_mouse_event(event)


RedButton()
Sprite.register_class(RedButton)

def runtime_imports():
    global game, Player
    import game.player
    from game.player import Player

def make_connections():
    for event_type in {pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.KEYDOWN, pygame.KEYUP, 
                       pygame.FINGERUP, pygame.FINGERDOWN, pygame.FINGERMOTION}:
        core_object.event_manager.bind(event_type, RedButton.receive_event)

def remove_connections():
    for event_type in {pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.KEYDOWN, pygame.KEYUP, 
                       pygame.FINGERUP, pygame.FINGERDOWN, pygame.FINGERMOTION}:
        core_object.event_manager.unbind(event_type, RedButton.receive_event)