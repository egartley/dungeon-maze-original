import py
import screen
import pygame
import math
from os import *


class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, target_x, target_y):
        super().__init__()
        self.picture = pygame.image.load(path.join('src','arrow.png'))
        self.picture = pygame.transform.scale(self.picture, (50,50))
        self.picture = pygame.transform.rotate(self.picture, 225)
        self.rect = self.picture.get_rect(topleft = (pos_x, pos_y))
        self.angle = math.atan2(target_y - pos_y, target_x - pos_x)
        self.velx = math.cos(self.angle) * 20
        self.vely = math.sin(self.angle) * 20
        self.x = pos_x
        self.y = pos_y

    def update(self):
        self.image = pygame.transform.rotate(self.picture, 360-self.angle*57.29)
        self.x += int(self.velx)
        self.y += int(self.vely)
        self.rect.x = int(self.x - self.image.get_rect().width/2)
        self.rect.y = int(self.y - self.image.get_rect().height/2)
        if self.rect.x >= screen.frame_size_x + 100 or self.rect.x <= -100 or \
            self.rect.y >= screen.frame_size_y + 100 or self.rect.y <= -100:
            self.kill()