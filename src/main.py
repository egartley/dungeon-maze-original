import sys
import pygame

WIDTH = 500
HEIGHT = 500
TARGET_FPS = 60


def main():
    pygame.init()
    fps = pygame.time.Clock()
    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dungeon Maze")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # handle keyboard/mouse input here

        tick()
        render(pygame.display.get_surface())
        pygame.display.flip()
        fps.tick(TARGET_FPS)


def tick():
    # update game logic
    pass


def render(surface):
    # draw whatever on the screen
    pass


if __name__ == "__main__":
    main()