import py
import pygame
from os import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        self.damage = 0
        self.sprite = None
        self.cooldown = 0
        self.in_cooldown = False
        self.range = 0


class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = 10
        self.cooldown = 1
        self.range = 8
        self.animation()


    def animation(self):
        self.sprites = []
        self.sprites.append(pygame.image.load(path.join('src','sprite_swing_sword0.png')))
        self.sprites.append(pygame.image.load(path.join('src','sprite_swing_sword1.png')))
        self.sprites.append(pygame.image.load(path.join('src','sprite_swing_sword2.png')))
        self.sprites.append(pygame.image.load(path.join('src','sprite_swing_sword3.png')))
        self.sprites.append(pygame.image.load(path.join('src','sprite_swing_sword4.png')))
        self.sprites[0] = pygame.transform.scale(self.sprites[0], (100,100))
        self.sprites[1] = pygame.transform.scale(self.sprites[1], (100,100))
        self.sprites[2] = pygame.transform.scale(self.sprites[2], (100,100))
        self.sprites[3] = pygame.transform.scale(self.sprites[3], (100,100))
        self.sprites[4] = pygame.transform.scale(self.sprites[4], (100,100))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.is_animating = False

    def render(self, surface, x, y):
        if self.in_cooldown == True and self.is_animating == True:
            if self.current_sprite >= len(self.sprites)-1:
                self.current_sprite = 0
                self.is_animating = False
            surface.blit(self.image, (x-30, y-20))
            self.current_sprite += 0.5
            self.image = self.sprites[int(self.current_sprite)]
            print('Speed ' + str(self.current_sprite))


class Bow(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = 15
