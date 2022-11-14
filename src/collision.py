import game


class Collision:
    def __init__(self, rect1, rect2):
        self.rect1 = rect1
        self.rect2 = rect2
        self.is_collided = False

    def tick(self, rect1, rect2):
        self.rect1 = rect1
        self.rect2 = rect2

    def collision_occurrence(self):
        pass

    def check(self):
        self.is_collided = self.rect1.colliderect(self.rect2)


class BoosterCollision(Collision):
    def __init__(self, booster, player_rect):
        super().__init__(booster.rect, player_rect)
        self.booster = booster

    def collision_occurrence(self):
        self.booster.booster_collision()


class EnemyCollision(Collision):
    def __init__(self, enemy, player_combat_rect):
        super().__init__(enemy.rect, player_combat_rect)
        self.enemy = enemy

    def collision_occurrence(self):
        game.GameEnvironment.PLAYER.enemies_in_range.append(self.enemy)
        self.enemy.player_in_combat_range = True

    def collision_end(self):
        if self.enemy in game.GameEnvironment.PLAYER.enemies_in_range:
            game.GameEnvironment.PLAYER.enemies_in_range.remove(self.enemy)
        self.enemy.player_in_combat_range = False

class ArrowCollision(Collision):
    def __init__(self, arrow, enemy):
        super().__init__(arrow, enemy)
