from game import *

TARGET_FPS = 60
objects = []


def main():
    pygame.init()
    fps = pygame.time.Clock()
    game_env = GameEnvironment(1000, 700)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game_env.event_handler(event)

        game_env.tick()
        game_env.render(pygame.display.get_surface())
        pygame.display.flip()
        fps.tick(TARGET_FPS)


if __name__ == "__main__":
    main()
