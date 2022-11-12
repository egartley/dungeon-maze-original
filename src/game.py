import sys

import pygame.mouse

import collision
from character import *
from screen import Screen


class GameEnvironment:
    # constants for keeping track of the game state
    START_STATE = 0
    INGAME_STATE = 1
    PAUSE_STATE = 2
    VICTORY_STATE = 3
    DEATH_STATE = 4

    PLAYER = MainCharacter()
    BOY = 0
    GIRL = 1

    # constants for differing between difficulties
    DIFFICULTY_EASY = 0
    DIFFICULTY_MEDIUM = 1
    DIFFICULTY_HARD = 2

    # assuming only one booster with a timer is active at a time, unique event id for it
    BOOSTER_EVENT_ID = pygame.USEREVENT + 9

    def __init__(self, screen_width, screen_height, ):
        # set to easy (currently no effect) for now since there's no selection yet
        self.maze_difficulty = GameEnvironment.DIFFICULTY_EASY
        self.enemy_difficulty = GameEnvironment.DIFFICULTY_EASY
        self.maze_environment = MazeEnvironment(self)
        # set default player values for testing, since no selection yet
        self.player_gender = GameEnvironment.BOY
        self.player_name = ""
        GameEnvironment.state = GameEnvironment.START_STATE
        self.screen = Screen(self.maze_environment, screen_width, screen_height)
        self.display_surface = pygame.display.set_mode((self.screen.width, self.screen.height))
        self.boosters = []
        self.booster_collisions = []
        self.enemies = []
        self.enemy_collisions = []
        self.active_combat_collisions = []

    def set_booster_collisions(self):
        for b in self.boosters:
            booster = b[0]
            c = collision.BoosterCollision(booster, GameEnvironment.PLAYER.rect)
            self.booster_collisions.append(c)

    def set_enemy_collisions(self):
        for e in self.enemies:
            c = collision.EnemyCollision(e[0], GameEnvironment.PLAYER.combat_rect)
            self.enemy_collisions.append(c)

    def start_ingame(self):
        # reset variables for when restarting from win/death
        self.boosters = []
        self.booster_collisions = []
        self.enemies = []
        self.enemy_collisions = []
        self.active_combat_collisions = []
        MazeEnvironment.SPEED = 4
        GameEnvironment.PLAYER = MainCharacter(GameEnvironment.PLAYER.name, GameEnvironment.PLAYER.gender)
        # default values for testing
        self.maze_difficulty = GameEnvironment.DIFFICULTY_MEDIUM
        self.enemy_difficulty = GameEnvironment.DIFFICULTY_MEDIUM
        self.player_name = "Player"
        self.player_gender = GameEnvironment.BOY
        GameEnvironment.PLAYER = MainCharacter(self.player_name, self.player_gender)
        self.maze_environment.generate_maze(4, 8, self.maze_difficulty)
        self.maze_environment.generate_boosters()
        self.maze_environment.generate_enemies()
        # put player at maze start, calculate all coords
        # relative = absolute - maze
        start = MazeEnvironment.MAZE.start
        pos = self.maze_environment.get_player_pos(start[1], start[0])
        GameEnvironment.PLAYER.relative_x = pos[0]
        GameEnvironment.PLAYER.relative_y = pos[1]
        if start[0] == 0:
            MazeEnvironment.MAP_Y = 0
            MazeEnvironment.MAP_X = -1 * (MazeEnvironment.TILE_SIZE * start[1]) + (MazeEnvironment.TILE_SIZE / 2)
        elif start[1] == 0:
            MazeEnvironment.MAP_X = 0
            MazeEnvironment.MAP_Y = -1 * (MazeEnvironment.TILE_SIZE * start[0]) + (MazeEnvironment.TILE_SIZE / 4)
        elif start[0] == len(MazeEnvironment.MAZE.grid) - 1:
            MazeEnvironment.MAP_Y = -1 * (MazeEnvironment.PIXEL_HEIGHT - self.screen.height)
            MazeEnvironment.MAP_X = -1 * (MazeEnvironment.TILE_SIZE * start[1]) + (MazeEnvironment.TILE_SIZE / 2)
        else:
            MazeEnvironment.MAP_X = -1 * (MazeEnvironment.PIXEL_WIDTH - self.screen.width)
            MazeEnvironment.MAP_Y = -1 * (MazeEnvironment.TILE_SIZE * start[0]) + (MazeEnvironment.TILE_SIZE / 4)
        GameEnvironment.PLAYER.x = GameEnvironment.PLAYER.relative_x + MazeEnvironment.MAP_X
        GameEnvironment.PLAYER.y = GameEnvironment.PLAYER.relative_y + MazeEnvironment.MAP_Y
        # set boosters
        self.maze_environment.place_boosters()
        self.set_booster_collisions()
        # set enemies
        self.maze_environment.place_enemies()
        self.set_enemy_collisions()

    def on_enemy_death(self, enemy):
        # when an enemy is killed, remove them and their collision(s)
        remove = None
        for c in self.active_combat_collisions:
            if c.enemy == enemy:
                remove = c
        if remove is not None:
            self.active_combat_collisions.remove(remove)
        remove = None
        for c in self.enemy_collisions:
            if c.enemy == enemy:
                remove = c
        if remove is not None:
            self.enemy_collisions.remove(remove)
        remove = None
        for e in self.enemies:
            if e == enemy:
                remove = e
        if remove is not None:
            self.enemies.remove(remove)

    def check_wall(self, x, y):
        # check if there is a wall at the given x/y
        r = int(y // MazeEnvironment.TILE_SIZE)
        c = int(x // MazeEnvironment.TILE_SIZE)
        if r >= len(MazeEnvironment.MAZE.grid) or c >= len(MazeEnvironment.MAZE.grid[0]):
            return True
        return MazeEnvironment.MAZE.grid[r][c] == MazeEnvironment.WALL

    def camera_tick(self):
        # all the yucky math for controlling the "camera"
        s = pygame.display.get_window_size()
        px = GameEnvironment.PLAYER.x
        py = GameEnvironment.PLAYER.y
        ps = GameEnvironment.PLAYER.speed
        pw = GameEnvironment.PLAYER.width
        ph = GameEnvironment.PLAYER.height
        GameEnvironment.PLAYER.at_center_x = abs(px - ((s[0] / 2) - (pw / 2))) <= ps
        GameEnvironment.PLAYER.at_center_y = abs(py - ((s[1] / 2) - (ph / 2))) <= ps
        GameEnvironment.PLAYER.relative_x = GameEnvironment.PLAYER.x - MazeEnvironment.MAP_X
        GameEnvironment.PLAYER.relative_y = GameEnvironment.PLAYER.y - MazeEnvironment.MAP_Y

        p = GameEnvironment.PLAYER
        MazeEnvironment.CAN_MOVE_UP = MazeEnvironment.MAP_Y < 0 and p.at_center_y and \
                                      not self.check_wall(p.relative_x,
                                                          p.relative_y - MazeEnvironment.SPEED) and \
                                      not self.check_wall(p.relative_x + p.width,
                                                          p.relative_y - MazeEnvironment.SPEED)
        MazeEnvironment.CAN_MOVE_DOWN = MazeEnvironment.MAP_Y > (-1 * MazeEnvironment.PIXEL_HEIGHT) + s[1] and \
                                        p.at_center_y and \
                                        not self.check_wall(p.relative_x,
                                                            p.relative_y + p.height + MazeEnvironment.SPEED) and \
                                        not self.check_wall(p.relative_x + p.width,
                                                            p.relative_y + p.height + MazeEnvironment.SPEED)
        MazeEnvironment.CAN_MOVE_LEFT = MazeEnvironment.MAP_X < 0 and p.at_center_x and \
                                        not self.check_wall(p.relative_x - MazeEnvironment.SPEED,
                                                            p.relative_y) and \
                                        not self.check_wall(p.relative_x - MazeEnvironment.SPEED,
                                                            p.relative_y + p.height)
        MazeEnvironment.CAN_MOVE_RIGHT = MazeEnvironment.MAP_X > (-1 * MazeEnvironment.PIXEL_WIDTH) + s[0] and \
                                         p.at_center_x and \
                                         not self.check_wall(p.relative_x + p.width + MazeEnvironment.SPEED,
                                                             p.relative_y) and \
                                         not self.check_wall(p.relative_x + p.width + MazeEnvironment.SPEED,
                                                             p.relative_y + p.height)

        blocked_up = self.check_wall(p.relative_x, p.relative_y - p.speed) or \
                     self.check_wall(p.relative_x + p.width, p.relative_y - p.speed)
        blocked_down = self.check_wall(p.relative_x, p.relative_y + p.height + p.speed) or \
                       self.check_wall(p.relative_x + p.width, p.relative_y + p.height + p.speed)
        blocked_left = self.check_wall(p.relative_x - p.speed, p.relative_y) or \
                       self.check_wall(p.relative_x - p.speed, p.relative_y + p.height)
        blocked_right = self.check_wall(p.relative_x + p.width + p.speed, p.relative_y) or \
                        self.check_wall(p.relative_x + p.width + p.speed, p.relative_y + p.height)
        GameEnvironment.PLAYER.blocked = (blocked_up, blocked_down, blocked_left, blocked_right)

    def tick(self):
        if GameEnvironment.state == GameEnvironment.INGAME_STATE:
            self.camera_tick()
            self.maze_environment.tick()
            GameEnvironment.PLAYER.tick()

            # after maze and player ticks, check all collisions
            for c in self.booster_collisions:
                c.tick(c.booster.rect, GameEnvironment.PLAYER.rect)
            to_remove = []
            for c in self.booster_collisions:
                c.check()
                if c.is_collided:
                    c.collision_occurrence()
                    to_remove.append(c)
            for r in to_remove:
                self.maze_environment.remove_booster(r.booster)
                self.booster_collisions.remove(r)

            for c in self.enemy_collisions:
                c.tick(c.enemy.rect, GameEnvironment.PLAYER.combat_rect)
                c.check()
                if c.is_collided and c not in self.active_combat_collisions:
                    c.collision_occurrence()
                    self.active_combat_collisions.append(c)
                if not c.is_collided and c in self.active_combat_collisions:
                    c.collision_end()
                    self.active_combat_collisions.remove(c)

            # dirty way to check for enemy death
            for e in self.enemies:
                if e[0].health <= 0:
                    self.on_enemy_death(e)

            if GameEnvironment.PLAYER.tile_pos[0] == MazeEnvironment.MAZE.end[0] and GameEnvironment.PLAYER.tile_pos[1] == MazeEnvironment.MAZE.end[1]:
                GameEnvironment.state = GameEnvironment.VICTORY_STATE

    def render(self, surface):
        background = pygame.Surface((self.screen.width, self.screen.height))
        background.convert()
        background.fill((0, 0, 0))
        surface.blit(background, (0, 0))
        # based on the game state, call a different method from the screen
        if GameEnvironment.state == GameEnvironment.START_STATE:
            self.screen.startView()
        elif GameEnvironment.state == GameEnvironment.INGAME_STATE:
            self.screen.activeGameView()
        elif GameEnvironment.state == GameEnvironment.PAUSE_STATE:
            self.screen.pauseView()
        elif GameEnvironment.state == GameEnvironment.VICTORY_STATE:
            self.screen.victory()
        elif GameEnvironment.state == GameEnvironment.DEATH_STATE:
            self.screen.death()

    def switch_to_ingame(self):
        GameEnvironment.state = GameEnvironment.INGAME_STATE
        self.start_ingame()

    def event_handler(self, event):
        # this handles all keyboard and mouse input, as well as timers
        if GameEnvironment.state == GameEnvironment.START_STATE:
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                self.switch_to_ingame()
        elif GameEnvironment.state == GameEnvironment.INGAME_STATE:
            if event.type == booster.AttackBooster.BOOSTERID + (GameEnvironment.PLAYER.attackStackLast % GameEnvironment.PLAYER.attackStackLen):
                GameEnvironment.PLAYER.cancel_active_booster( booster.AttackBooster.BOOSTERID + (GameEnvironment.PLAYER.attackStackLast % GameEnvironment.PLAYER.attackStackLen))
            if event.type == booster.SpeedBooster.BOOSTERID + (GameEnvironment.PLAYER.speedStackLast % GameEnvironment.PLAYER.speedStackLen):
                GameEnvironment.PLAYER.cancel_active_booster( booster.SpeedBooster.BOOSTERID + (GameEnvironment.PLAYER.speedStackLast % GameEnvironment.PLAYER.speedStackLen)) 
            if event.type == MainCharacter.ATTACK_EVENT_ID:
                GameEnvironment.PLAYER.weapon.in_cooldown = False
                pygame.time.set_timer(MainCharacter.ATTACK_EVENT_ID, 0)
            if event.type == MainCharacter.SWORD_SWING_EVENT_ID:
                GameEnvironment.PLAYER.swinging_sword = False
                pygame.time.set_timer(MainCharacter.SWORD_SWING_EVENT_ID, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    GameEnvironment.PLAYER.attack_motion()
                if event.button == 3:
                    GameEnvironment.PLAYER.shoot(pygame.mouse.get_pos())
                    GameEnvironment.PLAYER.is_using_bow = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.maze_environment.up = True
                    GameEnvironment.PLAYER.up = True
                elif event.key == pygame.K_a:
                    self.maze_environment.left = True
                    GameEnvironment.PLAYER.left = True
                elif event.key == pygame.K_s:
                    self.maze_environment.down = True
                    GameEnvironment.PLAYER.down = True
                elif event.key == pygame.K_d:
                    self.maze_environment.right = True
                    GameEnvironment.PLAYER.right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.maze_environment.up = False
                    GameEnvironment.PLAYER.up = False
                elif event.key == pygame.K_a:
                    self.maze_environment.left = False
                    GameEnvironment.PLAYER.left = False
                elif event.key == pygame.K_s:
                    self.maze_environment.down = False
                    GameEnvironment.PLAYER.down = False
                elif event.key == pygame.K_d:
                    self.maze_environment.right = False
                    GameEnvironment.PLAYER.right = False
                elif event.key == pygame.K_ESCAPE:
                    GameEnvironment.state = GameEnvironment.PAUSE_STATE
                elif event.key == pygame.K_v:
                    GameEnvironment.state = GameEnvironment.VICTORY_STATE
                elif event.key == pygame.K_k:
                    GameEnvironment.state = GameEnvironment.DEATH_STATE
        elif GameEnvironment.state == GameEnvironment.PAUSE_STATE:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                GameEnvironment.state = GameEnvironment.INGAME_STATE
        elif GameEnvironment.state == GameEnvironment.VICTORY_STATE or GameEnvironment.state == GameEnvironment.DEATH_STATE:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    self.switch_to_ingame()
