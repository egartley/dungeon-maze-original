import pygame
import booster
import game
import weapon
import math
import arrow
import random
from maze import MazeEnvironment


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

    def __init__(self, name=None):
        super().__init__()
        # relative coordinates:
        # these are the x/y based on relative = absolute - map
        # ex. relative_x = x - map_x
        # map x/y are the top left of the map itself, changing when moving the map
        # "absolute" x/y or just x/y by itself, is where the thing is actually rendered
        # to in the display window (where all the surface.blit calls are)
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
        self.bow_timer = 60
        self.set_animation_bow_timer = self.bow_timer

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
            self.speedStack[self.speedStackTop % self.speedStackLen] = True
            self.speedInstances[self.speedStackTop % self.speedStackLen] = b
            pygame.time.set_timer( (b.BOOSTERID + (self.speedStackTop % self.speedStackLen)), b.time * 1000)
            
        elif isinstance(b, booster.AttackBooster) and not self.isAttackFull():
            self.attack_multiplier += booster.AttackBooster.increase
            self.active_booster[0] = True
            self.attackStackTop += 1
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
            self.attack_multiplier -= booster.AttackBooster.increase
            self.attackStack[self.attackStackLast % self.attackStackLen] = False
            self.attackInstances[self.attackStackLast % self.attackStackLen] = None
            pygame.time.set_timer( boosterID , 0)
            self.attackStackLast += 1
            if self.isAttackEmpty():
                self.active_booster[0] = False
        elif self.active_booster[1] and boosterID == booster.SpeedBooster.BOOSTERID + (game.GameEnvironment.PLAYER.speedStackLast % game.GameEnvironment.PLAYER.speedStackLen):
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
        self.sprite_bow(surface, self.is_using_bow)
        self.arrow_group.update()
        self.arrow_group.draw(surface)
        if pygame.mouse.get_pos()[0] >= (self.x + (self.width/2)):
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
            self.weapon.directionSprite(self.x - 82, self.y + 15, "left")
            self.weapon_group.add(self.weapon)
            self.combat_rect = pygame.Rect(self.x - 40 - self.weapon.range, self.y + 10 - self.weapon.range,
                                    self.width + (self.weapon.range * 2), self.height - 10+ (self.weapon.range * 2))
            if not self.weapon.is_animating:
                self.weapon_group.draw(surface)
            if self.swinging_sword:
                self.weapon.render(self.x - 82, self.y + 15, "left")
                self.weapon_group.draw(surface)

    def sprite_bow(self, surface, is_using_bow):
        if self.set_animation_bow_timer == 0:
            self.set_animation_bow_timer = self.bow_timer
            self.is_using_bow = False

        if is_using_bow and self.set_animation_bow_timer > 0:
            self.bow.character_position(self.x + 25, self.y + 35)
            self.bow.target_position(pygame.mouse.get_pos())
            self.bow.move(surface)
            self.set_animation_bow_timer -= 1

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
                if not e.chasing:
                    e.chasing = True

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
                game.GameEnvironment.state = game.GameEnvironment.DEATH_STATE


class Enemy(Character):
    # constants for the direction the enemy is facing for use in "seeing" the player
    LEFT = 0
    RIGHT = 1

    enemy_walk_frames = []
    enemy_walk_frames_left = []
    enemy_attack_frames = []
    enemy_attack_frames_left = []
    loaded_frames = False

    def __init__(self, damage):
        super().__init__()
        self.weapon_type = None
        self.is_player_in_view = False
        self.player_in_combat_range = False
        self.weapon = weapon.Sword()
        self.width = 180
        self.height = 123
        self.buffer = 35
        self.image = pygame.image.load('src/sprites/Enemies/Minotaur_01_Idle_000.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image2 = (pygame.transform.flip(self.image, True, False))
        self.mask = pygame.mask.from_surface(self.image)

        self.sprite = [self.image]
        self.sprite_counter = 0
        self.sprites_right_walk = []
        self.sprites_left_walk = []
        self.sprites_right_attack = []
        self.sprites_left_attack = []
        self.sprite_modes = [self.sprite, self.sprites_right_walk, self.sprites_right_attack]
        self.sprite_mode = 0
        self.attack_animation = 0
        self.damage = damage
        self.health_bar_surface = pygame.Surface((self.width / 2, 8))
        self.health_bar_surface.convert()
        self.health_bar_color_background = (0, 0, 0)
        self.health_bar_color_foreground = (255, 0, 0)
        self.health_bar_color_outline = (255, 255, 255)
        self.max_health = 100

        if not Enemy.loaded_frames:
            self.right_walk_animation()
            self.right_attack_animation()
            Enemy.loaded_frames = True
        self.self_load_animations()

        self.rect = self.image.get_rect()
        self.direction = Enemy.LEFT
        self.speed = 3
        self.chasing = False
        self.damage = damage
        self.coolDown = 10
        self.placed = False
        self.collision_set = False

        r = random.Random()
        x = r.randint(1000, 9999)
        while x in MazeEnvironment.ENEMY_IDS:
            x = r.randint(1000, 9999)
        self.unique_id = x + pygame.USEREVENT
        MazeEnvironment.ENEMY_IDS.append(self.unique_id)

    def chase_player(self):
        # move in the direction of the player if not already next to them
        px = game.GameEnvironment.PLAYER.x
        py = game.GameEnvironment.PLAYER.y
        player_to_left = px + game.GameEnvironment.PLAYER.width < self.x + self.buffer
        player_to_right = px > self.x + self.width - self.buffer 
        player_above = py + game.GameEnvironment.PLAYER.height < self.y + self.buffer
        player_below = py > self.y + self.height - self.buffer
        if player_above:
            self.y -= self.speed
        elif player_below:
            self.y += self.speed

        if player_to_right:
            self.x += self.speed
            self.direction = True
        elif player_to_left:
            self.x -= self.speed
            self.direction = False

    def tick(self):
        # calculate if player is visible
        px = game.GameEnvironment.PLAYER.x
        py = game.GameEnvironment.PLAYER.y
        lineofsight = self.y < py + game.GameEnvironment.PLAYER.height < self.y + self.height or self.y < py < self.y + self.height
        player_to_left = px < self.x
        player_to_right = px > self.x + self.width
        in_range_x = (max(self.x, px) - min(self.x, px) - self.width  * 2) < MazeEnvironment.TILE_SIZE
        in_range_y = (max(self.y, py) - min(self.y, py) - self.height * 2) < MazeEnvironment.TILE_SIZE

        self.is_player_in_view = lineofsight and (player_to_left if self.direction == Enemy.LEFT else player_to_right) and in_range_x and in_range_y
        if self.is_player_in_view:
            self.chasing = True

        if self.chasing:
            self.chase_player()

        # update rect based on any changes to actual x/y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.player_in_combat_range:
            self.attack()

    def change_sprite(self):
        if self.sprite_counter >= len(self.sprite_modes[int(self.sprite_mode)]) - 2:
            self.sprite_counter = 0
        else:
            self.sprite_counter += 0.5       

    def render(self, surface):
        if self.chasing:
            if self.attack_animation == 1:
                self.sprite_mode = 2
                self.change_sprite()
                if self.direction:
                    surface.blit(self.sprites_right_attack[int(self.sprite_counter)], (self.x, self.y))
                else:
                    surface.blit(self.sprites_left_attack[int(self.sprite_counter)], (self.x, self.y))
                if self.sprite_counter == len(self.sprites_right_attack) - 2:
                    self.attack_animation = 0

            elif self.player_in_combat_range:
                if self.direction:
                    surface.blit(self.image, (self.x, self.y))
                else:
                    surface.blit(self.image2, (self.x, self.y))
                
            else:
                self.sprite_mode = 1
                self.change_sprite()
                if self.direction:
                    surface.blit(self.sprites_right_walk[int(self.sprite_counter)], (self.x, self.y))
                else:
                    surface.blit(self.sprites_left_walk[int(self.sprite_counter)], (self.x, self.y))
        else:
            if self.direction:
                surface.blit(self.image, (self.x, self.y))
            else:
                surface.blit(self.image2, (self.x, self.y))

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

        precalcw = int((self.health / self.max_health) * w) - (o * 2)
        if precalcw < 0:
            precalcw = 0
        foreground = pygame.Surface((precalcw, h - (o * 2)))
        foreground.convert()
        foreground.fill(self.health_bar_color_foreground)
        self.health_bar_surface.blit(foreground, (o, o))
        surface.blit(self.health_bar_surface, (self.x + int(w / 2), self.y - h - 4))

    def self_load_animations(self):
        for i in range(len(Enemy.enemy_walk_frames)):
            self.sprites_right_walk.append(Enemy.enemy_walk_frames[i])
        for i in range(len(Enemy.enemy_attack_frames)):
            self.sprites_right_attack.append(Enemy.enemy_attack_frames[i])
        for i in range(len(Enemy.enemy_walk_frames_left)):
            self.sprites_left_walk.append(Enemy.enemy_walk_frames_left[i])
        for i in range(len(Enemy.enemy_attack_frames_left)):
            self.sprites_left_attack.append(Enemy.enemy_attack_frames_left[i])

    def right_walk_animation(self):
        for i in range(0, 18):
            s = str(i)
            if i < 10:
                s = "0" + s
            img = pygame.image.load("src/sprites/Enemies/Walking/Minotaur_01_Walking_0" + s + ".png")
            Enemy.enemy_walk_frames.append(img)
            Enemy.enemy_walk_frames_left.append(pygame.transform.flip(img, True, False))

    def right_attack_animation(self):
        for i in range(0, 12):
            s = str(i)
            if i < 10:
                s = "0" + s
            img = pygame.image.load("src/sprites/Enemies/Walking/Minotaur_01_Walking_0" + s + ".png")
            Enemy.enemy_attack_frames.append(img)
            Enemy.enemy_attack_frames_left.append(pygame.transform.flip(img, True, False))

    def attack(self):
        if not self.weapon.in_cooldown:
            self.attack_animation = 1
            # start cooldown timer
            pygame.time.set_timer(self.unique_id, self.weapon.cooldown * 1000)
            self.weapon.in_cooldown = True
            # do the actual damage to all enemies in range
            game.GameEnvironment.PLAYER.take_damage(self.damage)
