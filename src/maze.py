import random
import character
from booster import *
from mazelib import Maze
from mazelib.generate.Prims import Prims
import pygame

class MazeEnvironment:
    TILE_SIZE = 500
    MAP_X = 0
    MAP_Y = 0
    SPEED = 4
    PIXEL_WIDTH = 0
    PIXEL_HEIGHT = 0
    ROOM = 0
    WALL = 1
    START = 2
    END = 3

    MAZE = Maze()

    # whether the map (not player!) can move in the direction
    CAN_MOVE_UP = False
    CAN_MOVE_DOWN = False
    CAN_MOVE_LEFT = False
    CAN_MOVE_RIGHT = False

    def __init__(self, game_env):
        MazeEnvironment.maze = Maze()
        self.size = ()
        self.game_environment = game_env
        self.difficulty = 0
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.floor_surface = pygame.image.load("src/sprites/maze/floor.png")
        self.corner_surface = pygame.image.load("src/sprites/maze/corner.png")
        walls = ["0001", "0010", "0011", "0100", "0110", "0111", "1000", "1001", "1011", "1100", "1101", "1110", "1010", "0101"]
        self.wall_surfaces = []
        for i in range(0, len(walls)):
            self.wall_surfaces.append((walls[i], pygame.image.load("src/sprites/maze/" + walls[i] + ".png")))
        self.calculated_walls = []
        self.corners = []

    def generate_maze(self, rows, columns, difficulty):
        self.difficulty = difficulty
        self.size = (rows, columns)
        m = Maze()
        # difficulty currently has no effect
        m.generator = Prims(self.size[0], self.size[1])
        m.generate()
        m.generate_entrances()
        s = m.start
        e = m.end
        m.grid[s[0]][s[1]] = MazeEnvironment.START
        m.grid[e[0]][e[1]] = MazeEnvironment.END
        MazeEnvironment.MAZE = m
        MazeEnvironment.PIXEL_WIDTH = len(MazeEnvironment.MAZE.grid[0]) * MazeEnvironment.TILE_SIZE
        MazeEnvironment.PIXEL_HEIGHT = len(MazeEnvironment.MAZE.grid) * MazeEnvironment.TILE_SIZE
        self.floor_surface.convert()
        self.corner_surface.convert()
        for i in range(0, len(self.wall_surfaces)):
            self.wall_surfaces[i][1].convert()
        self.calculate_walls()
        self.calculate_corners()

    def calculate_walls(self):
        grid = MazeEnvironment.MAZE.grid
        numstring = ""
        for i in range(len(grid)):
            s = ""
            for j in range(len(grid[0])):
                s += str(grid[i][j])
            print(s)
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if not grid[i][j] == MazeEnvironment.WALL:
                    continue
                numstring += "1" if j - 1 >= 0 and not grid[i][j - 1] == MazeEnvironment.WALL else "0"
                numstring += "1" if i - 1 >= 0 and not grid[i - 1][j] == MazeEnvironment.WALL else "0"
                numstring += "1" if j + 1 < len(grid[i]) and not grid[i][j + 1] == MazeEnvironment.WALL else "0"
                numstring += "1" if i + 1 < len(grid) and not grid[i + 1][j] == MazeEnvironment.WALL else "0"
                for w in range(0, len(self.wall_surfaces)):
                    if numstring == self.wall_surfaces[w][0]:
                        self.calculated_walls.append(([i, j], self.wall_surfaces[w][1]))
                        print(str(i) + ", " + str(j) + ": " + numstring)
                numstring = ""

    def calculate_corners(self):
        grid = MazeEnvironment.MAZE.grid
        num = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if not grid[i][j] == MazeEnvironment.WALL:
                    continue
                if j - 1 >= 0 and grid[i][j - 1] == MazeEnvironment.WALL and i - 1 >= 0 and grid[i - 1][j] == MazeEnvironment.WALL:
                    num = 1
                elif j + 1 < len(grid[i]) and grid[i][j + 1] == MazeEnvironment.WALL and i - 1 >= 0 and grid[i - 1][j] == MazeEnvironment.WALL:
                    num = 2
                elif j + 1 < len(grid[i]) and grid[i][j + 1] == MazeEnvironment.WALL and i + 1 < len(grid) and grid[i + 1][j] == MazeEnvironment.WALL:
                    num = 3
                elif j - 1 >= 0 and grid[i][j - 1] == MazeEnvironment.WALL and i + 1 < len(grid) and grid[i + 1][j] == MazeEnvironment.WALL:
                    num = 4
                if not num == 0:
                    #print([i, j])
                    #print(num)
                    self.corners.append(([i, j], num))
                num = 0

    def generate_boosters(self):
        # generate boosters in each room with a 50% chance, and equally likely to be each type
        r = random.Random()
        rooms = []
        grid = MazeEnvironment.MAZE.grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == MazeEnvironment.ROOM:
                    x = r.randint(1, 100)
                    if x <= 50:
                        rooms.append((i, j))
        for room in rooms:
            x = r.randint(1, 5)
            if x == 1:
                self.game_environment.boosters.append((ArrowBooster(), room[0], room[1]))
            elif x == 2:
                self.game_environment.boosters.append((SpeedBooster(), room[0], room[1]))
            elif x == 3:
                self.game_environment.boosters.append((HealthBooster(), room[0], room[1]))
            elif x == 4:
                self.game_environment.boosters.append((ShieldBooster(), room[0], room[1]))
            else:
                self.game_environment.boosters.append((AttackBooster(), room[0], room[1]))

    def place_boosters(self):
        # do all the yucky math for determining where to actually render the boosters based on their generation
        r = random.Random()
        for b in self.game_environment.boosters:
            booster = b[0]
            row = b[1]
            col = b[2]
            x_offset = r.randint(12, MazeEnvironment.TILE_SIZE - booster.sprite.get_width() - 12)
            y_offset = r.randint(12, MazeEnvironment.TILE_SIZE - booster.sprite.get_width() - 12)
            booster.relative_x = MazeEnvironment.TILE_SIZE * col + x_offset
            booster.relative_y = MazeEnvironment.TILE_SIZE * row + y_offset
            booster.x = booster.relative_x + MazeEnvironment.MAP_X
            booster.y = booster.relative_y + MazeEnvironment.MAP_Y
            booster.rect = pygame.Rect(booster.x, booster.y, booster.size, booster.size)

    def remove_booster(self, booster):
        for b in self.game_environment.boosters:
            if b[0] == booster:
                self.game_environment.boosters.remove(b)
                return

    def generate_enemies(self):
        # difficulty currently has no effect here
        r = random.Random()
        rooms = []
        grid = MazeEnvironment.MAZE.grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == MazeEnvironment.ROOM:
                    x = r.randint(1, 100)
                    if x <= 50:
                        rooms.append((i, j))
        for room in rooms:
            e = character.Enemy()
            if r.randint(1, 100) <= 50:
                e.direction = character.Enemy.RIGHT
            self.game_environment.enemies.append((e, room[0], room[1]))

    def place_enemies(self):
        # do all the yucky math for determing where to actually render the enemies based on their generation
        r = random.Random()
        for e in self.game_environment.enemies:
            enemy = e[0]
            row = e[1]
            col = e[2]
            x_offset = r.randint(12, MazeEnvironment.TILE_SIZE - enemy.width - 12)
            y_offset = r.randint(12, MazeEnvironment.TILE_SIZE - enemy.height - 12)
            enemy.relative_x = MazeEnvironment.TILE_SIZE * col + x_offset
            enemy.relative_y = MazeEnvironment.TILE_SIZE * row + y_offset
            enemy.x = enemy.relative_x + MazeEnvironment.MAP_X
            enemy.y = enemy.relative_y + MazeEnvironment.MAP_Y
            enemy.rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

    def remove_enemy(self, enemy):
        for e in self.game_environment.enemies:
            if e[0] == enemy:
                self.game_environment.enemies.remove(e)
                return

    def get_player_pos(self, r, c):
        # get the player's tile position (ex. 0, 0 is top left)
        return MazeEnvironment.TILE_SIZE * r + (MazeEnvironment.TILE_SIZE / 2 - game.GameEnvironment.PLAYER.width / 2), \
               MazeEnvironment.TILE_SIZE * c + (MazeEnvironment.TILE_SIZE / 2 - game.GameEnvironment.PLAYER.height / 2)

    def fog_of_war(self):
        pass

    def tick(self):
        if self.up and MazeEnvironment.CAN_MOVE_UP:
            MazeEnvironment.MAP_Y += MazeEnvironment.SPEED
            for b in self.game_environment.boosters:
                b[0].y += MazeEnvironment.SPEED
            for e in self.game_environment.enemies:
                e[0].y += MazeEnvironment.SPEED
            if MazeEnvironment.MAP_Y > 0:
                MazeEnvironment.MAP_Y = 0
        elif self.down and MazeEnvironment.CAN_MOVE_DOWN:
            MazeEnvironment.MAP_Y -= MazeEnvironment.SPEED
            for b in self.game_environment.boosters:
                b[0].y -= MazeEnvironment.SPEED
            for e in self.game_environment.enemies:
                e[0].y -= MazeEnvironment.SPEED
            # dirty way to correct any map movement that is out of bounds
            ch = -1 * MazeEnvironment.PIXEL_HEIGHT + pygame.display.get_window_size()[1]
            if MazeEnvironment.MAP_Y < ch:
                MazeEnvironment.MAP_Y = ch

        if self.left and MazeEnvironment.CAN_MOVE_LEFT:
            MazeEnvironment.MAP_X += MazeEnvironment.SPEED
            for b in self.game_environment.boosters:
                b[0].x += MazeEnvironment.SPEED
            for e in self.game_environment.enemies:
                e[0].x += MazeEnvironment.SPEED
            if MazeEnvironment.MAP_X > 0:
                MazeEnvironment.MAP_X = 0
        elif self.right and MazeEnvironment.CAN_MOVE_RIGHT:
            MazeEnvironment.MAP_X -= MazeEnvironment.SPEED
            for b in self.game_environment.boosters:
                b[0].x -= MazeEnvironment.SPEED
            for e in self.game_environment.enemies:
                e[0].x -= MazeEnvironment.SPEED
            # dirty way to correct any map movement that is out of bounds
            cw = -1 * MazeEnvironment.PIXEL_WIDTH + pygame.display.get_window_size()[0]
            if MazeEnvironment.MAP_X < cw:
                MazeEnvironment.MAP_X = cw

        # tick the boosters and enemies
        for b in self.game_environment.boosters:
            b[0].tick()

        for e in self.game_environment.enemies:
            e[0].tick()

    def render(self, surface):
        s = MazeEnvironment.TILE_SIZE
        wall = pygame.Surface((s, s))
        wall.convert()
        wall.fill((0, 0, 0))
        start = pygame.Surface((s, s))
        start.convert()
        start.fill((0, 255, 0))
        end = pygame.Surface((s, s))
        end.convert()
        end.fill((255, 0, 0))

        grid = MazeEnvironment.MAZE.grid
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                position = (MazeEnvironment.MAP_X + (j * s), MazeEnvironment.MAP_Y + (i * s))
                if MazeEnvironment.START == grid[i][j]:
                    surface.blit(start, position)
                elif MazeEnvironment.END == grid[i][j]:
                    surface.blit(end, position)
                elif MazeEnvironment.WALL == grid[i][j]:
                    edgewall = False
                    for w in range(0, len(self.calculated_walls)):
                        ij = self.calculated_walls[w][0]
                        if i == ij[0] and j == ij[1]:
                            surface.blit(self.calculated_walls[w][1], position)
                            edgewall = True
                    if not edgewall:
                        surface.blit(wall, position)
                else:
                    surface.blit(self.floor_surface, position)

        # render the boosters and enemies
        for b in self.game_environment.boosters:
            b[0].render(surface)

        for e in self.game_environment.enemies:
            e[0].render(surface)
