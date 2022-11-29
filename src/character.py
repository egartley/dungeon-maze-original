import pygame
import booster
import game
import weapon
import math
import arrow
import random
from maze import MazeEnvironment
from animation import Animation
from animation import build_frames


def check_wall(x, y):
    r = int(y // MazeEnvironment.TILE_SIZE)
    c = int(x // MazeEnvironment.TILE_SIZE)
    if r >= len(MazeEnvironment.MAZE.grid) or c >= len(MazeEnvironment.MAZE.grid[0]):
        return True
    return MazeEnvironment.MAZE.grid[r][c] == MazeEnvironment.WALL


def get_event_id():
    r = random.Random()
    x = r.randint(1000, 9999)
    while x in MazeEnvironment.ENEMY_EVENT_IDS:
        x = r.randint(1000, 9999)
    uid = x + pygame.USEREVENT
    MazeEnvironment.ENEMY_EVENT_IDS.append(uid)
    return uid


def build_animations():
    attacksheet = pygame.image.load("src/sprites/Enemies/Attacking/attacking.png")
    attacksheet.convert_alpha()
    walksheet = pygame.image.load("src/sprites/Enemies/Walking/walking.png")
    walksheet.convert_alpha()
    deathsheet = pygame.image.load("src/sprites/Enemies/Death/death.png")
    deathsheet.convert_alpha()
    Enemy.ATTACK_RIGHT_FRAMES = build_frames(attacksheet, 12)
    Enemy.ATTACK_LEFT_FRAMES = build_frames(pygame.transform.flip(attacksheet, True, False), 12, True)
    Enemy.WALK_RIGHT_FRAMES = build_frames(walksheet, 18)
    Enemy.WALK_LEFT_FRAMES = build_frames(pygame.transform.flip(walksheet, True, False), 18, True)
    Enemy.DEATH_RIGHT_FRAMES = build_frames(deathsheet, 15)
    Enemy.DEATH_LEFT_FRAMES = build_frames(pygame.transform.flip(deathsheet, True, False), 15, True)


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weapon = weapon.Weapon()
        self.sprite = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.health = 100
        self.shield = 0
        self.x = 0
        self.y = 0
        # see explanation for relative coords in maincharacter
        self.relative_x = 0
        self.relative_y = 0
        self.width = 0
        self.height = 0
        self.speed = 0
        self.arrow_count = 1000
        # whether character (enemy or player) is moving in said direction
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
    DEATH_ID = pygame.USEREVENT + 1000
    # unique event ids
    ATTACK_EVENT_ID = pygame.USEREVENT + 74
    SWORD_SWING_EVENT_ID = pygame.USEREVENT + 75
    METH_COUNT = 0
    ATTACK_COUNT = 0

    def __init__(self, name=None):
        super().__init__()
        # relative coordinates:
        # these are the x/y based on relative = absolute - map
        # ex. relative_x = x - map_x
        # map x/y are the top left of the map itself, changing when moving the map
        # "absolute" x/y or just x/y by itself, is where the thing is actually rendered
        # to in the display window (where all the surface.blit calls are)
        self.arrow_count = 10
        self.name = name
        self.health = 100
        self.shield = 100
        self.weapon = weapon.Sword()
        self.speed = 4
        self.speedStackLen = 3
        self.speedStackCount = -1
        self.speedStackTop = -1
        self.speedStackLast = 0
        self.speedInstances = [None] * self.speedStackLen
        self.speedStack = [False] * self.speedStackLen

        self.attack = 1
        self.attackStackLen = 3
        self.attackStackCount = -1
        self.attackStackTop = -1
        self.attackStackLast = 0
        self.attackInstances = [None] * self.attackStackLen
        self.attackStack = [False] * self.attackStackLen

        self.width = 192 / 4
        self.height = 285 / 4
        self.combat_rect = pygame.Rect(0, 0, 0, 0)
        self.active_booster = [False] * 2  # 0 for attack 1 for speed
        self.direction = None
        self.image = pygame.image.load('src/sprites/Character/Wraith_01_Idle_000.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.sprite = self.image
        self.rect = self.image.get_rect()
        self.at_center_x = False
        self.at_center_y = False
        # whether the player is blocked from going in a direction
        self.blocked = (False, False, False, False)
        # the player's tile position within the map
        self.tile_pos = ()
        self.attack_multiplier = 1
        # enemies that are currently within melee range
        self.enemies_in_range = []
        self.swinging_sword = False
        # set group sprite for weapon and arrows
        self.weapon_group = pygame.sprite.Group()
        self.arrow_group = pygame.sprite.Group()
        self.bow = weapon.Bow()
        self.bow_group = pygame.sprite.Group()
        self.is_using_bow = False
        self.is_using_sword = True

    def apply_booster(self, b):
        if isinstance(b, booster.HealthBooster):
            if self.health + b.increase >= 100:
                self.health = 100
            else:
                self.health += booster.HealthBooster.increase

        elif isinstance(b, booster.SpeedBooster) and not self.isSpeedFull():
            self.speed = int (math.ceil(self.speed * booster.SpeedBooster.increase))
            MazeEnvironment.SPEED = int(math.ceil(MazeEnvironment.SPEED * booster.SpeedBooster.increase))
            self.active_booster[1] = True
            self.speedStackTop += 1
            MainCharacter.METH_COUNT += 1
            self.speedStack[self.speedStackTop % self.speedStackLen] = True
            self.speedInstances[self.speedStackTop % self.speedStackLen] = b
            pygame.time.set_timer( (b.BOOSTERID + (self.speedStackTop % self.speedStackLen)), b.time * 1000)

        elif isinstance(b, booster.AttackBooster) and not self.isAttackFull():
            self.attack_multiplier += booster.AttackBooster.increase
            self.active_booster[0] = True
            self.attackStackTop += 1
            MainCharacter.ATTACK_COUNT += 1
            self.attackStack[self.attackStackTop % self.attackStackLen] = True
            self.attackInstances[self.attackStackTop % self.attackStackLen] = b
            pygame.time.set_timer((b.BOOSTERID + (self.attackStackTop % self.attackStackLen)), b.time * 1000)

        elif isinstance(b, booster.ShieldBooster):
            if self.shield + b.increase >= 100:
                self.shield = 100
            else:
                self.shield += booster.ShieldBooster.increase

        elif isinstance(b, booster.ArrowBooster):
            self.arrow_count += b.increase

    def isSpeedFull(self):
        i = 0
        for i in range(len(self.speedStack)):
            if not self.speedStack[i]:
                return False
            i += 1
        return True

    def isSpeedEmpty(self):
        i = 0
        for i in range(len(self.speedStack)):
            if not self.speedStack[i]:
                return False
            i += 1
        return True

    def isAttackFull(self):
        i = 0
        for i in range(len(self.attackStack)):
            if not self.attackStack[i]:
                return False
            i += 1
        return True

    def isAttackEmpty(self):
        i = 0
        for i in range(len(self.attackStack)):
            if not self.attackStack[i]:
                return False
            i += 1
        return True

    def cancel_active_booster(self, boosterID):
        if self.active_booster[0] and boosterID == booster.AttackBooster.BOOSTERID + (game.GameEnvironment.PLAYER.attackStackLast % game.GameEnvironment.PLAYER.attackStackLen):
            MainCharacter.ATTACK_COUNT -= 1
            self.attack_multiplier -= booster.AttackBooster.increase
            self.attackStack[self.attackStackLast % self.attackStackLen] = False
            self.attackInstances[self.attackStackLast % self.attackStackLen] = None
            pygame.time.set_timer( boosterID , 0)
            self.attackStackLast += 1
            if self.isAttackEmpty():
                self.active_booster[0] = False
        elif self.active_booster[1] and boosterID == booster.SpeedBooster.BOOSTERID + (game.GameEnvironment.PLAYER.speedStackLast % game.GameEnvironment.PLAYER.speedStackLen):
            MainCharacter.METH_COUNT -= 1
            self.speed = int(math.ceil(self.speed/booster.SpeedBooster.increase))
            MazeEnvironment.SPEED = int(math.ceil(MazeEnvironment.SPEED/booster.SpeedBooster.increase))
            pygame.time.set_timer(boosterID, 0)
            self.speedStack[self.speedStackLast % self.speedStackLen] = False
            self.speedInstances[self.speedStackLast % self.speedStackLen] = None
            self.speedStackLast += 1
            if self.isSpeedEmpty():
                self.active_booster[1] = False
                self.speed = 4
                MazeEnvironment.speed = 4
        else:
            pygame.time.set_timer(game.GameEnvironment.BOOSTER_EVENT_ID, 0)

    def tick(self):
        if self.up:
            if not MazeEnvironment.CAN_MOVE_UP:
                self.move(MainCharacter.UP)
        elif self.down:
            if not MazeEnvironment.CAN_MOVE_DOWN:
                self.move(MainCharacter.DOWN)
        if self.left:
            self.sprite = pygame.transform.flip(self.image, True, False)
            if not MazeEnvironment.CAN_MOVE_LEFT:
                self.move(MainCharacter.LEFT)
        elif self.right:
            self.sprite = self.image
            if not MazeEnvironment.CAN_MOVE_RIGHT:
                self.move(MainCharacter.RIGHT)
        # update tile pos and both rects for the updated x/y from moving
        self.tile_pos = int(self.relative_y // MazeEnvironment.TILE_SIZE), int(
            self.relative_x // MazeEnvironment.TILE_SIZE)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, surface):
        surface.blit(self.sprite, (self.x, self.y))
        self.arrow_group.update()
        self.arrow_group.draw(surface)
        if (self.is_using_sword == False):
            self.sprite_bow(surface)
            self.is_using_bow = True
        elif pygame.mouse.get_pos()[0] >= (self.x + (self.width/2)):
            self.is_using_sword = True
            self.weapon.directionSprite(self.x + 30, self.y + 15, "right")
            self.weapon_group.add(self.weapon)
            self.combat_rect = pygame.Rect(self.x + 40 - self.weapon.range, self.y + 10 - self.weapon.range,
                                    self.width + (self.weapon.range * 2), self.height - 10 + (self.weapon.range * 2))
            if not self.weapon.is_animating:
                self.weapon_group.draw(surface)
            if self.swinging_sword:
                self.weapon.render(self.x + 30, self.y + 15, "right")
                self.weapon_group.draw(surface)

        elif pygame.mouse.get_pos()[0] < (self.x + (self.width/2)):
            self.is_using_sword = True
            self.weapon.directionSprite(self.x - 82, self.y + 15, "left")
            self.weapon_group.add(self.weapon)
            self.combat_rect = pygame.Rect(self.x - 40 - self.weapon.range, self.y + 10 - self.weapon.range,
                                    self.width + (self.weapon.range * 2), self.height - 10+ (self.weapon.range * 2))
            if not self.weapon.is_animating:
                self.weapon_group.draw(surface)
            if self.swinging_sword:
                self.weapon.render(self.x - 82, self.y + 15, "left")
                self.weapon_group.draw(surface)

    def sprite_bow(self, surface):
        self.bow.character_position(self.x + 25, self.y + 35)
        self.bow.target_position(pygame.mouse.get_pos())
        self.bow.move(surface)

    def create_arrow(self, target_pos):
        return arrow.Arrow(self.x + 25, self.y + 35, target_pos[0], target_pos[1])

    def shoot(self, target_pos):
        if self.arrow_count > 0:
            self.arrow_group.add(self.create_arrow(target_pos))
            self.arrow_count -= 1

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

    def attack_motion(self):
        if not self.weapon.in_cooldown:
            # start cooldown timer
            pygame.time.set_timer(MainCharacter.ATTACK_EVENT_ID, self.weapon.cooldown * 1000)
            self.weapon.in_cooldown = True
            self.weapon.is_animating = True
            pygame.time.set_timer(MainCharacter.SWORD_SWING_EVENT_ID, 430)
            self.swinging_sword = True
            # do the actual damage to all enemies in range
            for e in self.enemies_in_range:
                e.health -= self.weapon.damage * self.attack_multiplier
                e.force_chase = True

    def take_damage(self, damage):
        if self.shield > 0:
            if self.shield < 0:
                remaining = self.shield - damage
                self.shield = 0
                self.health -= remaining
            elif self.shield + self.health - damage <= 0:
                game.GameEnvironment.state = game.GameEnvironment.DEATH_STATE
            else:
                self.shield -= damage
        else:
            self.health -= damage
            if self.health <= 0:
                MainCharacter.METH_COUNT = 0
                MainCharacter.ATTACK_COUNT = 0
                game.GameEnvironment.state = game.GameEnvironment.DEATH_STATE


class Enemy(Character):

    LEFT = 0
    RIGHT = 1

    ATTACK_LEFT_FRAMES = []
    ATTACK_RIGHT_FRAMES = []
    WALK_LEFT_FRAMES = []
    WALK_RIGHT_FRAMES = []
    DEATH_LEFT_FRAMES = []
    DEATH_RIGHT_FRAMES = []
    loaded_frames = False

    def __init__(self, damage, game_env, seed):
        super().__init__()
        self.game_environment = game_env
        self.weapon_type = None
        self.is_player_in_view = False
        self.player_in_combat_range = False
        self.weapon = weapon.Sword()
        self.width = 133
        self.height = 118
        self.collision_padding = 8
        self.image = pygame.image.load("src/sprites/Enemies/idle.png")
        self.image2 = pygame.transform.flip(self.image, True, False)

        self.damage = damage
        self.health_bar_surface = pygame.Surface((self.width / 2, 8))
        self.health_bar_surface.convert()
        self.health_bar_color_background = (0, 0, 0)
        self.health_bar_color_foreground = (255, 0, 0)
        self.health_bar_color_outline = (255, 255, 255)
        self.max_health = 100
        self.seed = seed

        self.rect = self.image.get_rect()
        self.direction = Enemy.LEFT
        self.last_direction = Enemy.LEFT
        self.speed = 3
        self.chasing = False
        self.force_chase = False
        self.damage = damage
        self.coolDown = 10
        self.placed = False
        self.collision_set = False
        self.blocked = ()
        self.collision_rect = pygame.Rect(0, 0, 0, 0)

        self.unique_id = get_event_id()

        if not Enemy.loaded_frames:
            build_animations()
            Enemy.loaded_frames = True
        delay = 40
        self.walk_animation = [Animation(Enemy.WALK_LEFT_FRAMES, delay, True, get_event_id()),
                               Animation(Enemy.WALK_RIGHT_FRAMES, delay, True, get_event_id())]
        self.attack_animation = [Animation(Enemy.ATTACK_LEFT_FRAMES, delay, True, get_event_id()),
                                 Animation(Enemy.ATTACK_RIGHT_FRAMES, delay, True, get_event_id())]
        self.death_animation = [Animation(Enemy.DEATH_LEFT_FRAMES, delay, False, get_event_id()),
                                Animation(Enemy.DEATH_RIGHT_FRAMES, delay, False, get_event_id())]
        self.start_attack_animation = False
        self.current_animation = None
        self.alive = True

    def die(self):
        self.x -= 20
        self.current_animation = self.death_animation[0 if self.direction == Enemy.LEFT else 1]
        self.current_animation.restart()
        self.alive = False

    def chase_player(self):
        # move in the direction of the player if not already next to them
        px = game.GameEnvironment.PLAYER.x
        py = game.GameEnvironment.PLAYER.y
        pw = game.GameEnvironment.PLAYER.width
        ph = game.GameEnvironment.PLAYER.height
        pr = game.GameEnvironment.PLAYER.rect
        pc_x = px + (pw // 2)
        pc_y = py + (ph // 2)
        ec_x = self.x + (self.width // 2)
        ec_y = self.y + (self.height // 2)
        player_to_left = pc_x < ec_x + self.collision_padding
        player_to_right = pc_x > ec_x - self.collision_padding
        player_above = pc_y < ec_y + self.collision_padding
        player_below = pc_y > ec_y - self.collision_padding

        wall_check_rect = pygame.Rect(self.relative_x + 56, self.relative_y + 10, 70, 104)
        blocked_up = check_wall(wall_check_rect.x, wall_check_rect.y - self.speed) or \
                     check_wall(wall_check_rect.x + wall_check_rect.width, wall_check_rect.y - self.speed)
        blocked_down = check_wall(wall_check_rect.x,
                                  wall_check_rect.y + wall_check_rect.height + self.speed) or \
                       check_wall(wall_check_rect.x + wall_check_rect.width,
                                  wall_check_rect.y + wall_check_rect.height + self.speed)
        blocked_left = check_wall(wall_check_rect.x - self.speed, wall_check_rect.y) or \
                       check_wall(wall_check_rect.x - self.speed, wall_check_rect.y + wall_check_rect.height)
        blocked_right = check_wall(wall_check_rect.x + wall_check_rect.width + self.speed,
                                   wall_check_rect.y) or \
                        check_wall(wall_check_rect.x + wall_check_rect.width + self.speed,
                                   wall_check_rect.y + wall_check_rect.height)
        self.blocked = (blocked_up, blocked_down, blocked_left, blocked_right)

        next_move = (self.collision_rect.move(0, -1 * self.speed * 2), self.collision_rect.move(0, self.speed * 2),
                     self.collision_rect.move(-1 * self.speed * 2, 0), self.collision_rect.move(self.speed * 2, 0))
        if player_above and not self.blocked[0] and not pr.colliderect(next_move[0]):
            if not self.would_collide_with_other_enemy(next_move[0], 0):
                self.y -= self.speed
        if player_below and not self.blocked[1] and not pr.colliderect(next_move[1]):
            if not self.would_collide_with_other_enemy(next_move[1], 1):
                self.y += self.speed
        if player_to_left and not self.blocked[2] and not pr.colliderect(next_move[2]):
            if not self.would_collide_with_other_enemy(next_move[2], 2):
                self.x -= self.speed
        if player_to_right and not self.blocked[3] and not pr.colliderect(next_move[3]):
            if not self.would_collide_with_other_enemy(next_move[3], 3):
                self.x += self.speed

        if player_to_left:
            self.direction = Enemy.LEFT
        elif player_to_right:
            self.direction = Enemy.RIGHT

    def would_collide_with_other_enemy(self, r, d):
        would = False
        for e in self.game_environment.enemies:
            if not e[0].unique_id == self.unique_id:
                dirblock = False
                if d == 0:
                    dirblock = e[0].collision_rect.collidepoint((r.x, r.y)) or \
                               e[0].collision_rect.collidepoint((r.x + r.width, r.y))
                elif d == 1:
                    dirblock = e[0].collision_rect.collidepoint((r.x, r.y + r.height)) or \
                               e[0].collision_rect.collidepoint((r.x + r.width, r.y + r.height))
                elif d == 2:
                    dirblock = e[0].collision_rect.collidepoint((r.x, r.y)) or \
                               e[0].collision_rect.collidepoint((r.x, r.y + r.height))
                elif d == 3:
                    dirblock = e[0].collision_rect.collidepoint((r.x + r.width, r.y)) or \
                               e[0].collision_rect.collidepoint((r.x + r.width, r.y + r.height))
                if dirblock:
                    would = True
                else:
                    continue
                break
        return would

    def tick(self):
        if not self.alive:
            if not self.current_animation.running:
                self.game_environment.on_enemy_death(self)
            return
        # calculate if player is visible
        px = game.GameEnvironment.PLAYER.x
        py = game.GameEnvironment.PLAYER.y
        lineofsight = self.y < py + game.GameEnvironment.PLAYER.height < self.y + self.height or self.y < py < self.y + self.height
        player_to_left = px < self.x
        player_to_right = px > self.x + self.width
        in_range_x = (max(self.x, px) - min(self.x, px) - self.width * 2) < MazeEnvironment.TILE_SIZE
        in_range_y = (max(self.y, py) - min(self.y, py) - self.height * 2) < MazeEnvironment.TILE_SIZE
        self.relative_x = self.x - MazeEnvironment.MAP_X
        self.relative_y = self.y - MazeEnvironment.MAP_Y

        self.is_player_in_view = lineofsight and (player_to_left if self.direction == Enemy.LEFT else player_to_right) and in_range_x and in_range_y
        if self.is_player_in_view:
            self.chasing = True

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # idle
        xoffset = 10 if self.direction == Enemy.RIGHT else 52
        if self.weapon.in_cooldown:
            # attack
            xoffset = 52 if self.direction == Enemy.LEFT else 12
        self.collision_rect = pygame.Rect(self.x + xoffset, self.y + 22, 70, 94)

        if self.chasing or self.force_chase:
            if not self.chasing:
                self.chasing = True
            self.chase_player()

        if self.player_in_combat_range:
            self.attack()

    def render(self, surface):
        if not self.alive:
            surface.blit(self.current_animation.frame, (self.x, self.y))
            return
        if self.chasing:
            if self.weapon.in_cooldown:
                if self.start_attack_animation:
                    self.last_direction = self.direction
                    self.current_animation = self.attack_animation[0 if self.direction == Enemy.LEFT else 1]
                    self.current_animation.restart()
                    self.start_attack_animation = False
                if not self.direction == self.last_direction:
                    self.current_animation = self.attack_animation[0 if self.direction == Enemy.LEFT else 1]
                    self.current_animation.restart()
                    self.last_direction = self.direction
                surface.blit(self.current_animation.frame, (self.x, self.y))
            elif self.player_in_combat_range:
                surface.blit(self.image if self.direction == Enemy.LEFT else self.image2, (self.x, self.y))
            else:
                i = 0 if self.direction == Enemy.LEFT else 1
                if self.current_animation is None:
                    self.current_animation = self.walk_animation[i]
                    self.current_animation.restart()
                else:
                    current = self.current_animation.event_id
                    desired = self.walk_animation[i].event_id
                    if not current == desired:
                        self.current_animation = self.walk_animation[i]
                        self.current_animation.restart()
                surface.blit(self.current_animation.frame, (self.x, self.y))
        else:
            surface.blit(self.image if self.direction == Enemy.RIGHT else self.image2, (self.x, self.y))
        # pygame.draw.rect(surface, (255, 255, 255), self.collision_rect, 1)

        # render health bar
        o = 1
        w = self.health_bar_surface.get_width()
        h = self.health_bar_surface.get_height()
        outline = pygame.Surface((w, h))
        outline.convert()
        outline.fill(self.health_bar_color_outline)
        self.health_bar_surface.blit(outline, (0, 0))
        background = pygame.Surface((w - (o * 2), h - (o * 2)))
        background.convert()
        background.fill(self.health_bar_color_background)
        self.health_bar_surface.blit(background, (o, o))
        fw = int((self.health / self.max_health) * w) - (o * 2)
        if fw < 0:
            fw = 0
        foreground = pygame.Surface((fw, h - (o * 2)))
        foreground.convert()
        foreground.fill(self.health_bar_color_foreground)
        self.health_bar_surface.blit(foreground, (o, o))

    def attack(self):
        if not self.weapon.in_cooldown:
            self.weapon.in_cooldown = True
            self.start_attack_animation = True
            # start cooldown timer
            if game.GameEnvironment.DIFFICULTY_TRACKER == game.GameEnvironment.DIFFICULTY_HARD:
                pygame.time.set_timer(self.unique_id, self.weapon.cooldown * (1000 + self.seed))
            elif game.GameEnvironment.DIFFICULTY_TRACKER == game.GameEnvironment.DIFFICULTY_MEDIUM:
                 pygame.time.set_timer(self.unique_id, self.weapon.cooldown * (2000 + self.seed))
            else:
                pygame.time.set_timer(self.unique_id, self.weapon.cooldown * (3000 + self.seed))
            self.weapon.in_cooldown = True
            self.start_attack_animation = True
            pygame.time.set_timer(self.unique_id, self.weapon.cooldown * 1000)
            game.GameEnvironment.PLAYER.take_damage(self.damage)

    def on_death(self):
        self.walk_animation[0].stop()
        self.walk_animation[1].stop()
        self.attack_animation[0].stop()
        self.attack_animation[1].stop()
        self.death_animation[0].stop()
        self.death_animation[1].stop()
