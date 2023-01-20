import pygame
from pygame import mixer

class MusicManager:
    def __init__(self):
        self.tracks = ["bg2.mp3", "bg3.mp3", "bg1.mp3"]
        self.currentTrack = 0
        self.track = self.tracks[self.currentTrack % len(self.tracks)]
        self.volume = 1
        self.doMusic = True

    def play(self, *file):
        if len(file) == 0:
            file = self.track
            self.currentTrack += 1
            self.track = self.tracks[self.currentTrack % len(self.tracks)]
        else:
            file = file[0]
        mixer.music.load(f"../resources/sounds/{file}")
        mixer.music.play(-1)

    def stop(self):
        mixer.music.stop()

    def setVolume(self, volume):
        self.volume = volume
        if self.doMusic:
            mixer.music.set_volume(volume)
        else:
            mixer.music.set_volume(0)

    def setDoMusic(self, doMusic):
        self.doMusic = doMusic
        self.setVolume(self.volume)

    def pause(self, pause):
        if pause:
            mixer.music.pause()
        else:
            mixer.music.unpause()


pygame.init()