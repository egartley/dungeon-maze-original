import pygame
import booster
import game
import weapon
from maze import MazeEnvironment


class Character:
    def __init__(self):
        self.weapon = weapon.Weapon()
        self.sprite = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.health = 100
        self.shield = 0
        self.x = 0
        self.y = 0
        # see explaination for relative coords in maincharacter
        self.relative_x = 0
        self.relative_y = 0
        self.width = 0
        self.height = 0
        self.speed = 0
        self.arrow_count = 0
        # whether or not charater (enemy or player) is moving in said direction
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def tick(self):
        pass

    def render(self, surface):
        pass

    def attack(self):
        pass


class MainCharacter(Character):
    # constants for differing between directions
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    # unique event id that can only be used for player attack
    ATTACK_EVENT_ID = pygame.USEREVENT + 74

    def __init__(self, name=None, gender=None):
        super().__init__()
        self.name = name
        self.health = 100
        self.shield = 100
        self.weapon = weapon.Sword()
        self.speed = 4
        self.color = (0, 16, 255)
        self.width = 28
        self.height = 42
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # this is later defined as a rect that is bigger than above rect by sword range
        self.combat_rect = pygame.Rect(0, 0, 0, 0)
        self.active_booster = None
        self.gender = gender
        if self.gender == 1:
            self.color = (245, 40, 145)
        self.sprite = pygame.Surface((self.width, self.height))
        if name is not None:
            self.sprite.convert()
        self.sprite.fill(self.color)
        # whether the player is in the center of the screen in each axis
        self.at_center_x = False
        self.at_center_y = False
        # whether the player is blocked from going in a direction
        self.blocked = (False, False, False, False)
        # the player's tile position within the map
        self.tile_pos = ()
        self.attack_multiplier = 1
        # enemies that are currently within melee range
        self.enemies_in_range = []

    def apply_booster(self, b):
        need_timer = False
        if isinstance(b, booster.HealthBooster):
            self.health += b.increase
        elif isinstance(b, booster.SpeedBooster):
            self.speed = int(self.speed * b.increase)
            MazeEnvironment.SPEED = int(MazeEnvironment.SPEED * b.increase)
            need_timer = True
        elif isinstance(b, booster.AttackBooster):
            self.attack_multiplier = b.increase
            need_timer = True
        elif isinstance(b, booster.ShieldBooster):
            self.shield += b.increase
        elif isinstance(b, booster.ArrowBooster):
            self.arrow_count += b.increase

        if need_timer:
            self.active_booster = b
            pygame.time.set_timer(game.GameEnvironment.BOOSTER_EVENT_ID, b.time * 1000)

    def cancel_active_booster(self):
        b = self.active_booster
        if isinstance(b, booster.AttackBooster):
            self.attack_multiplier = 1
            pass
        elif isinstance(b, booster.SpeedBooster):
            self.speed /= b.increase
            MazeEnvironment.SPEED /= b.increase
        self.active_booster = None
        pygame.time.set_timer(game.GameEnvironment.BOOSTER_EVENT_ID, 0)

    def tick(self):
        if self.up:
            if not MazeEnvironment.CAN_MOVE_UP:
                self.move(MainCharacter.UP)
        elif self.down:
            if not MazeEnvironment.CAN_MOVE_DOWN:
                self.move(MainCharacter.DOWN)
        if self.left:
            if not MazeEnvironment.CAN_MOVE_LEFT:
                self.move(MainCharacter.LEFT)
        elif self.right:
            if not MazeEnvironment.CAN_MOVE_RIGHT:
                self.move(MainCharacter.RIGHT)
        # update tile pos and both rects for the updated x/y from moving
        self.tile_pos = int(self.relative_y // MazeEnvironment.TILE_SIZE), int(
            self.relative_x // MazeEnvironment.TILE_SIZE)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.combat_rect = pygame.Rect(self.x - self.weapon.range, self.y - self.weapon.range,
                                       self.width + (self.weapon.range * 2), self.height + (self.weapon.range * 2))

    def render(self, surface):
        surface.blit(self.sprite, (self.x, self.y))

    def move(self, direction):
        # actually change x/y based on direction and not being blocked
        if direction == MainCharacter.UP and not self.blocked[0]:
            self.y -= self.speed
        elif direction == MainCharacter.DOWN and not self.blocked[1]:
            self.y += self.speed

        if direction == MainCharacter.LEFT and not self.blocked[2]:
            self.x -= self.speed
        elif direction == MainCharacter.RIGHT and not self.blocked[3]:
            self.x += self.speed

    def attack(self):
        if not self.weapon.in_cooldown:
            # start cooldown timer
            pygame.time.set_timer(MainCharacter.ATTACK_EVENT_ID, self.weapon.cooldown * 1000)
            self.weapon.in_cooldown = True
            # do the actualy damage to all enemies in range
            for e in self.enemies_in_range:
                e.health -= self.weapon.damage
                if not e.chasing:
                    e.chasing = True


class Enemy(Character):
    # constants for the direction the enemy is facing for use in "seeing" the player
    LEFT = 0
    RIGHT = 1

    def __init__(self):
        super().__init__()
        self.weapon_type = None
        self.is_player_in_view = False
        self.player_in_combat_range = False
        self.width = 48
        self.height = 48
        self.color = (160, 32, 240)
        self.sprite = pygame.Surface((self.width, self.height))
        self.sprite.convert()
        self.sprite.fill(self.color)
        self.rect = self.sprite.get_rect()
        self.direction = Enemy.LEFT
        self.speed = 3
        self.chasing = False

    def chase_player(self):
        # move in the direction of the player if not already next to them
        px = game.GameEnvironment.PLAYER.x
        py = game.GameEnvironment.PLAYER.y
        player_to_left = px + game.GameEnvironment.PLAYER.width < self.x
        player_to_right = px > self.x + self.width
        player_above = py + game.GameEnvironment.PLAYER.height < self.y
        player_below = py > self.y + self.height
        if player_above:
            self.y -= self.speed
        elif player_below:
            self.y += self.speed

        if player_to_right:
            self.x += self.speed
        elif player_to_left:
            self.x -= self.speed

    def tick(self):
        # calculate if player is visible
        px = game.GameEnvironment.PLAYER.x
        py = game.GameEnvironment.PLAYER.y
        lineofsight = self.y < py + game.GameEnvironment.PLAYER.height < self.y + self.height or self.y < py < self.y + self.height
        player_to_left = px < self.x
        player_to_right = px > self.x + self.width
        in_range_x = (max(self.x, px) - min(self.x, px) - self.width) < MazeEnvironment.TILE_SIZE
        in_range_y = (max(self.y, py) - min(self.y, py) - self.height) < MazeEnvironment.TILE_SIZE
        if self.direction == Enemy.LEFT:
            self.is_player_in_view = lineofsight and player_to_left and in_range_x and in_range_y
        else:
            self.is_player_in_view = lineofsight and player_to_right and in_range_x and in_range_y
        if self.is_player_in_view:
            self.chasing = True

        if self.chasing:
            self.chase_player()

        # update rect based on any changes to actual x/y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, surface):
        surface.blit(self.sprite, (self.x, self.y))
        s = pygame.Surface((8, 8))
        s.convert()
        s.fill((255, 255, 255))
        if self.direction == Enemy.LEFT:
            surface.blit(s, (self.x, self.y + (self.height / 2 - 4)))
        else:
            surface.blit(s, (self.x + self.width - 8, self.y + (self.height / 2 - 4)))
        # health bar (keep?)
        w = (self.health / 100) * self.width
        if w < 0:
            w = 0
        h = pygame.Surface((w, 6))
        h.convert()
        h.fill((255, 0, 0))
        surface.blit(h, (self.x, self.y))

    def attack(self):
        pass  # overrides character.attack
