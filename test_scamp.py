from scamp import Session

def main():
    s = Session(tempo=120)
    piano = s.new_part("piano")
    print("Spiele Testnote...")
    piano.play_note(
        pitch=60,     # Mittleres C
        length=2.0,
        volume=0.8
    )
    print("Testnote gespielt.")

if __name__ == "__main__":
    main()
