import pygame
from game.sprite import Sprite
from core.core import core_object

from utils.animation import Animation
from utils.pivot_2d import Pivot2D
from typing import Literal
from utils.helpers import load_alpha_to_colorkey

import game.red_button
from game.red_button import RedButton

class Player(Sprite):
    active_elements : list['Player'] = []
    inactive_elements : list['Player'] = []
    linked_classes : list['Sprite'] = [Sprite]
    '''
    diameter = 24
    outline : int = 1
    
    IMAGE_SIZE = (diameter + outline * 2, diameter + outline * 2)
    print(IMAGE_SIZE)
    test_image : pygame.Surface = pygame.surface.Surface(IMAGE_SIZE)
    test_image.set_colorkey((97, 255, 34))
    test_image.fill((97, 255, 34))
    pygame.draw.circle(test_image, "Black", (IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 2), diameter // 2 + outline)
    pygame.draw.circle(test_image, "Red", (IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 2), diameter // 2)
    '''
    test_image : pygame.Surface = load_alpha_to_colorkey('assets/graphics/player/main_player.png', (0, 255, 0))
    def __init__(self) -> None:
        super().__init__()
        self.control_method : Literal['keyboard', 'mouse']
        Player.inactive_elements.append(self)

    @classmethod
    def spawn(cls, new_pos : pygame.Vector2, control_method : Literal['keyboard', 'mouse'] = 'mouse'):
        element = cls.inactive_elements[0]

        element.image = cls.test_image
        element.rect = element.image.get_rect()
        element.position = new_pos
        element.align_rect()
        element.zindex = 0

        element.control_method = control_method
        cls.unpool(element)
        return element
    
    def update(self, delta: float):
        if self.control_method == 'keyboard':
            keyboard_map = pygame.key.get_pressed()
            move_vector : pygame.Vector2 = pygame.Vector2(0,0)
            speed : int = 5
            if keyboard_map[pygame.K_a]:
                move_vector += pygame.Vector2(-1, 0)
            if keyboard_map[pygame.K_d]:
                move_vector += pygame.Vector2(1, 0)
            if keyboard_map[pygame.K_s]:
                move_vector += pygame.Vector2(0, 1)
            if keyboard_map[pygame.K_w]:
                move_vector += pygame.Vector2(0, -1)
            if keyboard_map[pygame.K_e]:
                self.angle += 5 * delta
            if keyboard_map[pygame.K_q]:
                self.angle -= 5 * delta
            if move_vector.magnitude(): move_vector.normalize()
            self.position += move_vector * speed * delta
        elif self.control_method == 'mouse':
            self.max_follow_speed : int|None = None
            mouse_pos : pygame.Vector2 = pygame.Vector2(pygame.mouse.get_pos())
            if not self.max_follow_speed:
                self.position = mouse_pos
            else:
                vec_to_mouse : pygame.Vector2 = mouse_pos - self.position
                distance_to_mouse : float = vec_to_mouse.magnitude()
                if distance_to_mouse > self.max_follow_speed * delta:
                    self.position += vec_to_mouse.normalize() * self.max_follow_speed * delta
                else:
                    self.position = mouse_pos
        self.clamp_rect(pygame.Rect(0,0, *core_object.main_display.get_size()))
    
    def handle_mouse_event(self, event : pygame.Event):
        pass

    def handle_key_event(self, event : pygame.Event):
        pass

    def handle_touch_event(self, event : pygame.Event):
        pass
    
    def clean_instance(self):
        super().clean_instance()
        self.control_method = None
    
    
    @classmethod
    def receive_event(cls, event : pygame.Event):
        for element in cls.active_elements:
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                element.handle_mouse_event(event)
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                element.handle_key_event(event)
            elif event.type in (pygame.FINGERDOWN, pygame.FINGERMOTION, pygame.FINGERUP):
                element.handle_touch_event(event)
        

Player()
Sprite.register_class(Player)


def runtime_imports():
    pass

def make_connections():
    core_object.event_manager.bind(pygame.MOUSEBUTTONDOWN, Player.receive_event)
    core_object.event_manager.bind(pygame.MOUSEBUTTONUP, Player.receive_event)
    core_object.event_manager.bind(pygame.MOUSEMOTION, Player.receive_event)

    core_object.event_manager.bind(pygame.KEYDOWN, Player.receive_event)
    core_object.event_manager.bind(pygame.KEYUP, Player.receive_event)

    core_object.event_manager.bind(pygame.FINGERUP, Player.receive_event)
    core_object.event_manager.bind(pygame.FINGERDOWN, Player.receive_event)
    core_object.event_manager.bind(pygame.FINGERMOTION, Player.receive_event)

def remove_connections():
    core_object.event_manager.unbind(pygame.MOUSEBUTTONDOWN, Player.receive_event)
    core_object.event_manager.unbind(pygame.MOUSEBUTTONUP, Player.receive_event)
    core_object.event_manager.unbind(pygame.MOUSEMOTION, Player.receive_event)

    core_object.event_manager.unbind(pygame.KEYDOWN, Player.receive_event)
    core_object.event_manager.unbind(pygame.KEYUP, Player.receive_event)

    core_object.event_manager.unbind(pygame.FINGERUP, Player.receive_event)
    core_object.event_manager.unbind(pygame.FINGERDOWN, Player.receive_event)
    core_object.event_manager.unbind(pygame.FINGERMOTION, Player.receive_event)