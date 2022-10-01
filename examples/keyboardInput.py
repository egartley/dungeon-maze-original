import sys
import pygame

WIDTH = 800
HEIGHT = 620
TARGET_FPS = 60


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.surface = pygame.Surface((32, 32))
        self.surface.convert()
        self.surface.fill((128, 255, 128))

    def tick(self):
        if self.up:
            self.y -= self.speed
        elif self.down:
            self.y += self.speed

        if self.left:
            self.x -= self.speed
        elif self.right:
            self.x += self.speed

    def render(self, surface):
        surface.blit(self.surface, (self.x, self.y))


def main():
    pygame.init()
    pygame.display.set_caption("Keyboard Input Example")

    fps = pygame.time.Clock()
    # get the display window's surface
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

    # create a Box object starting in the center of the screen
    # making it global allows access outside of main()
    global box
    box = Box(WIDTH / 2 - 16, HEIGHT / 2 - 16)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # display window was closed
                pygame.quit()
                sys.exit()
            # otherwise call an event handler
            event_handler(event)

        tick()
        render(display_surface)

        # refresh display window's surface
        pygame.display.flip()
        # lock to 60 fps
        fps.tick(TARGET_FPS)


def event_handler(event):
    # bind WASD keys to movement of box
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            box.up = True
        elif event.key == pygame.K_a:
            box.left = True
        elif event.key == pygame.K_s:
            box.down = True
        elif event.key == pygame.K_d:
            box.right = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
            box.up = False
        elif event.key == pygame.K_a:
            box.left = False
        elif event.key == pygame.K_s:
            box.down = False
        elif event.key == pygame.K_d:
            box.right = False


def tick():
    box.tick()


def render(surface):
    # having a background is important because otherwise previous renders of the box are visible
    background = pygame.Surface((WIDTH, HEIGHT))
    background.convert()
    background.fill((0, 0, 0))
    surface.blit(background, (0, 0))

    box.render(surface)

    font = pygame.font.SysFont("Arial", 16)
    text = font.render("Use the WASD keys to move", True, (255, 255, 255))
    surface.blit(text, (12, 12))


if __name__ == "__main__":
    main()
