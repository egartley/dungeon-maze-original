from numpy import char
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
orange = pygame.Color(255,127,0)


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
        self.score = Score(self.name)
        self.timeGlitch = 0
        
    def pauseView(self):
        if self.timeGlitch == 0:
            self.score.end_time()
            self.timeGlitch +=1
        surface = pygame.display.get_surface() 
        surface.blit(self.secondary_font.render("Pause screen", True, Screen.TEXT_COLOR), (400, 8))
        pygame.mouse.set_cursor(self.cursor)
        #start button
        surface = pygame.display.get_surface() 
        startSurface = pygame.Surface((200,60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface,(250,350)) # hard coded button values if they get change , change in game.py event handler
        surface.blit(self.secondary_font.render("PLAY",True, black), (300,350))
        #quit button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(600,350))
        surface.blit(self.secondary_font.render("QUIT",True, black), (650,350))
        
    def startView(self):
        pygame.mouse.set_cursor(self.cursor)
        #nick name button
        surface = pygame.display.get_surface()  ## since hard coded position values, if this change it changes in game.py event handler
        surface.blit(self.font.render("Enter a three letter nickname", True,white),(362.5,130))
        startSurface = pygame.Surface((60,60))
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
        startSurface = pygame.Surface((200,60))
        startSurface.convert()  # 100, 350, 200, 60
        startSurface.fill(green)
        surface.blit(startSurface,(100,350))
        surface.blit(self.secondary_font.render("EASY", True, black), (150, 350))
        #medium button
        startSurface.convert()
        startSurface.fill(yellow)
        surface.blit(startSurface,(375,350))  ## since hard coded if this change it changes in game.py event handler
        surface.blit(self.secondary_font.render("MEDIUM",True, black), (395,350))
        #hard button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(675,350))
        surface.blit(self.secondary_font.render("HARD",True, black), (720,350))
        ## check if when mouse clicks on button it changes game state 
        startSurface.convert()
        startSurface.fill(orange)
        surface.blit(startSurface,(375,550)) 
        surface.blit(self.secondary_font.render("QUIT",True, black), (430,550))
        
        
    def draw_minimap(self, surface):
        s = 4
        wall = pygame.Surface((s, s))
        wall.convert()
        #wall.fill((160, 160, 160)) 
        wall.fill((255, 255, 255))
        start = pygame.Surface((s, s))
        start.convert()
        start.fill((0, 255, 0)) # green
        end = pygame.Surface((s, s))
        end.convert()
        end.fill((160, 160, 160))
        player = pygame.Surface((s, s))
        player.convert()
        player.fill((138, 43, 226)) #purple

        grid = MazeEnvironment.MAZE.grid

        background = pygame.Surface((len(grid[0]) * s + 8, len(grid) * s + 8))
        background.convert()
        background.fill((210, 186, 147))

        for chunk in MazeEnvironment.CHUNKS:
            if chunk not in MazeEnvironment.TRACKED_CHUNKS:
                MazeEnvironment.TRACKED_CHUNKS.append(chunk)

        # the "base" x/y the use for calculating the indiviudal x/y of each tile
        for chunk in MazeEnvironment.TRACKED_CHUNKS:
            i = chunk.r
            j = chunk.c
            position = (4 + (j * s), 4 + (i * s))
            if game.GameEnvironment.PLAYER.tile_pos == (i, j):
                background.blit(player, position)
            elif MazeEnvironment.MAZE.start == (i, j):
                background.blit(start, position)
            elif MazeEnvironment.MAZE.end == (i, j):
                background.blit(end, position)
            elif len(grid) > 0 and i < len(grid) and j < len(grid[0]) and grid[i][j] == 1:
                background.blit(wall, position)
        if self.SHOW_MAP == True:
            surface.blit(background, (pygame.display.get_surface().get_width() - 20 - len(grid[0]) * s, 12))
        

    def activeGameView(self):
        self.timeGlitch = 0
        self.score.start_time()
        surface = pygame.display.get_surface() 
        self.maze_environment.render(surface)
        game.GameEnvironment.PLAYER.render(surface)
        
        self.draw_minimap(surface)
    
        surface.blit(self.font.render("In-game view", True, Screen.TEXT_COLOR), (12, 8))
        surface.blit(self.font.render("Move with WASD", True, Screen.TEXT_COLOR), (12, 30))
        
        # back fill of health bar plus health bar
        backFillSprite = pygame.Surface((90,10))
        backFillSprite.convert()
        backFillSprite.fill(white)
        surface.blit(backFillSprite,(12,74))
        healthBarWidth = (game.GameEnvironment.PLAYER.health / 100)  * 90
        if healthBarWidth < 0:
            healthBarWidth = 0
        sprite = pygame.Surface((healthBarWidth,10))
        sprite.convert()
        sprite.fill(red)
        surface.blit(sprite, (12,74))
        
        
        #Shield and Shield Backfill 
        shieldBarBackFill = (100 / 100) * 10
        shieldFill = pygame.Surface((90, shieldBarBackFill))
        shieldFill.convert()
        shieldFill.fill(white)
        surface.blit(shieldFill, (12,52))
        shieldBarWidth = (game.GameEnvironment.PLAYER.shield / 100 ) * 90
        if shieldBarWidth < 0:
            shieldBarWidth = 0
        shieldSprite = pygame.Surface((shieldBarWidth,10))
        shieldSprite.convert()
        shieldSprite.fill(blue)
        surface.blit(shieldSprite, (12,52))
        
        arrow_sprite = pygame.image.load('src/sprites/Boosters/arrow.png')
        arrow_sprite = pygame.transform.scale(arrow_sprite, (50,30))
        surface.blit(arrow_sprite,(12,surface.get_height() - 50))
        surface.blit(self.font.render(str(game.GameEnvironment.PLAYER.arrow_count) + 'X', True, Screen.TEXT_COLOR), (75,surface.get_height() -45))
        
        if game.GameEnvironment.PLAYER.weapon.in_cooldown:
            sprite = pygame.image.load('src/sprites/Weapons/Sword/sprite_swing_sword_right4.png')
            sprite =  pygame.transform.scale(sprite, (90,90))
            surface.blit(sprite,(game.GameEnvironment.PLAYER.x - 40, game.GameEnvironment.PLAYER.y - 70))
        
        
        
    def top_scores(self):
        x = 100
        
        list_scores = self.score.read_score()
        for i in range(len(list_scores)):
            score = ' '.join(map(str, list_scores[i]))
            pygame.display.get_surface().blit(
                self.font.render(score, True, Screen.TEXT_COLOR), (frame_size_x/2-200, x))
            x += 40

    def victory(self):
        if self.timeGlitch == 0:
            self.score.end_time()
            self.timeGlitch +=1
        surface = pygame.display.get_surface() 
        bg_img = pygame.image.load('src\\sprites\\background\\victorybg.jpg')
        bg_img = pygame.transform.scale(bg_img,(frame_size_x, frame_size_y))
        surface.blit(bg_img, (0,0))
        surface.blit(self.victory_font.render("VICTORY CIRCLE", True, Screen.TEXT_COLOR), (250, 8))
        self.show_score(0, red, 'Times New Roman', 20)
        pygame.mouse.set_cursor(self.cursor)
        #pygame.draw.rect(surface, black, pygame.Rect(frame_size_x/2-150, 100, 300, 400))
        #pygame.gfxdraw.box(surface, pygame.Rect(frame_size_x/2-150, 100, 300, 400), black)
        s = pygame.Surface((480,440))  # the size of your rect
        s.set_alpha(150)
        s.fill(black)
        surface.blit(s, (200,90))
        self.top_scores()
        
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
        surface.blit(self.secondary_font.render("QUIT",True, black), (630,600))

    def death(self):
        if self.timeGlitch == 0:
            self.score.end_time()
            self.timeGlitch +=1
        pygame.mouse.set_cursor(self.cursor)
        my_font = pygame.font.SysFont('Times New Roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
        pygame.display.get_surface().blit(game_over_surface, game_over_rect)
        #RESTART BUTTON
        surface = pygame.display.get_surface() 
        startSurface = pygame.Surface((200,60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface,(200,350))
        surface.blit(self.secondary_font.render("RESTART", True, black), (210, 550))
        #QUIT BUTTON
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(575,350))
        surface.blit(self.secondary_font.render("QUIT",True, black), (627,650))
        self.show_score(0, red, 'Times New Roman', 20)
        #check for position 
        
    def show_score(self,choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        self.score.cal_score()
        score_surface = score_font.render('Score : ' + str(self.score.player_score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (frame_size_x/10, 15)
        else:
            score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
        pygame.display.get_surface().blit(score_surface, score_rect)

    def quit(self):
        pass
