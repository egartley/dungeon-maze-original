from multiprocessing.dummy import Array
import pygame
import booster
import game
import weapon
import math
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

    # unique event ids
    ATTACK_EVENT_ID = pygame.USEREVENT + 74
    SWORD_SWING_EVENT_ID = pygame.USEREVENT + 75

    def __init__(self, name=None, gender=None):
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
        self.weapon = None
        if name is not None:
            self.weapon = weapon.Sword()

        self.speed = 4
        self.speedStackLen = 3
        self.speedStackCount = 0
        self.speedStackTop = -1
        self.speedStackLast = -1
        self.speedInstances = [None] * self.speedStackLen
        self.speedStack = [False] * self.speedStackLen

        self.attack = 1
        self.attackStackLen = 3
        self.attackStackCount = 0
        self.attackStackTop = 0
        self.attackStackLast = 0
        self.attackInstances = [False] * self.attackStackLen
        self.attackStack = [False] * self.attackStackLen

        self.width = 192 / 4
        self.height = 285 / 4
        self.combat_rect = pygame.Rect(0, 0, 0, 0)
        self.active_booster = [False] * 2 # 0 for attack 1 for speed
        self.gender = gender
        self.direction = None
        self.image = pygame.image.load("Wraith_01_Idle_000.png")
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

    def apply_booster(self, b):
        if isinstance(b, booster.HealthBooster):
            self.health += booster.HealthBooster.increase
            
        elif isinstance(b, booster.SpeedBooster) and not self.isSpeedFull():
            self.speed = int (math.ceil(self.speed * booster.SpeedBooster.increase))
            MazeEnvironment.SPEED = int(math.ceil(MazeEnvironment.SPEED * booster.SpeedBooster.increase))
            self.active_booster[1] = True
            self.speedStackTop += 1
            self.speedStack[self.speedStackTop % self.speedStackLen] = True
            self.speedInstances[self.speedStackTop % self.speedStackLen] = b
            pygame.time.set_timer( (booster.SpeedBooster.BOOSTERID + (self.speedStackTop % self.speedStackLen)), b.time * 1000)
            
        elif isinstance(b, booster.AttackBooster) and not self.isAttackFull():
            self.attack_multiplier += booster.AttackBooster.increase
            self.active_booster[0] = True
            self.attackStackTop += 1
            self.attackStack[self.attackStackTop % self.attackStackLen] = True
            self.attackInstances[self.attackStackTop % self.attackStackLen] = b
            pygame.time.set_timer( ( booster.AttackBooster.BOOSTERID + (self.attackStackTop % self.attackStackLen)), b.time * 1000)
            
        elif isinstance(b, booster.ShieldBooster):
            self.shield += b.increase
            
        elif isinstance(b, booster.ArrowBooster):
            self.arrow_count += b.increase

    def isSpeedFull(self):
        i = 0
        for i in range(len(self.speedStack)):
            if self.speedStack[i] != True:
                return False
            i+=1
        return True
    
    def isSpeedEmpty(self):
        i = 0
        for i in range(len(self.speedStack)):
            if self.speedStack[i] != False:
                return False
            i+=1
        return True
    
    
    def isAttackFull(self):
        i = 0
        for i in range(len(self.attackStack)):
            if self.attackStack[i] != True:
                return False
            i+=1
        return True
    
    def isAttackEmpty(self):
        i = 0
        for i in range(len(self.attackStack)):
            if self.speedStack[i] != False:
                return False
            i+=1
        return True

    def cancel_active_booster(self,boosterID): 
        if self.active_booster[0] == True:
            self.attack_multiplier -= booster.AttackBooster.increase
            self.attackStack[self.attackStackLast % self.attackStackLen] = False
            self.attackInstances[self.attackStackLast % self.attackStackLen] = None
            pygame.time.set_timer( boosterID , 0)
            self.attackStackLast += 1
            if self.isAttackEmpty():
                self.active_booster[0] = False
        elif self.active_booster[1] == True:
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
        weapon_group = pygame.sprite.Group()
        if pygame.mouse.get_pos()[0] >= (self.x + (self.width/2)):
            self.weapon.directionSprite(self.x + 30, self.y + 15, "right")
            weapon_group.add(self.weapon)
            self.combat_rect = pygame.Rect(self.x + 40 - self.weapon.range, self.y + 10 - self.weapon.range,
                                    self.width + (self.weapon.range * 2), self.height - 10 + (self.weapon.range * 2))
            if self.weapon.is_animating == False:
                weapon_group.draw(surface)
            if self.swinging_sword:
                self.weapon.render(surface, self.x + 30, self.y + 15, "right")
                weapon_group.draw(surface)

        elif pygame.mouse.get_pos()[0] < (self.x + (self.width/2)):
            self.weapon.directionSprite(self.x - 82, self.y + 15, "left")
            weapon_group.add(self.weapon)
            self.combat_rect = pygame.Rect(self.x - 40 - self.weapon.range, self.y + 10 - self.weapon.range,
                                    self.width + (self.weapon.range * 2), self.height - 10+ (self.weapon.range * 2))
            if self.weapon.is_animating == False:
                weapon_group.draw(surface)
            if self.swinging_sword:
                self.weapon.render(surface, self.x - 82, self.y + 15, "left")
                weapon_group.draw(surface)


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
        if self.shield >= damage:
            self.shield -= damage
        elif self.shield > 0:
            damage_remaining = self.shield - damage
            self.shield = 0
            self.health -= damage_remaining
        else:
            self.health -=damage


class Enemy(Character):
    # constants for the direction the enemy is facing for use in "seeing" the player
    LEFT = 0
    RIGHT = 1

    def __init__(self):
        super().__init__()
        self.weapon_type = None
        self.is_player_in_view = False
        self.player_in_combat_range = False
        self.width = 180
        self.height = 123
        self.image = pygame.image.load("Minotaur_01_Idle_000.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.sprite = self.image
        self.rect = self.image.get_rect()
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
            self.sprite = self.image
        elif player_to_left:
            self.x -= self.speed
            self.sprite = pygame.transform.flip(self.image, True, False)




    def tick(self):
        # calculate if player is visible
        px = game.GameEnvironment.PLAYER.x
        py = game.GameEnvironment.PLAYER.y
        lineofsight = self.y < py + game.GameEnvironment.PLAYER.height < self.y + self.height or self.y < py < self.y + self.height
        player_to_left = px < self.x
        player_to_right = px > self.x + self.width
        in_range_x = (max(self.x, px) - min(self.x, px) - self.width  * 2) < MazeEnvironment.TILE_SIZE
        in_range_y = (max(self.y, py) - min(self.y, py) - self.height * 2) < MazeEnvironment.TILE_SIZE
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
        self.combat_rect = pygame.Rect(self.x - self.weapon.range, self.y - self.weapon.range,
                                       self.width + (self.weapon.range * 2), self.height + (self.weapon.range * 2))
        
        if self.player_in_combat_range:
            self.attack()

    def render(self, surface):
        if (self.direction):
            surface.blit(self.sprite, (self.x, self.y))
        else:
            surface.blit(self.sprite, (self.x, self.y))

        # health bar (keep?)
        w = (self.health / 100) * self.width
        if w < 0:
            w = 0

    def attack(self):
        game.GameEnvironment.PLAYER.take_damage(10)
