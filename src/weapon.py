import pygame


class Weapon:
    def __init__(self):
        self.damage = 0
        self.sprite = None
        self.cooldown = 0
        self.in_cooldown = False
        self.range = 0


class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = 10
        self.cooldown = 1
        self.range = 8
        self.sprite = pygame.Surface((5, 20))
        self.sprite.convert()
        self.sprite.fill((255, 255, 255))

    def render(self, surface, x, y):
        surface.blit(self.sprite, (x, y))


class Bow(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = 15
