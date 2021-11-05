import pygame.mixer
import os
from xretro import utility


class SoundBox(object):
    def __init__(self, file):
        self.file = os.path.join(utility.sounds_folder(), file)
        self.volume: float = 1.0
        self.sound: pygame.mixer.Sound = None
        self.music = False

    def play_music(self):
        pygame.mixer.music.load(self.file)
        pygame.mixer.music.play()
        self.music = True
        return self

    def loop_music(self):
        pygame.mixer.music.load(self.file)
        pygame.mixer.music.play(loops=-1)
        self.music = True
        return self

    def unload(self):
        if self.music:
            pygame.mixer.music.unload()

    def stop(self):
        if self.music:
            pygame.mixer.music.stop()
        else:
            self.sound.stop()
        return self

    def pause(self):
        if self.music:
            pygame.mixer.music.stop()
        return self

    def resume(self):
        if self.music:
            pygame.mixer.music.unpause()
        return self

    def play(self):
        if self.sound is None:
            self.sound = pygame.mixer.Sound(self.file)
            self.sound.play()
        return self

    def loop(self):
        if not self.music:
            if self.sound is None:
                self.sound = pygame.mixer.Sound(self.file)
            self.sound.play(loops=-1)
        return self

    def volume(self, v: float):
        if self.music:
            pygame.mixer.music.set_volume(v)
        else:
            self.sound.set_volume(v)
        return self

    def fadeout(self, timemilli: int):
        if self.music:
            pygame.mixer.music.fadeout(timemilli)
        else:
            self.sound.fadeout(timemilli)
        return self

    def isbusy(self):
        if self.music:
            return pygame.mixer.music.get_busy()
        else:
            return False
