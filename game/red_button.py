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

    def __init__(self):
        super().__init__()
        RedButton.inactive_elements.append(self)
    
    @classmethod
    def spawn(cls, pos : pygame.Vector2):
        element = cls.inactive_elements[0]

        element.image = cls.unpressed_image
        element.rect = element.image.get_rect()
        element.position = pos
        element.align_rect()
        element.zindex = -5

        cls.unpool(element)
        return element
    
    def update(self, delta : float):
        current_player : Player = Player.active_elements[0] if Player.active_elements else None
        if not current_player: return
        curr_image : pygame.Surface = self.image
        if current_player.is_collding_rect(self):
            self.image = self.pressed_image
        else:
            self.image = self.unpressed_image
        if curr_image != self.image:
            self.rect = self.image.get_rect()
            self.align_rect()
    
    def clean_instance(self):
        super().clean_instance()

RedButton()
Sprite.register_class(RedButton)

def runtime_imports():
    global game, Player
    import game.player
    from game.player import Player

def make_connections():
    pass

def remove_connections():
    pass