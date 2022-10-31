import py
import pygame
from os import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
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
        self.is_animating = False
        self.current_sprite = 0
        self.sprites_right_swing = []
        self.sprites_left_swing = []
        self.right_animation()
        self.left_animation()
        self.image = self.sprites_right_swing[self.current_sprite]
        self.rect = self.image.get_rect()
        self.direction = None


    def directionSprite(self, x, y, direction):
        if direction == "right":
            self.image = self.sprites_right_swing[0]
            self.rect = self.image.get_rect()
            self.rect.topleft = [x, y]
        elif direction == "left":
            self.image = self.sprites_left_swing[0]
            self.rect = self.image.get_rect()
            self.rect.topleft = [x, y]

    def right_animation(self):
        self.sprites_right_swing.append(pygame.image.load('sprite_swing_sword_right0.png'))
        self.sprites_right_swing.append(pygame.image.load('sprite_swing_sword_right1.png'))
        self.sprites_right_swing.append(pygame.image.load('sprite_swing_sword_right2.png'))
        self.sprites_right_swing.append(pygame.image.load('sprite_swing_sword_right3.png'))
        self.sprites_right_swing.append(pygame.image.load('sprite_swing_sword_right4.png'))
        self.sprites_right_swing[0] = pygame.transform.scale(self.sprites_right_swing[0], (100,100))
        self.sprites_right_swing[1] = pygame.transform.scale(self.sprites_right_swing[1], (100,100))
        self.sprites_right_swing[2] = pygame.transform.scale(self.sprites_right_swing[2], (100,100))
        self.sprites_right_swing[3] = pygame.transform.scale(self.sprites_right_swing[3], (100,100))
        self.sprites_right_swing[4] = pygame.transform.scale(self.sprites_right_swing[4], (100,100))

    def left_animation(self):
        self.sprites_left_swing.append(pygame.image.load('sprite_swing_sword_left0.png'))
        self.sprites_left_swing.append(pygame.image.load('sprite_swing_sword_left1.png'))
        self.sprites_left_swing.append(pygame.image.load('sprite_swing_sword_left2.png'))
        self.sprites_left_swing.append(pygame.image.load('sprite_swing_sword_left3.png'))
        self.sprites_left_swing.append(pygame.image.load('sprite_swing_sword_left4.png'))
        self.sprites_left_swing[0] = pygame.transform.scale(self.sprites_left_swing[0], (100,100))
        self.sprites_left_swing[1] = pygame.transform.scale(self.sprites_left_swing[1], (100,100))
        self.sprites_left_swing[2] = pygame.transform.scale(self.sprites_left_swing[2], (100,100))
        self.sprites_left_swing[3] = pygame.transform.scale(self.sprites_left_swing[3], (100,100))
        self.sprites_left_swing[4] = pygame.transform.scale(self.sprites_left_swing[4], (100,100))

    def render(self, surface, x, y, direction):
        if self.in_cooldown == True and self.is_animating == True:
            if self.current_sprite >= len(self.sprites_right_swing):
                self.current_sprite = 0
                self.is_animating = False
            if direction == "right":
                self.image = self.sprites_right_swing[int(self.current_sprite)]
                self.rect = self.image.get_rect()
                self.rect.topleft = [x, y]
                self.current_sprite += 0.5
            elif direction == "left":
                self.image = self.sprites_left_swing[int(self.current_sprite)]
                self.rect = self.image.get_rect()
                self.rect.topleft = [x, y]
                self.current_sprite += 0.5


class Bow(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = 15
