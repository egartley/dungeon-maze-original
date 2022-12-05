import pygame
import game
import os
from scores import Score
from maze import MazeEnvironment


# Initialise colors for resuse
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255,255,0)
orange = pygame.Color(255,127,39)
purple_meth = pygame.Color(163,73,164)
shield_blue = pygame.Color(0,162,232)
health_grey = pygame.Color(195,195,195)
health_red = pygame.Color(237,28,36)

frame_size_x = 0
frame_size_y = 0

class Screen:
    TEXT_COLOR = (255, 255, 255)
    SHOW_MAP = False

    def __init__(self, maze_env, width, height):
        self.prev_window_width = width
        self.prev_window_height = height
        self.cursor = pygame.cursors.Cursor(pygame.cursors.arrow)
        self.maze_environment = maze_env
        self.title = "Dungeon Maze"
        pygame.display.set_caption(self.title)
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 18)
        self.secondary_font = pygame.font.SysFont("Arial", 50)
        self.third_font = pygame.font.SysFont("calibri.ttf", 30)
        self.victory_font = pygame.font.SysFont("calibri.ttf", 80)
        self.CHARONE = chr(ord('A'))
        self.CHARTWO = chr(ord('A'))
        self.CHARTHREE = chr(ord('A'))
        self.name = self.CHARONE + self.CHARTWO + self.CHARTHREE
        self.score = Score(self.name,game.GameEnvironment.DIFFICULTY_TRACKER)
        self.victory_time_glitch = 0
        self.start_time_glitch = 0
        self.display_score = True
        self.arrow_sprite = pygame.image.load('src/sprites/Boosters/arrow.png')
        self.arrow_sprite = pygame.transform.scale(self.arrow_sprite, (50, 30))
        self.bg_img = pygame.image.load('src/sprites/background/pause.png') #https://www.shutterstock.com/video/clip-1008683782-retro-videogame-pause-text-computer-old-tv
        self.cooldown_sprite = pygame.image.load('src/sprites/Weapons/Sword/sprite_swing_sword_right4.png')
        self.cooldown_sprite = pygame.transform.scale(self.cooldown_sprite, (90, 90))
        self.victory_bg_img = pygame.image.load('src/sprites/background/victorybg.jpg')
        self.death_bg_img = pygame.image.load('src/sprites/background/tombstone.png')  # https://www.pinterest.com/pin/677651075162388819/
        self.music_count = 0.0
        self.start_music = False
        self.shield =  pygame.image.load('src/sprites/Boosters/Shields.png')
        self.shield = pygame.transform.scale(self.shield, (20,20))
        self.health =  pygame.image.load("src/sprites/Boosters/health-booster.png")
        self.health = pygame.transform.scale(self.health, (20,20))
        self.speed = pygame.image.load('src/sprites/Boosters/speed.png')
        self.speed = pygame.transform.scale(self.speed, (20,20))
        self.attack = pygame.image.load('src/sprites/Boosters/attack.png')
        self.attack =  pygame.transform.scale(self.attack, (20,20))
        frame_size_x = width
        frame_size_y = height
        self.bg_img = pygame.transform.scale(self.bg_img, (width, height))
        self.victory_bg_img = pygame.transform.scale(self.victory_bg_img, (width, height))
        self.death_bg_img = pygame.transform.scale(self.death_bg_img, (width, height))

    def tick(self):
        s = pygame.display.get_surface()
        frame_size_x = s.get_width()
        frame_size_y = s.get_height()
        if not frame_size_x == self.prev_window_width or not self.prev_window_height == frame_size_y:
            self.bg_img = pygame.transform.scale(self.bg_img, (frame_size_x, frame_size_y))
            self.victory_bg_img = pygame.transform.scale(self.victory_bg_img, (frame_size_x, frame_size_y))
            self.death_bg_img = pygame.transform.scale(self.death_bg_img, (frame_size_x, frame_size_y))
            self.prev_window_width = frame_size_x
            self.prev_window_height = frame_size_y

    def pauseView(self, surface):
        sw = surface.get_width()
        sh = surface.get_height()
        pygame.mixer.music.stop()
        self.start_music = False
        if self.victory_time_glitch == 0:
            self.score.end_time()
            self.victory_time_glitch = 0
            self.start_time_glitch = 0
        surface.blit(self.bg_img, (0, 0))
        pygame.mouse.set_cursor(self.cursor)
        #start button
        startSurface = pygame.Surface((200, 60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface, ((sw // 2) - 400, sh - 150)) # hard coded button values if they get change , change in game.py event handler
        surface.blit(self.secondary_font.render("PLAY", True, black), ((sw // 2) - 350, sh - 150))
        #quit button
        startSurface = pygame.Surface((200, 60))
        startSurface.fill(red)
        surface.blit(startSurface, ((sw // 2) + 200, sh - 150))
        surface.blit(self.secondary_font.render("QUIT", True, black), ((sw // 2) + 250, sh - 150))
        #instructions button
        startSurface = pygame.Surface((200, 60))
        startSurface.fill(red)
        surface.blit(startSurface, ((sw // 2) - 100, sh - 150))
        surface.blit(self.secondary_font.render("MANUAL",True, black), ((sw // 2) - 80, sh - 150))

    def startView(self, surface):
        sw = surface.get_width()
        sh = surface.get_height()
        pygame.mouse.set_cursor(self.cursor)
        #nick name button
        surface = pygame.display.get_surface()  ## since hard coded position values, if this change it changes in game.py event handler
        surface.blit(self.victory_font.render("Dungeon Maze", True, white), ((sw // 2) - 206, 16))
        s = self.font.render("Enter a three letter nickname", True, white)
        surface.blit(s, ((sw // 2) - (s.get_width() // 2), 130))
        startSurface = pygame.Surface((60, 60))
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface, ((sw // 2) - 110, 160))
        surface.blit(self.secondary_font.render(self.CHARONE, True,black), ((sw // 2) - 95, 160))
        startSurface.fill(green)
        surface.blit(startSurface, ((sw // 2) - 30, 160))
        surface.blit(self.secondary_font.render(self.CHARTWO, True,black), ((sw // 2) - 15, 160))
        startSurface.fill(blue)
        surface.blit(startSurface, ((sw // 2) + 50, 160))
        surface.blit(self.secondary_font.render(self.CHARTHREE, True,black), ((sw // 2) + 65, 160))
        #easy buttons
        startSurface = pygame.Surface((200, 60))
        startSurface.convert()  
        startSurface.fill(green)
        surface.blit(startSurface, ((sw // 2) - 400, (sh // 2) - 30))
        surface.blit(self.secondary_font.render("EASY", True, black), ((sw // 2) - 355, (sh // 2) - 30))
        # medium button
        startSurface = pygame.Surface((200, 60))
        startSurface.fill(yellow)
        surface.blit(startSurface, ((sw // 2) - 100, (sh // 2) - 30))  ## since hard coded if this change it changes in game.py event handler
        surface.blit(self.secondary_font.render("MEDIUM", True, black), ((sw // 2) - 80, (sh // 2) - 30))
        # hard button
        startSurface = pygame.Surface((200, 60))
        startSurface.fill(red)
        surface.blit(startSurface, ((sw // 2) + 200, (sh // 2) - 30))
        surface.blit(self.secondary_font.render("HARD", True, black), ((sw // 2) + 245, (sh // 2) - 30))
        # quit button
        startSurface = pygame.Surface((200, 60))
        startSurface.fill(orange)
        surface.blit(startSurface, ((sw // 2) - 100, (sh // 2) + 200))
        surface.blit(self.secondary_font.render("QUIT", True, black), ((sw // 2) - 50, (sh // 2) + 200))
        #instructions button
        startSurface = pygame.Surface((200, 60))
        startSurface.fill(red)
        surface.blit(startSurface, ((sw // 2) + 200, (sh // 2) + 200))
        surface.blit(self.secondary_font.render("MANUAL", True, black), ((sw // 2) + 215, (sh // 2) + 200))

    def draw_minimap(self, surface):
        s = 4
        wall = pygame.Surface((s, s))
        wall.convert()
        wall.fill((255, 255, 255))
        start = pygame.Surface((s, s))
        start.convert()
        start.fill((0, 255, 0)) # green
        end = pygame.Surface((s, s))
        end.convert()
        end.fill((255, 0, 0)) # red
        player = pygame.Surface((s, s))
        player.convert()
        player.fill((138, 43, 226)) #purple

        grid = MazeEnvironment.MAZE.grid

        background = pygame.Surface((len(grid[0]) * s + 8, len(grid) * s + 8))
        background.convert()
        background.fill((210, 186, 147))

        for chunk in MazeEnvironment.CHUNKS:
            rc = (chunk.r, chunk.c)
            if rc not in MazeEnvironment.TRACKED_CHUNKS:
                MazeEnvironment.TRACKED_CHUNKS.append(rc)

        # the "base" x/y the use for calculating the individual x/y of each tile
        for chunk in MazeEnvironment.TRACKED_CHUNKS:
            i = chunk[0]
            j = chunk[1]
            position = (4 + (j * s), 4 + (i * s))
            if game.GameEnvironment.PLAYER.tile_pos == (i, j):
                background.blit(player, position)
            elif MazeEnvironment.MAZE.start == (i, j):
                background.blit(start, position)
            elif MazeEnvironment.MAZE.end == (i, j):
                background.blit(end, position)
            elif len(grid) > 0 and i < len(grid) and j < len(grid[0]) and grid[i][j] == 1:
                background.blit(wall, position)
        if self.SHOW_MAP:
            surface.blit(background, (surface.get_width() - 20 - len(grid[0]) * s, 12))

    def reset_background_music(self):
        if self.music_count > 277.00:
            self.music_count = 0

    def activeGameView(self):
        if not self.start_music:
            self.start_music = True
            pygame.mixer.music.load(os.path.join('src', 'sounds', 'Adventure-320bit.mp3'))
            pygame.mixer.music.play(-1, self.music_count)
        self.music_count += 0.016
        self.reset_background_music()
        if self.start_time_glitch == 0:
            self.victory_time_glitch = 0
            self.start_time_glitch = 1
            self.score.start_time()
        surface = pygame.display.get_surface() 
        self.maze_environment.render(surface)
        self.draw_minimap(surface)

        surface.blit(self.shield,(5,50))
        surface.blit(self.health,(5,70))
        surface.blit(self.speed, (5, 95))
        surface.blit(self.attack, (5, 115))
        # back fill of health bar plus health bar
        back_fill = pygame.Surface((90, 10))
        back_fill.convert()
        back_fill.fill(health_grey)
        surface.blit(back_fill, (30, 74))
        health_bar_width = (game.GameEnvironment.PLAYER.health / 100) * 90
        if health_bar_width < 0:
            health_bar_width = 0
        sprite = pygame.Surface((health_bar_width, 10))
        sprite.convert()
        sprite.fill(health_red)
        surface.blit(sprite, (30, 74))
        #Shield and Shield Backfill
        shield_fill = pygame.Surface((90, 10))
        shield_fill.convert()
        shield_fill.fill(orange)
        surface.blit(shield_fill, (30, 52))
        shield_bar_width = (game.GameEnvironment.PLAYER.shield / 100) * 90
        if shield_bar_width < 0:
            shield_bar_width = 0
        shield_sprite = pygame.Surface((shield_bar_width, 10))
        shield_sprite.convert()
        shield_sprite.fill(shield_blue)
        surface.blit(shield_sprite, (30, 52))
        #Meth Backfill
        meth_fill = pygame.Surface((90, 10))
        meth_fill.convert()
        meth_fill.fill(white)
        surface.blit(meth_fill, (30, 100))
        meth_bar_width = (game.GameEnvironment.PLAYER.METH_COUNT / 3) * 90
        if meth_bar_width < 0:
            meth_bar_width = 0
        meth_sprite = pygame.Surface((meth_bar_width, 10))
        meth_sprite.convert()
        meth_sprite.fill(purple_meth)
        surface.blit(meth_sprite, (30, 100))
        #attack backfill
        attack_back_fill = pygame.Surface((90, 10))
        attack_back_fill.convert()
        attack_back_fill.fill(white)
        surface.blit(attack_back_fill,(30,122))
        attack_width = (game.GameEnvironment.PLAYER.ATTACK_COUNT / 3) * 90
        if attack_width < 0:
            attack_width = 0
        attack_sprite = pygame.Surface((attack_width,10))
        attack_sprite.convert()
        attack_sprite.fill(green)
        surface.blit(attack_sprite,(30,122))
        #arrow
        surface.blit(self.arrow_sprite, (30, surface.get_height() - 50))
        surface.blit(self.font.render(str(game.GameEnvironment.PLAYER.arrow_count) + 'X', True, Screen.TEXT_COLOR), (75, surface.get_height() - 45))
        if game.GameEnvironment.PLAYER.weapon.in_cooldown:
            surface.blit(self.cooldown_sprite,(game.GameEnvironment.PLAYER.x - 40, game.GameEnvironment.PLAYER.y - 70))

    def display_top_scores(self, surface):
        x = 100
        for i in range(len(self.score.top_scores)):
            score = ''
            for k in range(len(self.score.top_scores[i])):
                    score += self.score.top_scores[i][k]
            score.replace('/n','')
            surface.blit(self.font.render(score, True, white), (surface.get_width() // 2 - 165, x))
            x += 40
        
    def victory(self, surface):
        if self.victory_time_glitch == 0:
            self.score.end_time()
            self.victory_time_glitch = 1
            self.start_time_glitch = 0
            pygame.mixer.music.stop()
            victory_sound = pygame.mixer.Sound(os.path.join('src', 'sounds', 'mixkit-video-game-win-2016.wav'))
            pygame.mixer.Sound.play(victory_sound)
        sw = surface.get_width()
        surface.blit(self.victory_bg_img, (0, 0))
        surface.blit(self.victory_font.render("VICTORY CIRCLE", True, Screen.TEXT_COLOR), ((sw // 2) - 234, 16))
        self.show_score(white, 'Times New Roman', 20, surface)
        if self.display_score:
            self.display_score = False
            self.score.determine_writability()
        pygame.mouse.set_cursor(self.cursor)
        s = pygame.Surface((630, 440))
        s.set_alpha(150)
        s.fill(black)
        surface.blit(s, ((sw // 2) - 315, 90))
        #RESTART BUTTON
        startSurface = pygame.Surface((200, 60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface, ((sw // 2) - 250, 600))
        surface.blit(self.secondary_font.render("RESTART", True, black), ((sw // 2) - 243, 600))
        #QUIT button
        startSurface = pygame.Surface((200, 60))
        startSurface.fill(red)
        surface.blit(startSurface, ((sw // 2) + 50, 600))
        surface.blit(self.secondary_font.render("QUIT",True, black), ((sw // 2) + 103, 600))
        self.display_top_scores(surface)
        
    def death(self, surface):
        sw = surface.get_width()
        pygame.mixer.music.stop()
        if self.victory_time_glitch == 0:
            self.score.end_time()
            self.victory_time_glitch = 1
            self.start_time_glitch = 1
            failure_sound = pygame.mixer.Sound(os.path.join('src', 'sounds', 'videogame-death-sound-43894.mp3'))
            pygame.mixer.Sound.play(failure_sound)
        surface.blit(self.death_bg_img, (0, 0))
        st = self.victory_font.render("DEATH", True, red)
        surface.blit(st, ((sw // 2) - (st.get_width() // 2), 16))
        # RESTART BUTTON
        startSurface = pygame.Surface((200, 60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface, ((sw // 2) - 250, 600))
        surface.blit(self.secondary_font.render("RESTART", True, black), ((sw // 2) - 243, 600))
        # QUIT BUTTON
        startSurface = pygame.Surface((200, 60))
        startSurface.fill(red)
        surface.blit(startSurface, ((sw // 2) + 50, 600))
        surface.blit(self.secondary_font.render("QUIT",True, black), ((sw // 2) + 103, 600))
        self.show_score(white, "Times New Roman", 20, surface)
        
    def show_score(self, color, font, size, surface):
        score_font = pygame.font.SysFont(font, size)
        self.score.cal_score()
        score_surface = score_font.render("Score: " + str(self.score.player_score), True, color)
        s = pygame.Surface((score_surface.get_width() + 16, score_surface.get_height() + 16))
        s.set_alpha(150)
        s.fill(black)
        surface.blit(s, ((surface.get_width() // 2) - (score_surface.get_width() // 2) - 8, 550 - 8))
        surface.blit(score_surface, ((surface.get_width() // 2) - (score_surface.get_width() // 2), 550))
    
    def manual(self, surface):
        sw = surface.get_width()
        sh = surface.get_height()
        s = self.secondary_font.render("Instruction Manual", True, white)
        surface.blit(s, ((sw // 2) - (s.get_width() // 2), (sh // 2) - 310))
        s = self.font.render("Move with the WASD keys. The W key represents up, A is left, S is down, and D is right.", True, Screen.TEXT_COLOR)
        surface.blit(s, ((sw // 2) - (s.get_width() // 2), (sh // 2) - 230))
        s = self.font.render("Left-click to swing the sword, and right-click to use the bow.", True, Screen.TEXT_COLOR)
        surface.blit(s, ((sw // 2) - (s.get_width() // 2), (sh // 2) - 200))
        s = self.font.render("Press M to toggle the minimap.", True, Screen.TEXT_COLOR)
        surface.blit(s, ((sw // 2) - (s.get_width() // 2), (sh // 2) - 170))
        s = self.font.render("Press the ESC key to pause the game.", True, Screen.TEXT_COLOR)
        surface.blit(s, ((sw // 2) - (s.get_width() // 2), (sh // 2) - 140))
        #BACK BUTTON
        startSurface = pygame.Surface((200, 60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface, ((sw // 2) - 300, (sh // 2) + 100))
        surface.blit(self.secondary_font.render("BACK", True, black), ((sw // 2) - 257, (sh // 2) + 100))
        #QUIT BUTTON
        startSurface = pygame.Surface((200, 60))
        startSurface.fill(red)
        surface.blit(startSurface, ((sw // 2) + 100, (sh // 2) + 100))
        surface.blit(self.secondary_font.render("QUIT", True, black), ((sw // 2) + 150, (sh // 2) + 100))
