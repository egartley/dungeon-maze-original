import random
import sys
import pygame

WIDTH = 800
HEIGHT = 620
TARGET_FPS = 60
TILE_SIZE = 128
# whether to allow movement beyond the limits of the window size
BOUND_TO_WINDOW = False


class Tile:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.surface.convert()
        self.surface.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def render(self, surface, x, y):
        surface.blit(self.surface, (x, y))


# performance issues WILL happen when the map is even slightly big. to solve
# this, only portions of the map that are visible should actually be rendered
class Map:
    def __init__(self, rows, columns):
        self.x = 0
        self.y = 0
        self.speed = 4
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.rows = rows
        self.columns = columns
        self.tiles = []
        self.build_tiles()

    def build_tiles(self):
        # build 2d array of specified size with tiles
        for r in range(self.rows):
            row = []
            for c in range(self.columns):
                row.append(Tile(r, c))
            self.tiles.append(row)

    def tick(self):
        # do the opposite addition/subtraction since tile coords
        # are offset from x and y
        if self.up:
            if not BOUND_TO_WINDOW or (BOUND_TO_WINDOW and self.y <= -self.speed):
                self.y += self.speed
        elif self.down:
            if not BOUND_TO_WINDOW or \
                    (BOUND_TO_WINDOW and TILE_SIZE + self.y + TILE_SIZE * (self.rows - 1) >= HEIGHT + self.speed):
                self.y -= self.speed

        if self.left:
            if not BOUND_TO_WINDOW or (BOUND_TO_WINDOW and self.x <= -self.speed):
                self.x += self.speed
        elif self.right:
            if not BOUND_TO_WINDOW or \
                    (BOUND_TO_WINDOW and TILE_SIZE + self.x + TILE_SIZE * (self.columns - 1) >= WIDTH + self.speed):
                self.x -= self.speed

    def render(self, surface):
        for r in range(self.rows):
            for c in range(self.columns):
                # switch the r and c variables when calculating coords to
                # render in the intended orientation
                self.tiles[r][c].render(surface, self.x + TILE_SIZE * c, self.y + TILE_SIZE * r)


def main():
    pygame.init()
    pygame.display.set_caption("Map Movement Example")

    fps = pygame.time.Clock()
    # get the display window's surface
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

    # create a Box object starting in the center of the screen
    # making it global allows access outside of main()
    global map
    map = Map(7, 10)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # display window was closed
                pygame.quit()
                sys.exit()
            event_handler(event)

        tick()
        render(display_surface)

        # refresh display window's surface
        pygame.display.flip()
        # lock to 60 fps
        fps.tick(TARGET_FPS)


def event_handler(event):
    # bind WASD keys to movement of map
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            map.up = True
        elif event.key == pygame.K_a:
            map.left = True
        elif event.key == pygame.K_s:
            map.down = True
        elif event.key == pygame.K_d:
            map.right = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
            map.up = False
        elif event.key == pygame.K_a:
            map.left = False
        elif event.key == pygame.K_s:
            map.down = False
        elif event.key == pygame.K_d:
            map.right = False


def tick():
    map.tick()


def render(surface):
    # having a background is important because otherwise previous renders are visible
    background = pygame.Surface((WIDTH, HEIGHT))
    background.convert()
    background.fill((0, 0, 0))
    surface.blit(background, (0, 0))

    map.render(surface)


if __name__ == "__main__":
    main()
