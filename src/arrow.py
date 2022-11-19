import py
import screen
import pygame
import math
import maze
from os import *


class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, target_x, target_y):
        super().__init__()
        self.picture = pygame.image.load('src/sprites/Boosters/arrow.png')
        self.picture = pygame.transform.scale(self.picture, (50,50))
        self.picture = pygame.transform.rotate(self.picture, 225)
        self.rect = self.picture.get_rect(topleft = (pos_x, pos_y))
        self.angle = math.atan2(target_y - pos_y, target_x - pos_x)
        self.velx = math.cos(self.angle) * 20
        self.vely = math.sin(self.angle) * 20
        self.x = pos_x
        self.y = pos_y
        self.relative_x = 0
        self.relative_y = 0

    def update(self):
        self.image = pygame.transform.rotate(self.picture, 360-self.angle*57.29)
        self.x += int(self.velx)
        self.y += int(self.vely)
        self.rect.x = int(self.x - self.image.get_rect().width/2)
        self.rect.y = int(self.y - self.image.get_rect().height/2)
        if self.rect.x >= screen.frame_size_x + 100 or self.rect.x <= -100 or \
            self.rect.y >= screen.frame_size_y + 100 or self.rect.y <= -100:
            self.kill()

        self.relative_x = self.x - maze.MazeEnvironment.MAP_X
        self.relative_y = self.y - maze.MazeEnvironment.MAP_Y

        if self.check_wall(self.relative_x - 20, self.relative_y - 20):
            self.self_destruct()


    def check_wall(self, x, y):
        # check if there is a wall at the given x/y
        r = int(y // maze.MazeEnvironment.TILE_SIZE)
        c = int(x // maze.MazeEnvironment.TILE_SIZE)
        if r >= len(maze.MazeEnvironment.MAZE.grid) or c >= len(maze.MazeEnvironment.MAZE.grid[0]):
            return True
        return maze.MazeEnvironment.MAZE.grid[r][c] == maze.MazeEnvironment.WALL

    def self_destruct(self):
        self.kill()