import pygame
from typing import Any
from math import floor
from random import shuffle, choice
import random
import utils.tween_module as TweenModule
from utils.ui.ui_sprite import UiSprite
from utils.ui.textbox import TextBox
from utils.ui.textsprite import TextSprite
from utils.ui.base_ui_elements import BaseUiElements
import utils.interpolation as interpolation
from utils.my_timer import Timer
from game.sprite import Sprite
from utils.helpers import average, random_float, get_drag_per_frame
from utils.ui.brightness_overlay import BrightnessOverlay
from utils.particle_effects import ParticleEffect

class GameState:
    def __init__(self, game_object : 'Game'):
        self.game = game_object

    def main_logic(self, delta : float):
        pass

    def pause(self):
        pass

    def unpause(self):
        pass

    def handle_key_event(self, event : pygame.Event):
        pass

    def handle_mouse_event(self, event : pygame.Event):
        pass

    def cleanup(self):
        pass

class NormalGameState(GameState):
    def main_logic(self, delta : float):
        Sprite.update_all_sprites(delta)
        Sprite.update_all_registered_classes(delta)

    def pause(self):
        if not self.game.active: return
        self.game.game_timer.pause()
        window_size = core_object.main_display.get_size()
        pause_ui1 = BrightnessOverlay(-60, pygame.Rect(0,0, *window_size), 0, 'pause_overlay', zindex=999)
        pause_ui2 = TextSprite(pygame.Vector2(window_size[0] // 2, window_size[1] // 2), 'center', 0, 'Paused', 'pause_text', None, None, 1000,
                               (self.game.font_70, 'White', False), ('Black', 2), colorkey=(0, 255, 0))
        core_object.main_ui.add(pause_ui1)
        core_object.main_ui.add(pause_ui2)
        self.game.state = PausedGameState(self.game, self)
    
    def handle_key_event(self, event : pygame.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.pause()

class TestGameState(NormalGameState):
    def __init__(self, game_object : 'Game'):
        self.game = game_object
        self.player : TestPlayer = TestPlayer.spawn(pygame.Vector2(random.randint(0, 960),random.randint(0, 540)))
        self.particle_effect : ParticleEffect = ParticleEffect.load_effect('test2', persistance=False)
        self.particle_effect.play(pygame.Vector2(480, 270), time_source=self.game.game_timer.get_time)
        game.test_player.make_connections()

    def main_logic(self, delta : float):
        super().main_logic(delta)
    
    def cleanup(self):
        game.test_player.remove_connections()

class RedButtonStage(NormalGameState):
    def __init__(self, game_object : 'Game'):
        self.game = game_object
    
    def main_logic(self, delta : float):
        super().main_logic(delta)
    
    def cleanup(self):
        super().cleanup()

class RedButtonStageStandby(RedButtonStage):
    def __init__(self, game_object : 'Game'):
        self.game : Game = game_object
        self.player : Player = Player.spawn(pygame.Vector2(480, 270))
        self.red_button : RedButton = RedButton.spawn(pygame.Vector2(480, 270))
        #StandardProjectile.spawn(pygame.Vector2(0,0), velocity=pygame.Vector2(10, 0).rotate(29.36), 
                                #accel=pygame.Vector2(0.005, 0.00).rotate(29.36), kill_offscreen=True, drag=get_drag_per_frame(0.5, 5))
        game.player.make_connections()
        game.red_button.make_connections()
    
    def main_logic(self, delta : float):
        super().main_logic(delta)
        if not self.red_button.rect.colliderect((0,0, *core_object.main_display.get_size())):
            self.switch_to_assault()
            self.red_button.kill_instance()

    def cleanup(self):
        game.player.remove_connections()
        game.red_button.remove_connections()
    
    def handle_mouse_event(self, event : pygame.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.red_button.rect.collidepoint(*event.pos) and (self.red_button.anchored):
                self.red_button.jump()
                print('hey')
    
    def switch_to_assault(self):
        self.game.state = RedButtonStageAssault(self.game, self)

class RedButtonStageAssault(RedButtonStage):
    def __init__(self, game_object : 'Game', previous : RedButtonStageStandby):
        self.game = game_object
        self.player : Player = previous.player
        self.curr_pattern = Patterns.TestPattern()
        self.curr_pattern.initialize(self.game.game_timer.get_time)
        print('attacking')
    
    def main_logic(self, delta : float):
        Sprite.update_all_sprites(delta)
        Sprite.update_all_registered_classes(delta)
        self.curr_pattern.process_frame()
        if self.curr_pattern.is_over: self.game.fire_gameover_event()
    
    def handle_mouse_event(self, event : pygame.Event):
        pass
    
    def cleanup(self):
        game.player.remove_connections()
        game.red_button.remove_connections()

class PausedGameState(GameState):
    def __init__(self, game_object : 'Game', previous : GameState):
        super().__init__(game_object)
        self.previous_state = previous
    
    def unpause(self):
        if not self.game.active: return
        self.game.game_timer.unpause()
        pause_ui1 = core_object.main_ui.get_sprite('pause_overlay')
        pause_ui2 = core_object.main_ui.get_sprite('pause_text')
        if pause_ui1: core_object.main_ui.remove(pause_ui1)
        if pause_ui2: core_object.main_ui.remove(pause_ui2)
        self.game.state = self.previous_state

    def handle_key_event(self, event : pygame.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.unpause()

def runtime_imports():
    global Game
    from game.game_module import Game
    global core_object
    from core.core import core_object

    #runtime imports for game classes
    global game, TestPlayer      
    import game.test_player
    from game.test_player import TestPlayer

    global Player
    import game.player
    from game.player import Player

    global RedButton
    import game.red_button
    from game.red_button import RedButton

    global BaseProjectile, StandardProjectile
    import game.projectiles
    from game.projectiles import BaseProjectile, StandardProjectile

    global AttackPattern, Patterns
    import game.attack_patterns
    from game.attack_patterns import AttackPattern, Patterns
    

    game.player.runtime_imports()
    game.red_button.runtime_imports()
    game.projectiles.runtime_imports()

class GameStates:
    NormalGameState = NormalGameState
    TestGameState = TestGameState
    PausedGameState = PausedGameState
    RedButtonStage = RedButtonStage
    RedButtonStageStandby = RedButtonStageStandby
    RedButtonStageAssault = RedButtonStageAssault