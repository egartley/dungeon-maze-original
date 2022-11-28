import sys
import collision
import pygame.mouse
from character import *
from screen import Screen
#from scores import Score


def get_player_pos(r, c):
    return MazeEnvironment.TILE_SIZE * r + (MazeEnvironment.TILE_SIZE / 2 - GameEnvironment.PLAYER.width / 2), \
           MazeEnvironment.TILE_SIZE * c + (MazeEnvironment.TILE_SIZE / 2 - GameEnvironment.PLAYER.height / 2)


class GameEnvironment:
    # constants for keeping track of the game state
    START_STATE = 0
    INGAME_STATE = 1
    PAUSE_STATE = 2
    VICTORY_STATE = 3
    DEATH_STATE = 4
    state = -1

    PLAYER = MainCharacter()
    BOY = 0
    GIRL = 1

    # constants for differing between difficulties
    DIFFICULTY_EASY = 0
    DIFFICULTY_MEDIUM = 1
    DIFFICULTY_HARD = 2
    DIFFICULTY_TRACKER = -1

    # assuming only one booster with a timer is active at a time, unique event id for it
    BOOSTER_EVENT_ID = pygame.USEREVENT + 9

    def __init__(self, screen_width, screen_height):
        self.maze_environment = MazeEnvironment(self)
        # set default player values for testing, since no selection yet
        self.player_gender = GameEnvironment.BOY
        GameEnvironment.state = GameEnvironment.START_STATE
        self.screen = Screen(self.maze_environment, screen_width, screen_height)
        self.display_surface = pygame.display.set_mode((self.screen.width, self.screen.height))
        self.boosters = []
        self.booster_collisions = []
        self.enemies = []
        self.enemy_collisions = []
        self.active_combat_collisions = []
        self.player_name = self.screen.CHARONE + self.screen.CHARTWO + self.screen.CHARTHREE
        #self.score = Score(self.player_name)

    def set_arrow_collisions(self):
        for a in self.PLAYER.arrow_group:
            for e in range(len(self.enemies)):
                arrow_collision = collision.ArrowCollision(a, self.enemies[e][0])
                arrow_collision.check()
                if arrow_collision.is_collided:
                    self.enemies[e][0].health -= GameEnvironment.PLAYER.bow.damage
                    self.enemies[e][0].force_chase = True
                    a.self_destruct()

    def set_booster_collisions(self):
        for b in self.boosters:
            booster = b[0]
            if booster.collision_set:
                continue
            booster.collision_set = True
            c = collision.BoosterCollision(booster, GameEnvironment.PLAYER.rect)
            self.booster_collisions.append(c)

    def set_enemy_collisions(self):
        for e in self.enemies:
            enemy = e[0]
            if enemy.collision_set:
                continue
            enemy.collision_set = True
            c = collision.EnemyCollision(e[0], GameEnvironment.PLAYER.rect)
            self.enemy_collisions.append(c)

    def start_ingame(self):
        # reset variables for when restarting from win/death
        if len(self.enemies) > 0:
            # ensure animation timers for left over enemies are stopped
            for e in self.enemies:
                e[0].on_death()
        self.boosters = []
        self.booster_collisions = []
        self.enemies = []
        self.enemy_collisions = []
        self.active_combat_collisions = []
        MazeEnvironment.SPEED = 4
        self.maze_environment.reset()
        
        self.player_name = self.screen.CHARONE + self.screen.CHARTWO + self.screen.CHARTHREE
        GameEnvironment.PLAYER = MainCharacter(self.player_name)
        self.maze_environment.generate_maze_difficulty()
        # put player at maze start, calculate all coords
        # relative = absolute - maze
        start = MazeEnvironment.MAZE.start
        pos = get_player_pos(start[1], start[0])
        GameEnvironment.PLAYER.relative_x = pos[0]
        GameEnvironment.PLAYER.relative_y = pos[1]
        if start[0] == 0:
            MazeEnvironment.MAP_Y = 0
            MazeEnvironment.MAP_X = -1 * (MazeEnvironment.TILE_SIZE * start[1]) + ((pygame.display.get_window_size()[0] / 2) - (MazeEnvironment.TILE_SIZE / 2))
        elif start[1] == 0:
            MazeEnvironment.MAP_X = 0
            MazeEnvironment.MAP_Y = -1 * (MazeEnvironment.TILE_SIZE * start[0]) + ((pygame.display.get_window_size()[1] / 2) - (MazeEnvironment.TILE_SIZE / 2))
        elif start[0] == len(MazeEnvironment.MAZE.grid) - 1:
            MazeEnvironment.MAP_Y = -1 * (MazeEnvironment.PIXEL_HEIGHT - self.screen.height)
            MazeEnvironment.MAP_X = -1 * (MazeEnvironment.TILE_SIZE * start[1]) + ((pygame.display.get_window_size()[0] / 2) - (MazeEnvironment.TILE_SIZE / 2))
        else:
            MazeEnvironment.MAP_X = -1 * (MazeEnvironment.PIXEL_WIDTH - self.screen.width)
            MazeEnvironment.MAP_Y = -1 * (MazeEnvironment.TILE_SIZE * start[0]) + ((pygame.display.get_window_size()[1] / 2) - (MazeEnvironment.TILE_SIZE / 2))
        GameEnvironment.PLAYER.x = GameEnvironment.PLAYER.relative_x + MazeEnvironment.MAP_X
        GameEnvironment.PLAYER.y = GameEnvironment.PLAYER.relative_y + MazeEnvironment.MAP_Y

    def on_enemy_death(self, enemy):
        enemy.on_death()
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
            if e[0] == enemy:
                remove = e
        if remove is not None:
            self.enemies.remove(remove)
        MazeEnvironment.ENEMY_EVENT_IDS.remove(enemy.unique_id)
        self.screen.score.update_kill()

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
        p = GameEnvironment.PLAYER
        px = p.x
        py = p.y
        ps = p.speed
        pw = p.width
        ph = p.height
        pr = p.rect
        p.at_center_x = abs(px - ((s[0] / 2) - (pw / 2))) <= ps
        p.at_center_y = abs(py - ((s[1] / 2) - (ph / 2))) <= ps
        p.relative_x = px - MazeEnvironment.MAP_X
        p.relative_y = py - MazeEnvironment.MAP_Y

        pnm = (pr.move(0, -1 * ps * 2), pr.move(0, ps * 2), pr.move(-1 * ps * 2, 0), pr.move(ps * 2, 0))
        enemy_block = [False, False, False, False]
        for e in self.enemies:
            for i in range(4):
                if enemy_block[i]:
                    continue
                enemy_block[i] = pnm[i].colliderect(e[0].collision_rect)

        MazeEnvironment.CAN_MOVE_UP = MazeEnvironment.MAP_Y < 0 and p.at_center_y and \
                                      not self.check_wall(p.relative_x,
                                                          p.relative_y - MazeEnvironment.SPEED) and \
                                      not self.check_wall(p.relative_x + p.width,
                                                          p.relative_y - MazeEnvironment.SPEED) and not enemy_block[0]
        MazeEnvironment.CAN_MOVE_DOWN = MazeEnvironment.MAP_Y > (-1 * MazeEnvironment.PIXEL_HEIGHT) + s[1] and \
                                        p.at_center_y and \
                                        not self.check_wall(p.relative_x,
                                                            p.relative_y + p.height + MazeEnvironment.SPEED) and \
                                        not self.check_wall(p.relative_x + p.width,
                                                            p.relative_y + p.height + MazeEnvironment.SPEED) and \
                                        not enemy_block[1]
        MazeEnvironment.CAN_MOVE_LEFT = MazeEnvironment.MAP_X < 0 and p.at_center_x and \
                                        not self.check_wall(p.relative_x - MazeEnvironment.SPEED,
                                                            p.relative_y) and \
                                        not self.check_wall(p.relative_x - MazeEnvironment.SPEED,
                                                            p.relative_y + p.height) and not enemy_block[2]
        MazeEnvironment.CAN_MOVE_RIGHT = MazeEnvironment.MAP_X > (-1 * MazeEnvironment.PIXEL_WIDTH) + s[0] and \
                                         p.at_center_x and \
                                         not self.check_wall(p.relative_x + p.width + MazeEnvironment.SPEED,
                                                             p.relative_y) and \
                                         not self.check_wall(p.relative_x + p.width + MazeEnvironment.SPEED,
                                                             p.relative_y + p.height) and not enemy_block[3]

        blocked_up = self.check_wall(p.relative_x, p.relative_y - ps) or \
                     self.check_wall(p.relative_x + pw, p.relative_y - ps) or enemy_block[0]
        blocked_down = self.check_wall(p.relative_x, p.relative_y + ph + ps) or \
                       self.check_wall(p.relative_x + pw, p.relative_y + ph + ps) or enemy_block[1]
        blocked_left = self.check_wall(p.relative_x - ps, p.relative_y) or \
                       self.check_wall(p.relative_x - ps, p.relative_y + ph) or enemy_block[2]
        blocked_right = self.check_wall(p.relative_x + pw + ps, p.relative_y) or \
                        self.check_wall(p.relative_x + pw + ps, p.relative_y + ph) or enemy_block[3]

        # edge case for when in the start tile (ignore end tile for now)
        tp = p.tile_pos
        if len(tp) > 0 and MazeEnvironment.MAZE.grid[tp[0]][tp[1]] == MazeEnvironment.START:
            if self.maze_environment.start_direction == 1:
                blocked_left = blocked_left or px - ps < self.maze_environment.start_end_walls[0].get_width()
            elif self.maze_environment.start_direction == 2:
                blocked_up = blocked_up or py - ps < self.maze_environment.start_end_walls[1].get_height()
            elif self.maze_environment.start_direction == 3:
                blocked_right = blocked_right or px + pw + ps > s[0] - self.maze_environment.start_end_walls[2].get_width()
            elif self.maze_environment.start_direction == 4:
                blocked_down = blocked_down or py + ph + ps > s[1] - self.maze_environment.start_end_walls[3].get_height()

        p.blocked = (blocked_up, blocked_down, blocked_left, blocked_right)

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
                c.tick(c.enemy.rect, GameEnvironment.PLAYER.rect)
                c.check()
                if c.is_collided and c not in self.active_combat_collisions:
                    c.collision_occurrence()
                    self.active_combat_collisions.append(c)
                if not c.is_collided and c in self.active_combat_collisions:
                    c.collision_end()
                    self.active_combat_collisions.remove(c)
            # dirty way to check for enemy death
            for e in self.enemies:
                if e[0].health <= 0 and e[0].alive:
                    e[0].die()
            self.set_arrow_collisions()

            if GameEnvironment.PLAYER.tile_pos[0] == MazeEnvironment.MAZE.end[0] and MazeEnvironment.MAZE.end[1] == \
                    GameEnvironment.PLAYER.tile_pos[1]:
                tx = self.maze_environment.end_x + (MazeEnvironment.TILE_SIZE // 2) - \
                     (self.maze_environment.treasure_surface.get_width() // 2)
                ty = self.maze_environment.end_y + (MazeEnvironment.TILE_SIZE // 2) - \
                     (self.maze_environment.treasure_surface.get_height() // 2)
                tr = pygame.Rect(tx, ty, self.maze_environment.treasure_surface.get_width(),
                                 self.maze_environment.treasure_surface.get_height())
                if GameEnvironment.PLAYER.rect.colliderect(tr):
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
            #self.score.start_time()
            self.screen.activeGameView()
        elif GameEnvironment.state == GameEnvironment.PAUSE_STATE:
            self.screen.pauseView()
        elif GameEnvironment.state == GameEnvironment.VICTORY_STATE:
            #self.score.end_time()
            self.screen.victory()
        elif GameEnvironment.state == GameEnvironment.DEATH_STATE:
            #self.score.end_time()
            self.screen.death()

    def switch_to_ingame(self):
        GameEnvironment.state = GameEnvironment.INGAME_STATE
        self.start_ingame()

    def event_handler(self, event):
        # this handles all keyboard and mouse input, as well as timers
        if GameEnvironment.state == GameEnvironment.START_STATE:
            GameEnvironment.PLAYER.METH_COUNT = 0
            GameEnvironment.PLAYER.ATTACK_COUNT = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                easyButton = pygame.Rect(100, 350, 200, 60)
                mediumButton = pygame.Rect(375, 350, 200, 60)
                hardButton = pygame.Rect(675, 350, 200, 60)
                quitButton = pygame.Rect(375, 550, 200, 60)
                
                char_one = pygame.Rect(355, 160, 60, 60)
                char_two = pygame.Rect(435, 160, 60, 60)
                char_three = pygame.Rect(510.5, 160, 60, 60)
                if char_one.collidepoint(event.pos) and self.screen.CHARONE != chr(ord('Z')):
                    self.screen.CHARONE = chr(ord(self.screen.CHARONE)+1)
                elif char_one.collidepoint(event.pos) and self.screen.CHARONE == chr(ord('Z')):
                    self.screen.CHARONE = chr(ord(self.screen.CHARONE)-25)
                
                elif char_two.collidepoint(event.pos) and self.screen.CHARTWO != chr(ord('Z')):
                    self.screen.CHARTWO = chr(ord(self.screen.CHARTWO)+1)
                elif char_two.collidepoint(event.pos) and self.screen.CHARTWO == chr(ord('Z')):
                    self.screen.CHARTWO =  chr(ord(self.screen.CHARTWO)-25)
                    
                if char_three.collidepoint(event.pos) and self.screen.CHARTHREE != chr(ord('Z')):
                    self.screen.CHARTHREE = chr(ord(self.screen.CHARTHREE)+1)
                elif char_three.collidepoint(event.pos) and self.screen.CHARTHREE == chr(ord('Z')):
                    self.screen.CHARTHREE = chr(ord(self.screen.CHARTHREE)-25)
                
                if easyButton.collidepoint(event.pos):
                    GameEnvironment.DIFFICULTY_TRACKER = GameEnvironment.DIFFICULTY_EASY
                    self.switch_to_ingame()
                elif mediumButton.collidepoint(event.pos):
                    GameEnvironment.DIFFICULTY_TRACKER = GameEnvironment.DIFFICULTY_MEDIUM
                    self.switch_to_ingame()
                elif hardButton.collidepoint(event.pos):
                    GameEnvironment.DIFFICULTY_TRACKER = GameEnvironment.DIFFICULTY_HARD
                    self.switch_to_ingame()
                elif quitButton.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        elif GameEnvironment.state == GameEnvironment.INGAME_STATE:
            if event.type == booster.AttackBooster.BOOSTERID + (GameEnvironment.PLAYER.attackStackLast % GameEnvironment.PLAYER.attackStackLen):
                GameEnvironment.PLAYER.cancel_active_booster(booster.AttackBooster.BOOSTERID + (GameEnvironment.PLAYER.attackStackLast % GameEnvironment.PLAYER.attackStackLen))
            if event.type == booster.SpeedBooster.BOOSTERID + (GameEnvironment.PLAYER.speedStackLast % GameEnvironment.PLAYER.speedStackLen):
                GameEnvironment.PLAYER.cancel_active_booster(booster.SpeedBooster.BOOSTERID + (GameEnvironment.PLAYER.speedStackLast % GameEnvironment.PLAYER.speedStackLen))
            if event.type == MainCharacter.ATTACK_EVENT_ID:
                GameEnvironment.PLAYER.weapon.in_cooldown = False
                pygame.time.set_timer(MainCharacter.ATTACK_EVENT_ID, 0)
            if event.type == MainCharacter.SWORD_SWING_EVENT_ID:
                GameEnvironment.PLAYER.swinging_sword = False
                pygame.time.set_timer(MainCharacter.SWORD_SWING_EVENT_ID, 0)
            if event.type in MazeEnvironment.ENEMY_EVENT_IDS:
                is_animation = False
                for e in self.enemies:
                    enemy = e[0]
                    a = None
                    if event.type == enemy.walk_animation[0].event_id:
                        a = enemy.walk_animation[0]
                    elif event.type == enemy.walk_animation[1].event_id:
                        a = enemy.walk_animation[1]
                    elif event.type == enemy.attack_animation[0].event_id:
                        a = enemy.attack_animation[0]
                    elif event.type == enemy.attack_animation[1].event_id:
                        a = enemy.attack_animation[1]
                    elif event.type == enemy.death_animation[0].event_id:
                        a = enemy.death_animation[0]
                    elif event.type == enemy.death_animation[1].event_id:
                        a = enemy.death_animation[1]
                    if a is None:
                        continue
                    else:
                        is_animation = True
                        a.next_frame()
                        break
                if is_animation:
                    # don't set timer to 0 since animation class will handle that if needed
                    return
                # not an animation, assume attack cooldown
                for enemy in self.enemies:
                    if event.type == enemy[0].unique_id:
                        enemy[0].weapon.in_cooldown = False
                        break
                pygame.time.set_timer(event.type, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    GameEnvironment.PLAYER.attack_motion()
                if event.button == 1:
                    GameEnvironment.PLAYER.is_using_sword = True
                    GameEnvironment.PLAYER.is_using_bow = False
                if event.button == 3:
                    GameEnvironment.PLAYER.shoot(pygame.mouse.get_pos())
                    GameEnvironment.PLAYER.is_using_bow = True
                    GameEnvironment.PLAYER.is_using_sword = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m and Screen.SHOW_MAP == True:
                    Screen.SHOW_MAP = False
                elif event.key == pygame.K_m and Screen.SHOW_MAP == False:
                    Screen.SHOW_MAP = True
                elif event.key == pygame.K_w:
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
        elif GameEnvironment.state == GameEnvironment.PAUSE_STATE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                startButton = pygame.Rect(150, 550, 200, 60)
                quitButton = pygame.Rect(700, 550, 200, 60)
                # goes in if clicked = buttonrect.collidepoint(event.pos)
                if startButton.collidepoint(event.pos):
                    GameEnvironment.state = GameEnvironment.INGAME_STATE
                elif quitButton.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        elif GameEnvironment.state == GameEnvironment.VICTORY_STATE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                startButton = pygame.Rect(200,600,200,60)
                quitButton = pygame.Rect(575,600,200,60)
                if quitButton.collidepoint(event.pos): # check if button clicked quit
                    pygame.quit()
                    sys.exit()
                elif startButton.collidepoint(event.pos): # checck if click was restart
                    GameEnvironment.PLAYER.METH_COUNT = 0
                    GameEnvironment.PLAYER.ATTACK_COUNT = 0
                    self.switch_to_ingame()
        elif  GameEnvironment.state == GameEnvironment.DEATH_STATE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                startButton = pygame.Rect(200, 550, 200, 60)
                quitButton = pygame.Rect(605, 550, 200, 60)
                if quitButton.collidepoint(event.pos): # check if button clicked quit
                    pygame.quit()
                    sys.exit()
                elif startButton.collidepoint(event.pos): # checck if click was restart
                    GameEnvironment.PLAYER.METH_COUNT = 0
                    GameEnvironment.PLAYER.ATTACK_COUNT = 0
                    self.switch_to_ingame()
