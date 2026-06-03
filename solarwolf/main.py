"""main module, starts game and main loop"""
import threading
import pygame
import game, gfx, snd, txt, input
import allmodules
import players, gamepref
import numpy as np
import time
from adaptive_music.input_analyzer import InputAnalyzer
from adaptive_music.music_controller import *
from adaptive_music.screen_processor import ScreenProcessor
import logging
from adaptive_music.intensity_calculator import IntensityCalculator
from adaptive_music.intensity_calc_GS import Intensity_calc_GS
from gameplay import GamePlay
from players import Player

# For plotting the graph
import matplotlib.pyplot as plt
import os  # Needed to check/create the folder
import sys

logging.basicConfig(level=logging.DEBUG)

last_update_time = time.time()
update_interval = 0.5  # in seconds

help_string ="""
USAGE: solarwolf [-mode=Obs|GS|Const]

  -mode=<mode>  Starts the game with the specified music mode.
     mode Obs   Music is driven by external observations (keyboard activity & screen differences).
     mode GS    Music adapts to internal game state variables.
     mode Const Music play with a constant intensity (level 3).
"""

def main(args):
    if "-h" in args or "--help" in args:
        print(args)
        print(help_string)
        sys.exit(0)
    try:
        print("Starting game main..")
        gamemain(args)
    except KeyboardInterrupt:
        print('Keyboard Interrupt...')
        print('Exiting')

def gamemain(args):
    # Initializations (music, display, input, etc.)
    music_cont = MusicController()
    pygame.display.init()
    pygame.font.init()
    pygame.joystick.init()
    pygame.mixer.quit() # <- disable original game sound
    game.clock = pygame.time.Clock()

    players.load_players()
    input.load_translations()
    gamepref.load_prefs()

    size = 800, 600
    full = 0 # <- always windowed
    #full = game.display
    #if '-window' in args:
    #    full = 0
    gfx.initialize(size, full)
    pygame.display.set_caption('SolarWolf')

    #if not '-nosound' in args:
    #    snd.initialize()
    input.init()

    if not txt.initialize():
        raise pygame.error("Pygame Font Module Unable to Initialize")

    # Create the starting game handler
    from gameinit import GameInit
    from gamefinish import GameFinish
    game.handler = GameInit(GameFinish(None))

    # Timer to control the stars
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    gamestart = pygame.time.get_ticks()
    numframes = 0

    input_analyzer = InputAnalyzer()

    # Initialize the ScreenProcessor
    screen_processor = ScreenProcessor()

    # Start the music controller thread
    music_thread = threading.Thread(target=music_cont.run_scamp, daemon=True)
    music_thread.start()
    
    def delayed_dump():
        time.sleep(5)
        music_cont.debug_dump_precomputed_data()
    threading.Thread(target=delayed_dump, daemon=True).start()
    ########################################################################################
    name = "1"

    game.player = Player(name=name, score=20)
    game.player.name = name

    # In the main function, after the initializations:
    level_seed = 2 # e.g. 0, 1 or 2
    game.level_seed = level_seed
    
    # Option for intensity calculation:
    # opt 0: internal calc off (Obs), 1: internal calc on (GS), 2: internal calc with constant (Const)
    opt = 0

    try:
        for option in args:
            if '-mode' in option:
                mode = option.split("=")[1]
                print("Mode request found:", mode)
                if "Observations".lower().startswith(mode.lower()):
                    opt = 0
                    print("Mode set to Obs")
                elif "GS".lower().startswith(mode.lower()):
                    opt = 1
                    print("Mode set to GS")
                elif "Constant".lower().startswith(mode.lower()):
                    opt = 2
                    print("Mode set to Const")
                else:
                    print("Invalid mode. Must be one of Obs, GS, Const, and not", mode)
    except:
        print("Option -mode could not be parsed. Fall back to mode 'Obs'.")
        opt = 0
        
    print("Set mode opt code:", opt)


    # For the layout – which level layouts should be selected:
    if level_seed == 0:
        game.level_layout_sequence = [10, 27, 28, 0]
    elif level_seed == 1:
        game.level_layout_sequence = [11, 28, 29, 1]
    elif level_seed == 2:
        game.level_layout_sequence = [12, 29, 27, 2]

    # For the difficulty level – this ensures the difficulty value increases as well:
    if level_seed == 0:
        game.forced_difficulty_sequence = [10, 27, 28, 0]
    elif level_seed == 1:
        game.forced_difficulty_sequence = [11, 28, 29, 1]  # Example values: level 10, then 20, then 30
    elif level_seed == 2:
        game.forced_difficulty_sequence = [12, 29, 27, 2]

    if opt == 0:
        use_internal_calc = False
        const = False
    elif opt == 1:
        use_internal_calc = True
        const = False
    elif opt == 2:
        use_internal_calc = True
        const = True
    ##########################################################################################


    intensity_calculator = IntensityCalculator()
    my_int_calc = None
    previous_intensity_level = None

    while game.handler:
        numframes += 1
        handler = game.handler
        if handler != None and hasattr(handler, 'starting'):
            handler.starting()
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                fps = game.clock.get_fps()
                gfx.starobj.recalc_num_stars(fps)
                continue
            elif event.type == pygame.ACTIVEEVENT:
                if event.state == 4 and event.gain:
                    pygame.display.update()
                elif event.state == 2:
                    if hasattr(game.handler, 'gotfocus'):
                        if event.gain:
                            game.handler.gotfocus()
                        else:
                            game.handler.lostfocus()
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if event.mod & pygame.KMOD_ALT:
                    game.display = not game.display
                    gfx.switchfullscreen()
                    continue
            inputevent = input.translate(event)
            if inputevent.normalized != None:
                inputevent = input.exclusive((input.UP, input.DOWN, input.LEFT, input.RIGHT), inputevent)
                handler.input(inputevent)
            elif event.type == pygame.QUIT:
                game.handler = None
                break
            handler.event(event)
            input_analyzer.process_event(event)

        handler.run()
        game.clockticks = game.clock.tick(40)
        gfx.update()

        current_intensity_level = 1

        current_time = time.time()

        if isinstance(game.handler, GamePlay) and use_internal_calc:
            #print("alternative calculation")
            if my_int_calc is None:
                my_int_calc = Intensity_calc_GS(game.handler)
            total_intensity = my_int_calc.calculate_total_intensity()
            current_intensity_level = my_int_calc.get_intensity_level(total_intensity, previous_intensity_level)

        else:
            my_int_calc = None
            image_intensity = screen_processor.process_screen()
            screen_processor.update_demo_capture()
            input_intensity = input_analyzer.get_input_intensity()
            total_intensity = intensity_calculator.calculate_total_intensity(image_intensity, input_intensity)
            current_intensity_level = intensity_calculator.get_intensity_level(total_intensity)
        
        # Update music accordingly
        if current_intensity_level != previous_intensity_level:
            if const:
                current_intensity_level = 3
            music_cont.update_music(current_intensity_level)
            # Optional: debug output
            print(f"Image Intensity: {image_intensity}")
            print(f"Input Intensity: {input_intensity}")
            print(f"Total Intensity (before smoothing): {total_intensity}")
            print(f"Smoothed Total Intensity: {current_intensity_level}")

        previous_intensity_level = current_intensity_level

        while not pygame.display.get_active():
            pygame.time.wait(100)
            pygame.event.pump()

    gameend = pygame.time.get_ticks()
    runtime = (gameend - gamestart) / 1000.0

    # Uninitialization and saving data
    input.save_translations()
    players.save_players()
    gamepref.save_prefs()
    pygame.quit()
