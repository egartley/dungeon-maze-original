import pygame
import game
from maze import MazeEnvironment


class Screen:
    TEXT_COLOR = (255, 255, 255)

    def __init__(self, maze_env, width, height):
        self.maze_environment = maze_env
        self.title = "Dungeon Maze"
        pygame.display.set_caption(self.title)
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 18)

    def pauseView(self):
        pygame.display.get_surface().blit(self.font.render("Pause screen", True, Screen.TEXT_COLOR), (12, 8))
        pygame.display.get_surface().blit(
            self.font.render("Press ESC again to resume playing", True, Screen.TEXT_COLOR), (12, 30))

    def startView(self):
        pygame.display.get_surface().blit(self.font.render("Start screen", True, Screen.TEXT_COLOR), (12, 8))
        pygame.display.get_surface().blit(self.font.render("Press ENTER to begin playing", True, Screen.TEXT_COLOR),
                                          (12, 30))

    def draw_minimap(self, surface):
        s = 4
        wall = pygame.Surface((s, s))
        wall.convert()
        wall.fill((160, 160, 160))
        start = pygame.Surface((s, s))
        start.convert()
        start.fill((0, 255, 0))
        end = pygame.Surface((s, s))
        end.convert()
        end.fill((255, 0, 0))
        player = pygame.Surface((s, s))
        player.convert()
        player.fill((138, 43, 226))

        grid = MazeEnvironment.MAZE.grid

        background = pygame.Surface((len(grid[0]) * s + 8, len(grid) * s + 8))
        background.convert()
        background.fill((255, 255, 255))
        surface.blit(background, (pygame.display.get_surface().get_width() - 20 - len(grid[0]) * s, 12))

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
        surface.blit(self.font.render("Health: " + str(game.GameEnvironment.PLAYER.health) + ", Shield: " + str(
            int(game.GameEnvironment.PLAYER.shield)), True, Screen.TEXT_COLOR), (12, 52))
        surface.blit(self.font.render("Relative XY: (" + str(game.GameEnvironment.PLAYER.relative_x) + ", " + str(
            game.GameEnvironment.PLAYER.relative_y) + ") tile=" + str(game.GameEnvironment.PLAYER.tile_pos), True,
                                      Screen.TEXT_COLOR), (12, 74))
        surface.blit(self.font.render("Active booster: " + str(game.GameEnvironment.PLAYER.active_booster), True,
                                      Screen.TEXT_COLOR), (12, 96))

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

    def death(self):
        pygame.display.get_surface().blit(self.font.render("Death screen", True, Screen.TEXT_COLOR), (12, 8))
        pygame.display.get_surface().blit(
            self.font.render("Press ENTER to play again, or BACKSPACE to quit", True, Screen.TEXT_COLOR), (12, 30))
        pygame.display.get_surface().blit(self.font.render("Get good", True, Screen.TEXT_COLOR), (12, 52))

    def quit(self):
        pass
