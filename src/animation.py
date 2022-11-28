import pygame
from maze import MazeEnvironment


def build_frames(image, num, reverse=False):
    w = image.get_width() / num
    h = image.get_height()
    frames = []
    if reverse:
        i = num - 1
        while i >= 0:
            frames.append(image.subsurface(i * w, 0, w, h))
            i -= 1
    else:
        for n in range(num):
            frames.append(image.subsurface((n * w, 0, w, h)))
    return frames


class Animation:
    def __init__(self, frames, frame_delay, looping, event_id):
        self.frame_delay = frame_delay
        self.frames = frames
        self.looping = looping
        self.event_id = event_id
        self.frame_index = 0
        self.frame = self.frames[0]
        self.running = False
        self.paused = False

    def start(self):
        if self.event_id not in MazeEnvironment.ANIMATION_TIMERS:
            MazeEnvironment.ANIMATION_TIMERS.append(self.event_id)
            pygame.time.set_timer(self.event_id, self.frame_delay)
        self.frame = self.frames[0]
        self.running = True

    def restart(self):
        if not self.running:
            self.start()
        else:
            self.frame = self.frames[0]
            self.running = True

    def stop(self):
        if self.event_id in MazeEnvironment.ANIMATION_TIMERS:
            pygame.time.set_timer(self.event_id, 0)
            MazeEnvironment.ANIMATION_TIMERS.remove(self.event_id)
            MazeEnvironment.ENEMY_EVENT_IDS.remove(self.event_id)
        self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def next_frame(self):
        if self.paused:
            return
        self.frame_index += 1
        if self.frame_index == len(self.frames):
            if self.looping:
                self.frame_index = 0
            else:
                self.frame_index = len(self.frames) - 1
                self.running = False
        self.frame = self.frames[self.frame_index]
