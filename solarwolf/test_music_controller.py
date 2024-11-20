from scamp import *
from music_controller import MusicController  # Replace with your actual module name

def main():
    # Initialize the MusicController
    controller = MusicController()

    # Start the SCAMP session directly without a separate thread
    print("Music playing... Listen to ensure everything works correctly.")
    #instruments.print_soundfont_presets()
    controller.run_scamp()
    # Run the SCAMP session on the main thread
    controller.update_music(2)
    controller.session.wait_forever()
    # Play music for a set amount of time (e.g., 30 seconds) to listen and verify
    #controller.session.wait(2)  # Adjust the time as needed

    # Stop the music after the specified duration
    print("Stopping music...")

if __name__ == "__main__":
    main()
