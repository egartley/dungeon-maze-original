import sys
import pygame
from game import *

TARGET_FPS = 60
objects = []


def main():
    pygame.init()
    font = pygame.font.SysFont('Arial', 40)
    fps = pygame.time.Clock()
    game_env = GameEnvironment(1000, 700)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game_env.event_handler(event)
            
        for object in objects:
            object.process()
        game_env.tick()
        game_env.render(pygame.display.get_surface())
        pygame.display.flip()
        fps.tick(TARGET_FPS)
        


if __name__ == "__main__":
    main()
