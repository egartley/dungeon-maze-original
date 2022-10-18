from pygame import *
import game
from os import *
class Booster:
    def __init__(self):
        self.increase = 0
        self.size = 14
        self.sprite = Surface((self.size, self.size))
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
        self.rect = Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())

    def render(self, surface):
        surface.blit(self.sprite, (self.x, self.y))


class ArrowBooster(Booster):
    def __init__(self):
        super().__init__()
        self.increase = 10
        self.sprite = image.load(path.join('game/src','arrow.png'))
        self.sprite = transform.scale(self.sprite, (20,20))
        self.rect = self.sprite.get_rect()


class SpeedBooster(Booster):
    def __init__(self):
        super().__init__()
        self.time = 30
        self.increase = 1.5
        self.sprite = image.load(path.join('game/src','speed.png'))
        self.sprite = transform.scale(self.sprite, (200,40))
        self.rect = self.sprite.get_rect()


class HealthBooster(Booster):
    def __init__(self):
        super().__init__()
        self.increase = 10
        self.sprite = image.load(path.join('game/src','health-booster.png'))
        self.sprite = transform.scale(self.sprite, (20,20))
        self.rect = self.sprite.get_rect()
       

class ShieldBooster(Booster):
    def __init__(self):
        super().__init__()
        self.increase = 10
        self.sprite = image.load(path.join('game/src','Shields.png'))
        self.sprite = transform.scale(self.sprite, (20,20))
        self.rect = self.sprite.get_rect()


class AttackBooster(Booster):
    def __init__(self):
        super().__init__()
        self.increase = 10
        self.time = 30
        self.sprite = image.load(path.join('game/src','attack.png'))
        self.sprite = transform.scale(self.sprite, (80,38))
        self.rect = self.sprite.get_rect()
