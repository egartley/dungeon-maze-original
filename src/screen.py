import pygame
import game
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
        self.cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_NO)
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
        self.timeGlitch = 0
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
        
    def pauseView(self):
        if self.timeGlitch == 0:
            self.score.end_time()
            self.timeGlitch +=1
        surface = pygame.display.get_surface()
        surface.blit(self.bg_img, (0,0))
        pygame.mouse.set_cursor(self.cursor)
        #start button
        surface = pygame.display.get_surface()
        startSurface = pygame.Surface((200, 60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface, (250, 550)) # hard coded button values if they get change , change in game.py event handler
        surface.blit(self.secondary_font.render("PLAY", True, black), (300, 550))
        #quit button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface, (600, 550))
        surface.blit(self.secondary_font.render("QUIT", True, black), (650, 550))

    def startView(self):
        pygame.mouse.set_cursor(self.cursor)
        #nick name button
        surface = pygame.display.get_surface()  ## since hard coded position values, if this change it changes in game.py event handler
        surface.blit(self.victory_font.render("Dungeon Maze", True, white), (270, 8))
        surface.blit(self.font.render("Enter a three letter nickname", True, white), (367.5, 130))
        startSurface = pygame.Surface((60, 60))
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface, (355, 160))
        surface.blit(self.secondary_font.render(self.CHARONE, True,black),(370.5,160))
        startSurface.fill(green)
        surface.blit(startSurface, (435, 160))
        surface.blit(self.secondary_font.render(self.CHARTWO, True,black),(450.5,160))
        startSurface.fill(blue)
        surface.blit(startSurface, (510.5, 160))
        surface.blit(self.secondary_font.render(self.CHARTHREE, True,black),(525.5,160))
        #easy buttons
        startSurface = pygame.Surface((200, 60))
        startSurface.convert()  # 100, 350, 200, 60
        startSurface.fill(green)
        surface.blit(startSurface, (100, 350))
        surface.blit(self.secondary_font.render("EASY", True, black), (150, 350))
        #medium button
        startSurface.convert()
        startSurface.fill(yellow)
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

    def activeGameView(self):
        self.timeGlitch = 0
        self.score.start_time()
        surface = pygame.display.get_surface() 
        self.maze_environment.render(surface)
        game.GameEnvironment.PLAYER.render(surface)
        self.draw_minimap(surface)
        surface.blit(self.font.render("Move with WASD", True, Screen.TEXT_COLOR), (12, 8))
        # back fill of health bar plus health bar
        back_fill = pygame.Surface((90, 10))
        back_fill.convert()
        back_fill.fill(health_grey)
        surface.blit(back_fill, (12, 74))
        health_bar_width = (game.GameEnvironment.PLAYER.health / 100) * 90
        if health_bar_width < 0:
            health_bar_width = 0
        sprite = pygame.Surface((health_bar_width, 10))
        sprite.convert()
        sprite.fill(health_red)
        surface.blit(sprite, (12, 74))
        #Shield and Shield Backfill
        shield_bar_fill = (100 / 100) * 10
        shield_fill = pygame.Surface((90, shield_bar_fill))
        shield_fill.convert()
        shield_fill.fill(orange)
        surface.blit(shield_fill, (12, 52))
        shield_bar_width = (game.GameEnvironment.PLAYER.shield / 100) * 90
        if shield_bar_width < 0:
            shield_bar_width = 0
        shield_sprite = pygame.Surface((shield_bar_width, 10))
        shield_sprite.convert()
        shield_sprite.fill(shield_blue)
        surface.blit(shield_sprite, (12, 52))
        #Meth Backfill
        meth_back_fill = (100 / 100) * 10
        meth_fill = pygame.Surface((90, meth_back_fill))
        meth_fill.convert()
        meth_fill.fill(white)
        surface.blit(meth_fill, (12, 94))
        meth_bar_width = (game.GameEnvironment.PLAYER.METH_COUNT / 3) * 90
        if meth_bar_width < 0:
            meth_bar_width = 0
        meth_sprite = pygame.Surface((meth_bar_width, 10))
        meth_sprite.convert()
        meth_sprite.fill(purple_meth)
        surface.blit(meth_sprite, (12, 94))
        #attack backfill
        attack_fill = 1 * 10
        attack_back_fill = pygame.Surface((90, attack_fill))
        attack_back_fill.convert()
        attack_back_fill.fill(white)
        surface.blit(attack_back_fill,(12,116))
        attack_width = (game.GameEnvironment.PLAYER.ATTACK_COUNT / 3) * 90
        if attack_width < 0:
            attack_width = 0
        attack_sprite = pygame.Surface((attack_width,10))
        attack_sprite.convert()
        attack_sprite.fill(green)
        surface.blit(attack_sprite,(12,116))
        #arrow
        surface.blit(self.arrow_sprite, (12, surface.get_height() - 50))
        surface.blit(self.font.render(str(game.GameEnvironment.PLAYER.arrow_count) + 'X', True, Screen.TEXT_COLOR), (75, surface.get_height() - 45))
        if game.GameEnvironment.PLAYER.weapon.in_cooldown:
            surface.blit(self.cooldown_sprite,(game.GameEnvironment.PLAYER.x - 40, game.GameEnvironment.PLAYER.y - 70))
        pygame.draw.rect(surface, (0, 0, 255), game.GameEnvironment.PLAYER.rect, 1)

    def display_top_scores(self):
        x = 100
        for i in range(len(self.score.top_scores)):
            score = ''
            for k in range(len(self.score.top_scores[i])):
                    score += self.score.top_scores[i][k]
            score.replace('/m','')
            pygame.display.get_surface().blit(
                self.font.render(score, True, white), (frame_size_x/2-150, x ))
            x += 40
        
    def victory(self):
        if self.timeGlitch == 0:
            self.score.end_time()
            self.timeGlitch +=1
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
        if self.timeGlitch == 0:
            self.score.end_time()
            self.timeGlitch +=1
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
        self.show_score(0, white, 'Times New Roman', 20)
        #check for position 
        
    def show_score(self,choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        self.score.cal_score()
        score_surface = score_font.render('Score : ' + str(self.score.player_score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (frame_size_x/10, 15)
        else:
            score_rect.midtop = ((frame_size_x/2)+10, frame_size_y/1.25)
        pygame.display.get_surface().blit(score_surface, score_rect)

    def quit(self):
        pass
