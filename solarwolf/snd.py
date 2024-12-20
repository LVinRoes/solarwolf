"""audio class, helps everyone to audio"""

import pygame, os
from pygame.locals import *
import game, input


mixer = music = None
sound_cache = {}


def initialize():
    global mixer, music
    try:
        import pygame.mixer as pymix
        pymix.init(22000, 8, 0)
        mixer = pymix
        music = pymix.music
        return 1
    except (ImportError, pygame.error):
        return 0


def preload(*names):
    "loads a sound into the cache"
    if not mixer:
        for name in names:
            sound_cache[name] = None
        return
    for name in names:
        if name not in sound_cache:
            fullname = os.path.join('data', 'audio', name+'.wav')
            file = game.get_resource(name+'.wav')
            try: sound = mixer.Sound(fullname)
            except: sound = None
            sound_cache[name] = sound
    return


def fetch(name):
    if name not in sound_cache:
        preload(name)
    return sound_cache[name]


def play(name, volume=0.3, pos=-1):
    volume = 0.3
    prefvolume = [0, 0.6, 1.0][game.volume]
    volume *= prefvolume
    if not volume:
        return
    sound = fetch(name)
    if sound:
        chan = sound.play()
        if not chan:
            chan = pygame.mixer.find_channel(1)
            chan.play(sound)
        if chan:
            if pos == -1:
                percent = 0.5
            else:
                percent = (pos / 700.0)
            inv = 1.0 - percent
            chan.set_volume(inv*volume, percent*volume)
    return

CurrentSong = None
CurrentVolume = 1.0
SwitchingSongs = 0

def playmusic(musicname, volume=1.0):
    if not music or not game.music:
        return
    global CurrentSong, SwitchingSongs, CurrentVolume
    if musicname == CurrentSong:
        return
    CurrentSong = musicname
    CurrentVolume = volume
    if SwitchingSongs:
        CurrentSong = musicname
    SwitchingSongs = 1
    if music.get_busy():
        music.set_endevent(input.FINISHMUSIC)
        music.fadeout(1000)
    else:
        prefvolume = [0, 0.6, 1.0][game.music]
        fullname = os.path.join('data', 'music', musicname)
        try:
            music.load(fullname)
            music.play(-1)
            music.set_volume(prefvolume*CurrentVolume)
        except pygame.error as e:
            print(f"Fehler beim Laden oder Abspielen der Musik: {e}")
            pass  # Fehler ignorieren, wenn Musikdatei nicht gefunden wird
    return


def finish_playmusic():
    global CurrentSong, SwitchingSongs, CurrentVolume
    SwitchingSongs = 0
    prefvolume = [0, 0.6, 1.0][game.music]
    fullname = os.path.join('data', 'music', CurrentSong)
    music.load(fullname)
    music.play(-1)
    music.set_volume(prefvolume*CurrentVolume)
    return



def tweakmusicvolume():
    if not music:
        return
    prefvolume = [0, 0.6, 1.0][game.music]
    if prefvolume == 0:
        music.stop()
    else:
        if not music.get_busy():
            try:
                music.play(-1)
            except pygame.error as e:
                print(f"Fehler beim Abspielen der Musik: {e}")
                pass  # Fehler ignorieren, wenn Musik nicht geladen ist
        music.set_volume(prefvolume*CurrentVolume)
    return
