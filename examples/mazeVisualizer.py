import sys
import pygame
from mazelib import Maze
from mazelib.generate.Prims import Prims

WIDTH = 650
HEIGHT = 650
TARGET_FPS = 60


def main():
    pygame.init()
    pygame.display.set_caption("Maze Visualizer")

    fps = pygame.time.Clock()
    # get the display window's surface
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

    # generate, then print, a maze
    global m
    m = Maze()
    m.generator = Prims(25, 25)
    m.generate()
    m.generate_entrances()
    print(m)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # display window was closed
                pygame.quit()
                sys.exit()

        # here would go a call to a tick() method to handle game logic (before rendering)

        render(display_surface)
        # refresh display window's surface
        pygame.display.flip()
        # lock to 60 fps
        fps.tick(TARGET_FPS)


def render(surface):
    # create different colored 12x12 squares
    wall = pygame.Surface((12, 12))
    wall.convert()
    wall.fill((160, 160, 160))  # medium gray

    start = pygame.Surface((12, 12))
    start.convert()
    start.fill((0, 255, 0))  # green

    end = pygame.Surface((12, 12))
    end.convert()
    end.fill((255, 0, 0))  # red

    # render maze, square if wall/start/end, nothing otherwise
    grid = m.grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            position = (18 + (j * 12), 18 + (i * 12))
            if m.start == (i, j):
                surface.blit(start, position)
            elif m.end == (i, j):
                surface.blit(end, position)
            elif grid[i][j] == 1:
                surface.blit(wall, position)


if __name__ == "__main__":
    main()
