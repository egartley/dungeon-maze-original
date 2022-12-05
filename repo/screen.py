import pygame
import game
import os
from scores import Score
from maze import MazeEnvironment

frame_size_x = 1000
frame_size_y = 700



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

class Screen:
    TEXT_COLOR = (255, 255, 255)
    SHOW_MAP = False

    def __init__(self, maze_env, width, height):
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
        self.bg_img = pygame.transform.scale(self.bg_img, (frame_size_x, frame_size_y))
        self.cooldown_sprite = pygame.image.load('src/sprites/Weapons/Sword/sprite_swing_sword_right4.png')
        self.cooldown_sprite = pygame.transform.scale(self.cooldown_sprite, (90, 90))
        self.victory_bg_img = pygame.image.load('src/sprites/background/victorybg.jpg')
        self.victory_bg_img = pygame.transform.scale(self.victory_bg_img, (frame_size_x, frame_size_y))
        self.death_bg_img = pygame.image.load('src/sprites/background/tombstone.png')  # https://www.pinterest.com/pin/677651075162388819/
        self.death_bg_img = pygame.transform.scale(self.death_bg_img, (frame_size_x, frame_size_y))
        self.start_bg_img = pygame.image.load('src/sprites/background/start_screen.jpg')
        self.start_bg_img = pygame.transform.scale(self.start_bg_img, (frame_size_x, frame_size_y))
        self.manual_bg_img = pygame.image.load('src/sprites/background/nuke.jpg')
        self.manual_bg_img = pygame.transform.scale(self.manual_bg_img, (frame_size_x,frame_size_y))
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

        

    def pauseView(self):
        pygame.mixer.music.stop()
        self.start_music = False
        if self.victory_time_glitch == 0:
            self.score.end_time()
            self.victory_time_glitch = 0
            self.start_time_glitch = 0
        surface = pygame.display.get_surface()
        surface.blit(self.bg_img, (0,0))
        pygame.mouse.set_cursor(self.cursor)
        #start button
        surface = pygame.display.get_surface()
        startSurface = pygame.Surface((200, 60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface, (150, 550)) # hard coded button values if they get change , change in game.py event handler
        surface.blit(self.secondary_font.render("PLAY", True, black), (200, 550))
        #quit button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface, (700, 550))
        surface.blit(self.secondary_font.render("QUIT", True, black), (750, 550))
        #instructions button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(425,550))
        surface.blit(self.secondary_font.render("MANUAL",True, black), (450,550))
        


    def startView(self):
        pygame.mouse.set_cursor(self.cursor)
        #nick name button
        surface = pygame.display.get_surface()  ## since hard coded position values, if this change it changes in game.py event handler
        surface.blit(self.start_bg_img, (0,0))
        surface.blit(self.victory_font.render("Dungeon Maze", True, white), (270, 8))
        surface.blit(self.font.render("Enter a three letter nickname", True, white), (380.5, 130))
        startSurface = pygame.Surface((60, 60))
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface, (375, 160))
        surface.blit(self.secondary_font.render(self.CHARONE, True,black),(390.5,160))
        startSurface.fill(red)
        surface.blit(startSurface, (442, 160))
        surface.blit(self.secondary_font.render(self.CHARTWO, True,black),(457.5,160))
        startSurface.fill(red)
        surface.blit(startSurface, (510.5, 160))
        surface.blit(self.secondary_font.render(self.CHARTHREE, True,black),(525.5,160))
        #easy buttons
        startSurface = pygame.Surface((200, 60))
        startSurface.convert()  
        startSurface.fill(green)
        surface.blit(startSurface, (100, 350))
        surface.blit(self.secondary_font.render("EASY", True, black), (150, 350))
        #medium button
        startSurface.convert()
        startSurface.fill(orange)
        surface.blit(startSurface, (375, 350))  ## since hard coded if this change it changes in game.py event handler
        surface.blit(self.secondary_font.render("MEDIUM", True, black), (395, 350))
        #hard button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface, (675, 350))
        surface.blit(self.secondary_font.render("HARD", True, black), (720, 350))
        ## check if when mouse clicks on button it changes game state 
        startSurface.convert()
        startSurface.fill(orange)
        surface.blit(startSurface, (375, 550))
        surface.blit(self.secondary_font.render("QUIT", True, black), (430, 550))
        #instructions button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(675,550))
        surface.blit(self.secondary_font.render("MANUAL",True, black), (690,550))
        #instructions button
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface,(100,550))
        surface.blit(self.secondary_font.render("AUTHORS",True, black), (100,550))


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
            surface.blit(background, (pygame.display.get_surface().get_width() - 20 - len(grid[0]) * s, 12))

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
        surface.blit(self.font.render("Score: " + str(self.score.player_score), True, red), (5,20))
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

    def display_top_scores(self):
        x = 100
        for i in range(len(self.score.top_scores)):
            score = ''
            for k in range(len(self.score.top_scores[i])):
                    score += self.score.top_scores[i][k]
            score.replace('/n','')
            pygame.display.get_surface().blit(
                self.font.render(score, True, white), (frame_size_x/2-150, x ))
            x += 40
        
    def victory(self):
        if self.victory_time_glitch == 0:
            self.score.end_time()
            self.victory_time_glitch = 1
            self.start_time_glitch = 0
            pygame.mixer.music.stop()
            victory_sound = pygame.mixer.Sound(os.path.join('src', 'sounds', 'mixkit-video-game-win-2016.wav'))
            pygame.mixer.Sound.play(victory_sound)
        surface = pygame.display.get_surface()
        surface.blit(self.victory_bg_img, (0,0))
        surface.blit(self.victory_font.render("VICTORY CIRCLE", True, Screen.TEXT_COLOR), (270, 8))
        self.show_score(0, red, 'Times New Roman', 20)
        if self.display_score:
            self.display_score = False
            self.score.determine_writability()
            self.display_top_scores()
        pygame.mouse.set_cursor(self.cursor)
        s = pygame.Surface((630,440))  # the size of your rect
        s.set_alpha(150)
        s.fill(black)
        surface.blit(s, (200,90))
        #RESTART BUTTON
        startSurface = pygame.Surface((250,60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface,(200,600))
        surface.blit(self.secondary_font.render("RESTART", True, black), (230, 600))
        #QUIT button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(575,600))
        surface.blit(self.secondary_font.render("QUIT",True, black), (650,600))
        self.display_top_scores()
        
    def death(self):
        surface = pygame.display.get_surface()
        pygame.mixer.music.stop()
        if self.victory_time_glitch == 0:
            self.score.end_time()
            self.victory_time_glitch = 1
            self.start_time_glitch = 1
            failure_sound = pygame.mixer.Sound(os.path.join('src', 'sounds', 'videogame-death-sound-43894.mp3'))
            pygame.mixer.Sound.play(failure_sound)
        pygame.mouse.set_cursor(self.cursor)
        surface.blit(self.death_bg_img, (0,0))
        surface.blit(self.victory_font.render("DEATH", True, red), (400, 8))
        #RESTART BUTTON
        startSurface = pygame.Surface((200, 60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface,(200,550))
        surface.blit(self.secondary_font.render("RESTART", True, black), (210, 550))
        #QUIT BUTTON
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(605,550))
        surface.blit(self.secondary_font.render("QUIT",True, black), (655,550))
        self.show_score(0, white, "Times New Roman", 20)
         
        
    def show_score(self,choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        self.score.cal_score()
        score_surface = score_font.render("Score : " + str(self.score.player_score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (frame_size_x/10, 15)
        else:
            score_rect.midtop = ((frame_size_x/2)+10, frame_size_y/1.25)
        pygame.display.get_surface().blit(score_surface, score_rect)

    def quit(self):
        pass
    
    def manual(self):
        surface = pygame.display.get_surface() 
        surface.blit(self.manual_bg_img, (0,0))
        surface.blit(
            self.secondary_font.render("Instructions Manual", True, white), (300, 8))
        surface.blit(
            self.font.render("WASD keyboard keys for moving. The W key represents up. The A key represents left. The D key represents right. The S key represents down.", True, Screen.TEXT_COLOR), (30, 70))
        surface.blit(
            self.font.render("ESC key can be presssed for pause menu.", True, Screen.TEXT_COLOR), (350, 120))
        surface.blit(
            self.font.render("You can Left-Click to switch to the Sword. You can Right-Click to switch to the Bow.", True, Screen.TEXT_COLOR), (200, 96))
        #BACK BUTTON
        startSurface = pygame.Surface((200,60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface,(200,350))
        surface.blit(self.secondary_font.render("   BACK", True, black), (210, 350))
        #QUIT BUTTON
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(575,350))
        surface.blit(self.secondary_font.render("QUIT",True, black), (627,350))
        
    def pause_manual(self):
        surface = pygame.display.get_surface() 
        surface.blit(self.manual_bg_img, (0,0))
        surface.blit(
            self.secondary_font.render("Instructions Manual", True, white), (300, 8))
        surface.blit(
            self.font.render("WASD keyboard keys for moving. The W key represents up. The A key represents left. The D key represents right. The S key represents down.", True, Screen.TEXT_COLOR), (30, 70))
        surface.blit(
            self.font.render("ESC key can be presssed for pause menu.", True, Screen.TEXT_COLOR), (350, 120))
        surface.blit(
            self.font.render("You can Left-Click to switch to the Sword. You can Right-Click to switch to the Bow.", True, Screen.TEXT_COLOR), (200, 96))
        #BACK BUTTON
        startSurface = pygame.Surface((200,60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface,(200,350))
        surface.blit(self.secondary_font.render("BACK", True, black), (210, 350))
        #QUIT BUTTON
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(575,350))
        surface.blit(self.secondary_font.render("QUIT",True, black), (627,350))
        
    def contributor_screen(self):
        surface = pygame.display.get_surface() 
        surface.blit(
            self.secondary_font.render("Special Thanks", True, white), (350, 8))
        surface.blit(self.font.render("Team Leaders", True, Screen.TEXT_COLOR), (30, 70))
        surface.blit(self.font.render("Cam Gower", True, Screen.TEXT_COLOR), (50, 90))
        surface.blit(self.font.render("Brian Hinger", True, Screen.TEXT_COLOR), (50, 115))
        surface.blit(self.font.render("Team Members", True, Screen.TEXT_COLOR), (30, 150))
        surface.blit(self.font.render("Evan Gartley", True, Screen.TEXT_COLOR), (50, 170))
        surface.blit(self.font.render("Tan Tran", True, Screen.TEXT_COLOR), (50, 190))
        surface.blit(self.font.render("Zaineb Radi", True, Screen.TEXT_COLOR), (50, 210))
        surface.blit(self.secondary_font.render("Thank you team leaders for supporting each team!!", True, Screen.TEXT_COLOR),(50,250))
        #BACK BUTTON
        startSurface = pygame.Surface((200,60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface,(200,350))
        surface.blit(self.secondary_font.render("BACK", True, black), (240, 350))
        #QUIT BUTTON
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(575,350))
        surface.blit(self.secondary_font.render("QUIT",True, black), (627,350))

