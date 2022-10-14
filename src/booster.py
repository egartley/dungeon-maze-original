import pygame
import game


class Booster:
    def __init__(self):
        self.increase = 0
        self.size = 14
        self.sprite = pygame.Surface((self.size, self.size))
        self.rect = self.sprite.get_rect()
        self.x = 0
        self.y = 0
        # see explaination for relative coords in maincharacter
        self.relative_x = 0
        self.relative_y = 0

    def booster_collision(self):
        # called when a booster collides with the player
        game.GameEnvironment.PLAYER.apply_booster(self)

    def tick(self):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def render(self, surface):
        surface.blit(self.sprite, (self.x, self.y))


class ArrowBooster(Booster):
    def __init__(self):
        super().__init__()
        self.increase = 5
        self.sprite.convert()
        self.sprite.fill((189, 154, 122))
        self.rect = self.sprite.get_rect()


class SpeedBooster(Booster):
    def __init__(self):
        super().__init__()
        self.increase = 1.5
        self.time = 30
        self.sprite.convert()
        self.sprite.fill((31, 176, 245))
        self.rect = self.sprite.get_rect()


class HealthBooster(Booster):
    def __init__(self):
        super().__init__()
        self.increase = 10
        self.sprite.convert()
        self.sprite.fill((255, 0, 0))
        self.rect = self.sprite.get_rect()


class ShieldBooster(Booster):
    def __init__(self):
        super().__init__()
        self.increase = 10
        self.sprite.convert()
        self.sprite.fill((211, 211, 211))
        self.rect = self.sprite.get_rect()


class AttackBooster(Booster):
    def __init__(self):
        super().__init__()
        self.increase = 1.2
        self.time = 30
        self.sprite.convert()
        self.sprite.fill((255, 165, 0))
        self.rect = self.sprite.get_rect()
