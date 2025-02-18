import random

def shuffle_list(numbers):
    # Erstelle eine Kopie der Liste, um das Original nicht zu verändern
    shuffled = numbers.copy()
    random.shuffle(shuffled)
    return shuffled

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    print("Originale Liste:", numbers)
    shuffled_numbers = shuffle_list(numbers)
    print("Zufällig angeordnete Liste:", shuffled_numbers)
