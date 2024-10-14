import pygame
import wave
import numpy


class AudioPlayer:

    def __init__(self, audio_file, speed=1, volume=1):
        self.audio_file = f'assets\\audio\\{audio_file}.mp3'
        self.channel = pygame.mixer.find_channel(True)
        self.channel.set_volume(volume)

        if self.channel:
            self.sound = pygame.mixer.Sound(self.audio_file)

            original_array = pygame.sndarray.array(self.sound)

            indices = numpy.arange(0, len(original_array), speed)
            indices = indices[indices < len(original_array)].astype(int)
            resampled_array = original_array[indices]

            self.sound = pygame.sndarray.make_sound(resampled_array)
        else:
            print('No available channel to play the audio.')

    def start(self, loops):
        if self.channel:
            self.channel.play(self.sound,  loops)

    def stop(self):
        if self.channel:
            self.channel.stop()

    def fade(self):
        if self.channel:
            self.channel.fadeout(1000)

    def pause(self):
        if self.channel:
            self.channel.pause()

    def unpause(self):
        if self.channel:
            self.channel.unpause()

    def is_playing(self):
        return self.channel.get_busy() if self.channel else False


class Audio:
    CHANNEL_COUNT = 4
    WALKING_SPEEDS = {
        'sand': 1.3,
        'water': 1.3
    }
    BG_VOLUMES = {
        'sand': 0.4
    }

    def __init__(self, game):
        self.game = game
        self.set_audio_location('sand')

    def set_audio_location(self, biome):
        self.bg_audio = AudioPlayer(f'{biome}_bg', self.BG_VOLUMES[biome])
        self.bg_audio.start(-1)
        self.walking_audio = AudioPlayer(f'{biome}_walk', self.WALKING_SPEEDS[biome])
        self.walking_audio.start(-1)

    def update(self):
        if self.game.player.state == 'moving':
            self.walking_audio.unpause()
        else:
            self.walking_audio.pause()
