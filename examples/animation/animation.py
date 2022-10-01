import sys
import pygame

WIDTH = 300
HEIGHT = 300
TARGET_FPS = 60


class Animation:
    def __init__(self, filename, num_frames, frame_delay, looping):
        self.filename = filename
        self.num_frames = num_frames
        # time between frames in milliseconds
        self.frame_delay = frame_delay
        self.frames = []
        self.frame_index = 0
        self.frame = pygame.Surface((0, 0))
        self.looping = looping
        # these initialization methods are called in the constructor but could
        # be pulled out and done elsewhere if performance becomes an issue
        self.build_frames()
        self.create_frame_change_event()

    def build_frames(self):
        # automatically cut frames from the image
        # since each frame is assumed the same size and
        # directly next to one another, in order
        image = pygame.image.load(self.filename)
        image.convert_alpha()
        # this width calculation only works when all frames are the same size
        w = image.get_width() / self.num_frames
        h = image.get_height()
        for n in range(self.num_frames):
            # a "sub-image" is taken from the full image at x=n * width, y = 0
            self.frames.append(image.subsurface((n * w, 0, w, h)))
        # start animation at beginning by setting frame to frames[0]
        self.frame = self.frames[0]

    def create_frame_change_event(self):
        # this will only work if there's only one animation in the whole game
        # each animation timer needs a unique id but for this example assigning
        # the id in the animated class is fine since there's only one
        # in the actual game, ids for the timers need to be stored somewhere else
        # to make sure they're all unique
        event_id = pygame.USEREVENT + 1
        pygame.time.set_timer(event_id, self.frame_delay)

    def cancel_frame_change_event(self):
        # see comment in create_frame_change_event about the event id
        event_id = pygame.USEREVENT + 1
        pygame.time.set_timer(event_id, 0)

    def next_frame(self):
        self.frame_index += 1
        if self.frame_index == len(self.frames):
            if self.looping:
                self.frame_index = 0
            else:
                self.frame_index = len(self.frames) - 1
                self.cancel_frame_change_event()
        self.frame = self.frames[self.frame_index]


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation = Animation("particle.png", 9, 75, True)

    def render(self, surface):
        surface.blit(self.animation.frame, (self.x, self.y))


def main():
    pygame.init()
    pygame.display.set_caption("Animation Example")

    fps = pygame.time.Clock()
    # get the display window's surface
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

    # create a Particle object starting in the center of the screen
    # making it global allows access outside of main()
    global particle
    particle = Particle(WIDTH / 2 - 26, HEIGHT / 2 - 26)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # display window was closed
                pygame.quit()
                sys.exit()
            animation_event_handler(event)

        render(display_surface)

        # refresh display window's surface
        pygame.display.flip()
        # lock to 60 fps
        fps.tick(TARGET_FPS)


def animation_event_handler(event):
    # see important comment in animated class about event ids
    if event.type == pygame.USEREVENT + 1:
        particle.animation.next_frame()


def render(surface):
    # having a background is important because otherwise previous renders are visible
    background = pygame.Surface((WIDTH, HEIGHT))
    background.convert()
    background.fill((0, 0, 0))
    surface.blit(background, (0, 0))

    particle.render(surface)


if __name__ == "__main__":
    main()
