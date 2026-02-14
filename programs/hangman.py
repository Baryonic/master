import random
import os

def get_word_from_file(filename):
    try:
        with open(filename, 'r') as file:
            words = file.read().split()
            return random.choice(words)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None

def play_hangman(word):
    guessed_word = ['_' for _ in word]
    attempts = 6
    guessed_letters = set()
    
    print("Welcome to Hangman!")
    print("Guess the word:")
    print(" ".join(guessed_word))
    
    while attempts > 0 and '_' in guessed_word:
        guess = input("\033[37mEnter a letter: ").lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("\033[31mPlease enter a single valid letter.")
            continue
        
        if guess in guessed_letters:
            print("\033[31mYou've already guessed this letter!")
            continue
        
        guessed_letters.add(guess)
        
        if guess in word:
            print(f"\033[92mGood guess! {guess} is in the word.")
            for idx, letter in enumerate(word):
                if letter == guess:
                    guessed_word[idx] = guess
        else:
            attempts -= 1
            print(f"\033[31mWrong guess! You have {attempts} attempts left.")
        
        print(" ".join(guessed_word))
    
    if '_' not in guessed_word:
        print(f"\033[92mCongratulations!\033[33m You've guessed the word: \033[92m{word}")
    else:
        print(f"\033[31mGame over! The word was: {word}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "words.txt")
    word = get_word_from_file(filename)
    if word:
        play_hangman(word)

if __name__ == "__main__":
    main()
