import random
import sys
import pygame

WIDTH = 350
HEIGHT = 350
TARGET_FPS = 60


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.surface = pygame.Surface((64, 64))
        self.surface.convert()
        self.surface.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        self.collided = False

    def tick(self):
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def render(self, surface):
        surface.blit(self.surface, (self.x, self.y))


def main():
    pygame.init()
    pygame.display.set_caption("Collision Example")

    fps = pygame.time.Clock()
    # get the display window's surface
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

    # create a Box object starting in the center of the screen
    # making it global allows access outside of main()
    global box
    box = Box(WIDTH / 2 - 32, HEIGHT / 2 - 32)

    global box2
    box2 = Box(0, HEIGHT / 2 - 72)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # display window was closed
                pygame.quit()
                sys.exit()

        tick()
        render(display_surface)

        # refresh display window's surface
        pygame.display.flip()
        # lock to 60 fps
        fps.tick(TARGET_FPS)


def tick():
    box2.x += box2.speed
    if box2.x > WIDTH:
        box2.x = -32

    # call box tick methods to update their rects
    # don't need to call box.tick() since it doesn't move
    box2.tick()

    # magic happens here
    box.collided = box.rect.colliderect(box2.rect)


def render(surface):
    # having a background is important because otherwise previous renders of the box are visible
    background = pygame.Surface((WIDTH, HEIGHT))
    background.convert()
    background.fill((0, 0, 0))
    surface.blit(background, (0, 0))

    box.render(surface)
    box2.render(surface)

    font = pygame.font.SysFont("Arial", 16)
    text = font.render("Collided: " + str(box.collided), True, (255, 255, 255))
    surface.blit(text, (12, 12))


if __name__ == "__main__":
    main()
