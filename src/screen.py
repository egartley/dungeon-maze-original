import pygame
import game
from maze import MazeEnvironment

frame_size_x = 1000
frame_size_y = 700

score = 0

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

    def __init__(self, maze_env, width, height):
        self.cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_NO)
        self.maze_environment = maze_env
        self.title = "Dungeon Maze"
        pygame.display.set_caption(self.title)
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 18)

    def pauseView(self):
        surface = pygame.display.get_surface() 
        surface.blit(self.font.render("Pause screen", True, Screen.TEXT_COLOR), (12, 8))
        surface.blit(
            self.font.render("Press ESC again to resume playing", True, Screen.TEXT_COLOR), (12, 30))
        pygame.mouse.set_cursor(self.cursor)
        #start button
        surface = pygame.display.get_surface() 
        startSurface = pygame.Surface((200,60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface,(250,350)) # hard coded button values if they get change , change in game.py event handler
        surface.blit(self.font.render("CONTINUE",True, black), (315,370))
        #quit button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(600,350))
        surface.blit(self.font.render("QUIT",True, black), (680,370))
        
    def startView(self):
        pygame.display.get_surface().blit(self.font.render("Start screen", True, Screen.TEXT_COLOR), (12, 8))
        pygame.display.get_surface().blit(self.font.render("Press ENTER to begin playing", True, Screen.TEXT_COLOR),
                                          (12, 30))
        pygame.mouse.set_cursor(self.cursor)
        #easy button
        surface = pygame.display.get_surface()  ## since hard coded position values, if this change it changes in game.py event handler
        startSurface = pygame.Surface((200,60))
        startSurface.convert()  # 100, 350, 200, 60
        startSurface.fill(green)
        surface.blit(startSurface,(100,350))
        surface.blit(self.font.render("EASY", True, black), (180, 370))
        #medium button
        startSurface.convert()
        startSurface.fill(yellow)
        surface.blit(startSurface,(375,350))  ## since hard coded if this change it changes in game.py event handler
        surface.blit(self.font.render("MEDIUM",True, black), (440,370))
        #hard button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(675,350))
        surface.blit(self.font.render("HARD",True, black), (750,370))
        ## check if when mouse clicks on button it changes game state 
        startSurface.convert()
        startSurface.fill(orange)
        surface.blit(startSurface,(100,550))
        surface.blit(self.font.render("QUIT",True, black), (180,570))
        
        
    def draw_minimap(self, surface):
        s = 4
        wall = pygame.Surface((s, s))
        wall.convert()
        wall.fill((160, 160, 160)) 
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
        background.fill((255, 255, 255))
        surface.blit(background, (pygame.display.get_surface().get_width() - 20 - len(grid[0]) * s, 12))

        # the "base" x/y the use for calculating the indiviudal x/y of each tile
        x = pygame.display.get_surface().get_width() - 16 - (len(grid[0]) * s)
        y = 16

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                position = (x + (j * s), y + (i * s))
                if game.GameEnvironment.PLAYER.tile_pos == (i, j):
                    surface.blit(player, position)
                elif MazeEnvironment.MAZE.start == (i, j):
                    surface.blit(start, position)
                elif MazeEnvironment.MAZE.end == (i, j):
                    surface.blit(end, position)
                elif grid[i][j] == 1:
                    surface.blit(wall, position)

    def activeGameView(self):
        surface = pygame.display.get_surface() 
        self.maze_environment.render(surface)
        game.GameEnvironment.PLAYER.render(surface)

        self.draw_minimap(surface)

        surface.blit(self.font.render("In-game view", True, Screen.TEXT_COLOR), (12, 8))
        surface.blit(self.font.render("Move with WASD", True, Screen.TEXT_COLOR), (12, 30))
        
        
        ## back fill of health bar plus health bar
        backFillSprite = pygame.Surface((90,10))
        backFillSprite.convert()
        backFillSprite.fill(white)
        surface.blit(backFillSprite,(12,74))
        healthBarWidth = (game.GameEnvironment.PLAYER.health / 100)  * 90
        sprite = pygame.Surface((healthBarWidth,10))
        sprite.convert()
        sprite.fill(red)
        surface.blit(sprite, (12,74))
        
        
        ## Shield and Shield Backfill 
        shieldBarBackFill = (100 / 100) * 10
        shieldFill = pygame.Surface((90, shieldBarBackFill))
        shieldFill.convert()
        shieldFill.fill(white)
        surface.blit(shieldFill, (12,52))
        shieldBarWidth = (game.GameEnvironment.PLAYER.shield / 100 ) * 90
        shieldSprite = pygame.Surface((shieldBarWidth,10))
        shieldSprite.convert()
        shieldSprite.fill(blue)
        surface.blit(shieldSprite, (12,52))
        surface.blit(self.font.render("Speed is: " + str(game.GameEnvironment.PLAYER.speed), True,
                                      Screen.TEXT_COLOR), (12, 140))
        surface.blit(
            self.font.render("Arrows: " + str(int(game.GameEnvironment.PLAYER.arrow_count)), True, Screen.TEXT_COLOR),
            (12, surface.get_height() - 29))
        surface.blit(self.font.render("Sword cooldown: " + str(game.GameEnvironment.PLAYER.weapon.in_cooldown), True,
                                      Screen.TEXT_COLOR), (12, surface.get_height() - 29 - 22))

    def victory(self):
        pygame.display.get_surface().blit(self.font.render("Victory screen", True, Screen.TEXT_COLOR), (12, 8))
        pygame.display.get_surface().blit(
            self.font.render("Press ENTER to play again, or BACKSPACE to quit", True, Screen.TEXT_COLOR), (12, 30))
        pygame.display.get_surface().blit(self.font.render("Score: 9999", True, Screen.TEXT_COLOR), (12, 52))
        pygame.display.get_surface().blit(
            self.font.render("Top 10 scores: 9999, 0, 0, 0, 0, 0, 0, 0, 0, 0", True, Screen.TEXT_COLOR), (12, 74))
        pygame.mouse.set_cursor(self.cursor)
        #RESTART BUTTON
        surface = pygame.display.get_surface() 
        startSurface = pygame.Surface((200,60))
        startSurface.convert()
        startSurface.fill(green)
        surface.blit(startSurface,(200,350))
        surface.blit(self.font.render("RESTART", True, black), (265, 370))
        #QUIT button
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(575,350))
        surface.blit(self.font.render("QUIT",True, black), (660,370))
        show_score(0, red, 'Times New Roman', 20)
        # add checck for position

    def death(self):
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
        surface.blit(self.font.render("RESTART", True, black), (265, 370))
        #QUIT BUTTON
        startSurface.convert()
        startSurface.fill(red)
        surface.blit(startSurface,(575,350))
        surface.blit(self.font.render("QUIT",True, black), (660,370))
        show_score(0, red, 'Times New Roman', 20)
        #check for position 
        
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    pygame.display.get_surface().blit(score_surface, score_rect)

    def quit(self):
        pass
