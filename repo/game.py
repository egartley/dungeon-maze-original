import sys
import collision
import pygame.mouse
from character import *
from screen import Screen
from scores import Score


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
    MANUAL_STATE = 5
    PAUSE_MANUAL_STATE = 6
    CONTRIBUTOR_STATE = 7
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

    ALLOW_RESIZE = True

    def __init__(self, screen_width, screen_height):
        self.maze_environment = MazeEnvironment(self)
        # set default player values for testing, since no selection yet
        self.player_gender = GameEnvironment.BOY
        GameEnvironment.state = GameEnvironment.START_STATE
        self.display_surface = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE) if GameEnvironment.ALLOW_RESIZE \
            else pygame.display.set_mode((screen_width, screen_height))
        self.screen = Screen(self.maze_environment, screen_width, screen_height)
        self.click_sound = pygame.mixer.Sound(os.path.join('src', 'sounds', 'mixkit-explainer-video-game-alert-sweep-236.wav'))
        self.boosters = []
        self.booster_collisions = []
        self.enemies = []
        self.enemy_collisions = []
        self.active_combat_collisions = []
        self.player_name = self.screen.CHARONE + self.screen.CHARTWO + self.screen.CHARTHREE
        self.score = Score(self.player_name, GameEnvironment.DIFFICULTY_TRACKER)
        self.sw = 0
        self.sh = 0

    def set_arrow_collisions(self):
        for a in self.PLAYER.arrow_group:
            for e in range(len(self.enemies)):
                arrow_collision = collision.ArrowCollision(a, self.enemies[e][0])
                arrow_collision.check()
                if arrow_collision.is_collided:
                    arrow_hit = pygame.mixer.Sound(os.path.join('src', 'sounds', 'arrow_incoming_whoosh.mp3'))
                    pygame.mixer.Sound.play(arrow_hit)
                    self.enemies[e][0].health -= GameEnvironment.PLAYER.bow.damage * GameEnvironment.PLAYER.attack_multiplier
                    self.enemies[e][0].force_chase = True
                    a.self_destruct()
        for e in self.enemies:
            enemy = e[0]
            if (enemy.enemy_type == 1):
                for a in enemy.arrow_group:
                    arrow_collision = collision.ArrowCollision(a, self.PLAYER)
                    arrow_collision.check()
                    if arrow_collision.is_collided:
                        arrow_hit = pygame.mixer.Sound(os.path.join('src', 'sounds', 'arrow_incoming_whoosh.mp3'))
                        pygame.mixer.Sound.play(arrow_hit)
                        self.PLAYER.take_damage(enemy.damage)
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

    def attack_sword_sound(self):
        if not GameEnvironment.PLAYER.weapon.in_cooldown:
            if len(self.active_combat_collisions) != 0:
                splash = pygame.mixer.Sound(os.path.join('src', 'sounds', 'mixkit-sword-slash-swoosh.mp3'))
                pygame.mixer.Sound.play(splash)
            else:
                woosh = pygame.mixer.Sound(os.path.join('src', 'sounds', 'mixkit-dagger-woosh.wav'))
                pygame.mixer.Sound.play(woosh)

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
        self.screen.start_music = False
        self.screen.music_count = 0.0
        self.screen.score.player_score = 0.0
        self.screen.score.kill_count = 0
        self.screen.score.total = 0
        self.screen.score.total_multiplier = 0
        self.player_name = self.screen.CHARONE + self.screen.CHARTWO + self.screen.CHARTHREE
        GameEnvironment.PLAYER = MainCharacter(self.player_name)
        self.maze_environment.generate_maze_difficulty()
        # put player at maze start, calculate all coords
        # relative = absolute - maze
        start = MazeEnvironment.MAZE.start
        pos = get_player_pos(start[1], start[0])
        GameEnvironment.PLAYER.relative_x = pos[0]
        GameEnvironment.PLAYER.relative_y = pos[1]
        self.sw, self.sh = pygame.display.get_window_size()
        if start[0] == 0:
            MazeEnvironment.MAP_Y = 0
            MazeEnvironment.MAP_X = -1 * (MazeEnvironment.TILE_SIZE * start[1]) + ((pygame.display.get_window_size()[0] / 2) - (MazeEnvironment.TILE_SIZE / 2))
        elif start[1] == 0:
            MazeEnvironment.MAP_X = 0
            MazeEnvironment.MAP_Y = -1 * (MazeEnvironment.TILE_SIZE * start[0]) + ((pygame.display.get_window_size()[1] / 2) - (MazeEnvironment.TILE_SIZE / 2))
        elif start[0] == len(MazeEnvironment.MAZE.grid) - 1:
            MazeEnvironment.MAP_Y = -1 * (MazeEnvironment.PIXEL_HEIGHT - self.sh)
            MazeEnvironment.MAP_X = -1 * (MazeEnvironment.TILE_SIZE * start[1]) + ((pygame.display.get_window_size()[0] / 2) - (MazeEnvironment.TILE_SIZE / 2))
        else:
            MazeEnvironment.MAP_X = -1 * (MazeEnvironment.PIXEL_WIDTH - self.sw)
            MazeEnvironment.MAP_Y = -1 * (MazeEnvironment.TILE_SIZE * start[0]) + ((pygame.display.get_window_size()[1] / 2) - (MazeEnvironment.TILE_SIZE / 2))
        GameEnvironment.PLAYER.x = GameEnvironment.PLAYER.relative_x + MazeEnvironment.MAP_X
        GameEnvironment.PLAYER.y = GameEnvironment.PLAYER.relative_y + MazeEnvironment.MAP_Y
        Screen.SHOW_MAP = False

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

        # edge case for when in the start tile or end tile
        tp = p.tile_pos
        check = self.maze_environment.start_direction if MazeEnvironment.MAZE.grid[tp[0]][tp[1]] == MazeEnvironment.START \
                else (self.maze_environment.end_direction if MazeEnvironment.MAZE.grid[tp[0]][tp[1]] == MazeEnvironment.END else -1)
        if len(tp) > 0 and not check == -1:
            if check == 1:
                blocked_left = blocked_left or px - ps < self.maze_environment.start_end_walls[0].get_width()
            elif check == 2:
                blocked_up = blocked_up or py - ps < self.maze_environment.start_end_walls[1].get_height()
            elif check == 3:
                blocked_right = blocked_right or px + pw + ps > s[0] - self.maze_environment.start_end_walls[2].get_width()
            elif check == 4:
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
                    victory_sound = pygame.mixer.Sound(os.path.join('src', 'sounds', 'mixkit-medieval-show-fanfare-announcement-226.wav'))
                    pygame.mixer.Sound.play(victory_sound)
                    GameEnvironment.state = GameEnvironment.VICTORY_STATE

    def render(self, surface):
        background = pygame.Surface((surface.get_width(), surface.get_height()))
        background.convert()
        background.fill((0, 0, 0))
        surface.blit(background, (0, 0))
        # based on the game state, call a different method from the screen
        if GameEnvironment.state == GameEnvironment.START_STATE:
            self.screen.startView(surface)
        elif GameEnvironment.state == GameEnvironment.INGAME_STATE:
            self.score.start_time()
            self.screen.activeGameView()
        elif GameEnvironment.state == GameEnvironment.PAUSE_STATE:
            self.screen.pauseView(surface)
        elif GameEnvironment.state == GameEnvironment.VICTORY_STATE:
            self.score.end_time()
            self.screen.victory(surface)
        elif GameEnvironment.state == GameEnvironment.DEATH_STATE:
            self.score.end_time()
            self.screen.death(surface)
        elif GameEnvironment.state == GameEnvironment.MANUAL_STATE or GameEnvironment.state == GameEnvironment.PAUSE_MANUAL_STATE:
            self.screen.manual(surface)
        elif GameEnvironment.state == GameEnvironment.CONTRIBUTOR_STATE:
            self.screen.contributor_screen(surface)


    def switch_to_ingame(self):
        self.screen.start_music = False
        self.screen.music_count = 0
        GameEnvironment.state = GameEnvironment.INGAME_STATE
        self.start_ingame()

    def adjust_maze_to_window(self, nw, nh):
        # rel = abs - map
        # rel - abs = -map
        # -1 * (rel - abs) = map
        # x = abs + 2 - map - 2
        dw = self.sw - nw
        dh = self.sh - nh
        mc = 0
        if not dw == 0:
            oldr = GameEnvironment.PLAYER.relative_x
            GameEnvironment.PLAYER.x = (nw // 2) - (GameEnvironment.PLAYER.width // 2)
            o = -1 * (oldr - GameEnvironment.PLAYER.x)
            mc = MazeEnvironment.MAP_X - o
            MazeEnvironment.MAP_X = o
            for e in self.enemies:
                e[0].x -= mc
            for b in self.boosters:
                b[0].x -= mc
        if not dh == 0:
            oldr = GameEnvironment.PLAYER.relative_y
            GameEnvironment.PLAYER.y = (nh // 2) - (GameEnvironment.PLAYER.height // 2)
            o = -1 * (oldr - GameEnvironment.PLAYER.y)
            mc = MazeEnvironment.MAP_Y - o
            MazeEnvironment.MAP_Y = o
            for e in self.enemies:
                e[0].y -= mc
            for b in self.boosters:
                b[0].y -= mc
        self.sw = nw
        self.sh = nh

    def event_handler(self, event):
        s = pygame.display.get_surface()
        sw = s.get_width()
        sh = s.get_height()
        if event.type == pygame.VIDEORESIZE:
            w, h = event.size
            mw = 1000
            mh = 700
            if w < mw and h >= mh:
                pygame.display.set_mode((mw, sh), pygame.RESIZABLE)
            elif h < mh and w >= mw:
                pygame.display.set_mode((sw, mh), pygame.RESIZABLE)
            elif w < mw and h < mh:
                pygame.display.set_mode((mw, mh), pygame.RESIZABLE)
            self.screen.tick()
            self.adjust_maze_to_window(sw if sw > mw else mw, sh if sh > mh else mh)
            return
        # this handles all keyboard and mouse input, as well as timers
        if GameEnvironment.state == GameEnvironment.START_STATE:
            GameEnvironment.PLAYER.METH_COUNT = 0
            GameEnvironment.PLAYER.ATTACK_COUNT = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(self.click_sound)
                easy_button = pygame.Rect((sw // 2) - 400, (sh // 2) - 30, 200, 60)
                medium_button = pygame.Rect((sw // 2) - 100, (sh // 2) - 30, 200, 60)
                hard_button = pygame.Rect((sw // 2) + 200, (sh // 2) - 30, 200, 60)
                quit_button = pygame.Rect((sw // 2) - 100, (sh // 2) + 200, 200, 60)
                manual_button = pygame.Rect((sw // 2) + 200, (sh // 2) + 200, 200, 60)
                contributor_button = pygame.Rect((sw // 2) - 400, (sh // 2) + 200, 200, 60)
                
                char_one = pygame.Rect((sw // 2) - 110, 160, 60, 60)
                char_two = pygame.Rect((sw // 2) - 30, 160, 60, 60)
                char_three = pygame.Rect((sw // 2) + 50, 160, 60, 60)
                
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
                
                if easy_button.collidepoint(event.pos):
                    GameEnvironment.DIFFICULTY_TRACKER = GameEnvironment.DIFFICULTY_EASY
                    self.switch_to_ingame()
                elif medium_button.collidepoint(event.pos):
                    GameEnvironment.DIFFICULTY_TRACKER = GameEnvironment.DIFFICULTY_MEDIUM
                    self.switch_to_ingame()
                elif hard_button.collidepoint(event.pos):
                    GameEnvironment.DIFFICULTY_TRACKER = GameEnvironment.DIFFICULTY_HARD
                    self.switch_to_ingame()
                elif manual_button.collidepoint(event.pos):
                    GameEnvironment.state = GameEnvironment.MANUAL_STATE
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif contributor_button.collidepoint(event.pos):
                    GameEnvironment.state = GameEnvironment.CONTRIBUTOR_STATE
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
                    self.attack_sword_sound()
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
                pygame.mixer.Sound.play(self.click_sound)
                start_button = pygame.Rect((sw // 2) - 400, sh - 150, 200, 60)
                quit_button = pygame.Rect((sw // 2) + 200, sh - 150, 200, 60)
                manual_button = pygame.Rect((sw // 2) - 100, sh - 150, 200, 60)
                if start_button.collidepoint(event.pos):
                    GameEnvironment.state = GameEnvironment.INGAME_STATE
                elif manual_button.collidepoint(event.pos):
                    GameEnvironment.state = GameEnvironment.PAUSE_MANUAL_STATE
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        elif GameEnvironment.state == GameEnvironment.VICTORY_STATE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(self.click_sound)
                startButton = pygame.Rect((sw // 2) - 250, 600, 200, 60)
                quitButton = pygame.Rect((sw // 2) + 50, 600, 200, 60)
                if quitButton.collidepoint(event.pos): # check if button clicked quit
                    pygame.quit()
                    sys.exit()
                elif startButton.collidepoint(event.pos): # check if click was restart
                    GameEnvironment.PLAYER.METH_COUNT = 0
                    GameEnvironment.PLAYER.ATTACK_COUNT = 0
                    GameEnvironment.state = GameEnvironment.START_STATE
                    self.switch_to_ingame()
        elif  GameEnvironment.state == GameEnvironment.DEATH_STATE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(self.click_sound)
                startButton = pygame.Rect((sw // 2) - 250, 600, 200, 60)
                quitButton = pygame.Rect((sw // 2) + 50, 600, 200, 60)
                if quitButton.collidepoint(event.pos): # check if button clicked quit
                    pygame.quit()
                    sys.exit()
                elif startButton.collidepoint(event.pos): # check if click was restart
                    GameEnvironment.PLAYER.METH_COUNT = 0
                    GameEnvironment.PLAYER.ATTACK_COUNT = 0
                    GameEnvironment.state = GameEnvironment.START_STATE
        elif  GameEnvironment.state == GameEnvironment.MANUAL_STATE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(self.click_sound)
                back_button = pygame.Rect((sw // 2) - 300, (sh // 2) + 100, 200, 60)
                quit_button = pygame.Rect((sw // 2) + 100, (sh // 2) + 100, 200, 60)
                if back_button.collidepoint(event.pos):
                    GameEnvironment.state = GameEnvironment.START_STATE
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        elif  GameEnvironment.state == GameEnvironment.PAUSE_MANUAL_STATE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(self.click_sound)
                back_button = pygame.Rect((sw // 2) - 300, (sh // 2) + 100, 200, 60)
                quit_button = pygame.Rect((sw // 2) + 100, (sh // 2) + 100, 200, 60)
                if back_button.collidepoint(event.pos):
                    GameEnvironment.state = GameEnvironment.PAUSE_STATE
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        elif  GameEnvironment.state == GameEnvironment.CONTRIBUTOR_STATE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(self.click_sound)
                back_button = pygame.Rect((sw // 2) - 300, (sh // 2) + 100, 200, 60)
                quit_button = pygame.Rect((sw // 2) + 100, (sh // 2) + 100, 200, 60)
                if back_button.collidepoint(event.pos):
                    GameEnvironment.state = GameEnvironment.START_STATE
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    


