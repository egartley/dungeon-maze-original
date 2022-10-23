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
        #self.sprites.append(pygame.image.load(path.join('src','SwingSwordSplash1.png')))
        self.sprites.append(pygame.image.load(path.join('src','SwingSplash.png')))
        self.sprites[0] = pygame.transform.scale(self.sprites[0], (58,80))
        #self.sprites.append(pygame.image.load(path.join('src','SwingSwordSplash2.png')))
        #self.sprites.append(pygame.image.load(path.join('src','SwordSwing01.png')))
        #self.sprites.append(pygame.image.load(path.join('src','SwordSwing02.png')))
        #self.sprites.append(pygame.image.load(path.join('src','SwordSwing03.png')))
        #self.sprites.append(pygame.image.load(path.join('src','SwordSwing04.png')))
        #self.sprites.append(pygame.image.load(path.join('src','SwordSwing05.png')))
        #self.sprites.append(pygame.image.load(path.join('src','SwordSwing06.png')))
        #self.sprites.append(pygame.image.load(path.join('src','SwordSwing07.png')))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.is_animating = False

    def render(self, surface, x, y):
        if self.in_cooldown == True and self.is_animating == True:
            if self.current_sprite >= len(self.sprites)-1:
                self.current_sprite = 0
                self.is_animating = False
            self.rect.topleft = [x,y]
            surface.blit(self.image, (x, y))
            self.current_sprite += 0.05
            self.image = self.sprites[int(self.current_sprite)]
            print('Speed ' + str(self.current_sprite))


class Bow(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = 15
