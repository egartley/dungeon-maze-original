##Authors: Cameron Gower, Evan Gartley
##Completion Date 10/30/22
##Purpose , create all the boosters for the dungeon maze game

from pygame import *
import pygame
import game
from os import *
class Booster:
    def __init__(self):
        self.increase = 0
        self.size = 14
        self.sprite = Surface((self.size, self.size))
        self.rect = self.sprite.get_rect()
        self.x = 0
        self.y = 0
        # see explaination for relative coords in maincharacter
        self.relative_x = 0
        self.relative_y = 0
        self.placed = False
        self.collision_set = False

    def booster_collision(self):
        pass

    def tick(self):
        self.rect = Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())

    def render(self, surface):
        surface.blit(self.sprite, (self.x, self.y))


class ArrowBooster(Booster):
    increase = 10
    
    def __init__(self):
        super().__init__()
        self.increase = 10
        self.sprite = image.load(path.join('src','sprites','Boosters','arrow.png'))
        self.sprite = transform.scale(self.sprite, (20,20))
        self.rect = self.sprite.get_rect()
        
    def booster_collision(self):
        game.GameEnvironment.PLAYER.apply_booster(self)


class SpeedBooster(Booster):
    increase = 1.5
    BOOSTERID = pygame.USEREVENT + 69
    def __init__(self):
        super().__init__()
        self.time = 15
        self.sprite = image.load(path.join('src','sprites','Boosters','speed.png'))
        self.sprite = transform.scale(self.sprite, (200,40))
        self.rect = self.sprite.get_rect()
        
        
    def booster_collision(self):
        game.GameEnvironment.PLAYER.apply_booster(self) 
        

class HealthBooster(Booster):
    BOOSTERID = 1000
    increase = 20
    def __init__(self):
        super().__init__()
        
        self.sprite = image.load(path.join('src','sprites','Boosters','health-booster.png'))
        self.sprite = transform.scale(self.sprite, (20,20))
        self.rect = self.sprite.get_rect()
        
    def booster_collision(self):
        game.GameEnvironment.PLAYER.apply_booster(self)
       

class ShieldBooster(Booster):
    increase = 20
    def __init__(self):
        super().__init__()
        
        self.sprite = image.load(path.join('src','sprites','Boosters','Shields.png'))
        self.sprite = transform.scale(self.sprite, (20,20))
        self.rect = self.sprite.get_rect()
        
    def booster_collision(self):
        game.GameEnvironment.PLAYER.apply_booster(self) 


class AttackBooster(Booster):
    increase = 10
    BOOSTERID = pygame.USEREVENT + 710
    def __init__(self):
        super().__init__()
        self.time = 30
        self.sprite = image.load(path.join('src','sprites','Boosters','attack.png'))
        self.sprite = transform.scale(self.sprite, (80,38))
        self.rect = self.sprite.get_rect()
        
    def booster_collision(self):
        game.GameEnvironment.PLAYER.apply_booster(self) 
