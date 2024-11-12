"""main module, starts game and main loop"""

import pygame
import game, gfx, snd, txt, input
import allmodules
import players, gamepref
import numpy as np
import time
from input_analyzer import InputAnalyzer
from music_controller import MusicController



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

def calculate_intensity(image_intensity, input_intensity):
    # Definieren der Gewichtungsfaktoren
    image_weight = 0.6
    input_weight = 0.4

    # Sicherstellen, dass beide Intensitäten verfügbar sind
    if image_intensity is not None and input_intensity is not None:
        total_intensity = (image_weight * image_intensity) + (input_weight * input_intensity)
        # Normalisieren auf den Bereich [0,1]
        total_intensity = min(max(total_intensity, 0.0), 1.0)
        return total_intensity
    else:
        return None


def process_screen(screenshot_counter):
    # Holen Sie sich das aktuelle Display-Surface
    screen_surface = pygame.display.get_surface()

    # Konvertieren Sie das Surface in ein Array
    screen_array = pygame.surfarray.array3d(screen_surface)

    # Transponieren Sie das Array, um die Achsen zu korrigieren
    screen_array = np.transpose(screen_array, (1, 0, 2))

    if screenshot_counter < 5:
        # Konvertieren Sie das Array zurück in ein Surface
        screenshot_surface = pygame.surfarray.make_surface(screen_array)
        # Speichern Sie das Bild als PNG-Datei
        pygame.image.save(screenshot_surface, f"screenshot_{screenshot_counter}.png")
        print(f"[INFO] Screenshot gespeichert: screenshot_{screenshot_counter}.png")

    # Reduzieren Sie die Auflösung (z. B. auf 1/4 der Originalgröße)
    small_array = screen_array[::4, ::4]

    # Konvertieren Sie in Graustufen
    gray_array = np.dot(small_array[...,:3], [0.2989, 0.5870, 0.1140])

    # Optional: Normieren Sie die Werte
    gray_array = gray_array / 255.0

    # Berechnen Sie das durchschnittliche Helligkeitsniveau
    average_brightness = np.mean(gray_array)

    # Extrahieren Sie weitere Merkmale nach Bedarf

    return average_brightness

def get_intensity_level(intensity):
    if intensity < 0.2:
        return 1
    elif intensity < 0.4:
        return 2
    elif intensity < 0.6:
        return 3
    elif intensity < 0.8:
        return 4
    else:
        return 5

def gamemain(args):
    #initialize all our code (not load resources)
    pygame.init()
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

    # Initialisieren des Musikcontrollers
    music_controller = MusicController()

    # Starten der Musik
    music_controller.play_music()

    previous_intensity_level = None

    screenshot_counter = 0

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

        # Erfassen und Verarbeiten des Screenshots
        image_intensity = process_screen(screenshot_counter)
        # Hier können Sie die image_intensity weiter verwenden
        if screenshot_counter < 5:
            screenshot_counter += 1
        # Erfassen der Eingabeintensität
        input_intensity = input_analyzer.get_input_intensity()
        # Gesamte Intensität berechnen
        total_intensity = calculate_intensity(image_intensity, input_intensity)

        if total_intensity is not None:

            current_intensity_level = get_intensity_level(total_intensity)
            # Musik entsprechend aktualisieren

            if current_intensity_level != previous_intensity_level:
                print(f"[INFO] Intensitätsstufe geändert zu: {current_intensity_level}")
                previous_intensity_level = current_intensity_level

            music_controller.update_music(total_intensity)
        
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



