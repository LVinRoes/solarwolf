"""main module, starts game and main loop"""
import threading
import pygame
import game, gfx, snd, txt, input
import allmodules
import players, gamepref
import numpy as np
import time
from input_analyzer import InputAnalyzer
from music_controller import *
from solarwolf.screen_processor import ScreenProcessor
import logging
from intensity_calculator import IntensityCalculator
from intensity_calc_IS import Intensity_calc_IS
from gameplay import GamePlay

logging.basicConfig(level=logging.DEBUG)



#import psyco

#at this point, all needed pygame modules should
#be imported, so they can be initialized at the
#start of main()

last_update_time = time.time()
update_interval = 0.5  # in Sekunden


def main(args):
    try:
        gamemain(args)
    except KeyboardInterrupt:
        print('Keyboard Interrupt...')
        print('Exiting')

def gamemain(args):
    #initialize all our code (not load resources)
    # Initialisieren des Musikcontrollers
    music_cont = MusicController()
    pygame.display.init()
    pygame.font.init()
    pygame.joystick.init()
    pygame.mixer.quit()
    game.clock = pygame.time.Clock()

    players.load_players()
    input.load_translations()
    gamepref.load_prefs()

    size = 800, 600
    full = game.display
    if '-window' in args:
        full = 0
    gfx.initialize(size, full)
    pygame.display.set_caption('SolarWolf')

    if not '-nosound' in args:
        snd.initialize()
    input.init()

    if not txt.initialize():
        raise pygame.error("Pygame Font Module Unable to Initialize")

    #create the starting game handler
    from gameinit import GameInit
    from gamefinish import GameFinish
    game.handler = GameInit(GameFinish(None))

    #set timer to control stars..
    pygame.time.set_timer(pygame.USEREVENT, 1000)


    #psyco.full()
    gamestart = pygame.time.get_ticks()
    numframes = 0
    #random.seed(0)


    

    #main game loop
    lasthandler = None

    input_analyzer = InputAnalyzer()

    # Initialisieren des ScreenProcessors
    screen_processor = ScreenProcessor()

    # Starten der Musik
    #music_controller.play_music()

    opt = 0
    if opt == 0:
        use_internal_calc = False
        const = False
    elif opt == 1:
        use_internal_calc = True
        const = False
    elif opt == 2:
        use_internal_calc = True
        const = True

    intensity_calculator = IntensityCalculator()
    my_int_calc = None
    previous_intensity_level = None

    # Starten des Musikcontrollers in einem separaten Thread
    music_thread = threading.Thread(target=music_cont.run_scamp, daemon=True)
    music_thread.start()
    
    def delayed_dump():
        time.sleep(5)
        music_cont.debug_dump_precomputed_data()

    threading.Thread(target=delayed_dump, daemon=True).start()

    while game.handler:
        numframes += 1
        handler = game.handler
        if handler != lasthandler:
            lasthandler = handler
            if hasattr(handler, 'starting'):
                handler.starting()
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                fps = game.clock.get_fps()
                #print 'FRAMERATE: %f fps' % fps
                gfx.starobj.recalc_num_stars(fps)
                continue
            elif event.type == pygame.ACTIVEEVENT:
                if event.state == 4 and event.gain:
                    #uniconified, lets try to kick the screen
                    pygame.display.update()
                elif event.state == 2:
                    if hasattr(game.handler, 'gotfocus'):
                        if event.gain:
                            game.handler.gotfocus()
                        else:
                            game.handler.lostfocus()
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if event.mod&pygame.KMOD_ALT:
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
        #print 'ticks=%d  rawticks=%d  fps=%.2f'%(game.clock.get_time(), game.clock.get_rawtime(), game.clock.get_fps())
        gfx.update()

        current_intensity_level = 1

        

        if isinstance(game.handler, GamePlay) and use_internal_calc:
            print("alternative berechnung")
            if my_int_calc is None:
                # Erzeuge eine Instanz des neuen Intensitätsrechners
                my_int_calc = Intensity_calc_IS(game.handler)

            # Berechne die Intensität
            total_intensity = my_int_calc.calculate_total_intensity()
            current_intensity_level = my_int_calc.get_intensity_level(total_intensity, previous_intensity_level)
        else:
            my_int_calc = None
            image_intensity = screen_processor.process_screen()
            # Erfassen der Eingabeintensität
            input_intensity = input_analyzer.get_input_intensity()

            total_intensity = intensity_calculator.calculate_total_intensity(image_intensity, input_intensity)
            current_intensity_level = intensity_calculator.get_intensity_level(total_intensity)
        
        # Gesamte Intensität berechnen

        #############################################################################
        
        #total_intensity = my_int_calc.calculate_intensity()
        #############################################################################

        
        
        # Musik entsprechend aktualisieren
        if current_intensity_level != previous_intensity_level:
            if const:
                current_intensity_level = 3
            music_cont.update_music(current_intensity_level)
            # Optional: Debugging-Ausgabe
            # Fügen Sie nach der Berechnung der Intensitäten folgende Zeilen hinzu
            print(f"Image Intensity: {image_intensity}")
            print(f"Input Intensity: {input_intensity}")
            print(f"Total Intensity (before smoothing): {total_intensity}")
            print(f"Smoothed Total Intensity: {current_intensity_level}")

        # Aktualisiere die Lautstärken in Echtzeit

        previous_intensity_level = current_intensity_level

            
        

        while not pygame.display.get_active():
            pygame.time.wait(100)
            pygame.event.pump()

        #pygame.time.wait(10)

    gameend = pygame.time.get_ticks()
    runtime = (gameend - gamestart) / 1000.0
    #print "FINAL FRAMERATE: ", numframes, runtime, numframes//runtime


    #game is finished at this point, do any
    #uninitialization needed
    input.save_translations()
    players.save_players()
    gamepref.save_prefs()
    pygame.quit()



