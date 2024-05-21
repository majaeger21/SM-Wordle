import random
import sys
from time import sleep
from rich import print
from rich.prompt import Prompt


def play():
    print("""[indian_red1]

 ____        __  __ 
/ ___|   _  |  \/  |
\___ \ _| |_| |\/| |
 ___) |_   _| |  | |
|____/  |_| |_|  |_|
__        _____  ____  ____  _     _____   ____   ___  _ __     _______ ____  
\ \      / / _ \|  _ \|  _ \| |   | ____| / ___| / _ \| |\ \   / / ____|  _ \ 
 \ \ /\ / / | | | |_) | | | | |   |  _|   \___ \| | | | | \ \ / /|  _| | |_) |
  \ V  V /| |_| |  _ <| |_| | |___| |___   ___) | |_| | |__\ V / | |___|  _ < 
   \_/\_/  \___/|_| \_\____/|_____|_____| |____/ \___/|_____\_/  |_____|_| \_\    

    [indian_red1]
    """)

    sleep(2)

    guess_results = ""
    answer_words, all_words = load_txts()
    number_of_guesses = 0
    ignore_chars = ""

    while len(answer_words) > 0:
        print(f"[light_slate_blue1]{len(answer_words)}[/light_slate_blue1] [white]{'word' if len(answer_words) == 1 else 'words'} remaining[/white]")

        current_guess = guess_word(all_words, answer_words, ignore_chars)
        print(f"[white]Current guess:[/white] [light_slate_blue1]{current_guess}[/light_slate_blue1]")

        guess_results = Prompt.ask("[plum4]Guess result: [/plum4]").strip().lower()

        if not results(guess_results):
            continue

        number_of_guesses += 1

        if guess_results == "ggggg":
            print(f"[green]Congratulations! The word was guessed in {number_of_guesses} attempts.[/green]")
            return number_of_guesses

        answer_words, ignore_chars = filter_words(answer_words, current_guess, guess_results, ignore_chars)

    print("[red]Could not guess the word.[/red]")
    sys.exit()

def results(guess_results):
    if len(guess_results) != 5:
        print("[red]Invalid guess result (must be exactly 5 characters).[/red]")
        return False

    if any(char not in "gyx" for char in guess_results):
        print("[red]Invalid guess result (can only contain 'g', 'y', or 'x').[/red]")
        return False

    return True

def load_txts():
    def load_file(filename):
        with open(filename, "r", newline="") as f:
            return [word.lower().strip() for word in f if len(word.strip()) == 5 and word.strip().isalpha()]

    answer_words = load_file("ans.txt")
    all_words = load_file("words.txt")

    return answer_words, all_words

def guess_word(all_words, answer_words, ignore_chars):
    letter_frequency = {}
    placement_frequency = [{} for _ in range(5)]  # Adjusted to have 5 dictionaries, one for each letter position

    if len(answer_words) <= 2:
        return answer_words[0]

    # Count letter frequency, ignoring letters that have already been guessed
    for word in answer_words:
        for i, letter in enumerate(word):
            if letter not in ignore_chars:
                if letter not in letter_frequency:
                    letter_frequency[letter] = 0
                letter_frequency[letter] += 1

                if letter not in placement_frequency[i]:
                    placement_frequency[i][letter] = 0
                placement_frequency[i][letter] += 1

    best_word = answer_words[0]
    max_frequency = 0
    max_placement_score = 0

    # Find the best word based on letter frequency, ignoring letters that have already been guessed
    for word in all_words:
        current_frequency = 0
        picked = set()
        for letter in word:
            if letter not in ignore_chars and letter not in picked:
                picked.add(letter)
                current_frequency += letter_frequency.get(letter, 0)

        if current_frequency > max_frequency:
            max_frequency = current_frequency
            best_word = word
            max_placement_score = sum(placement_frequency[i].get(word[i], 0) for i in range(len(word)))

        elif current_frequency == max_frequency:
            current_placement_score = sum(placement_frequency[i].get(word[i], 0) for i in range(len(word)))
            if current_placement_score > max_placement_score:
                max_placement_score = current_placement_score
                best_word = word

    return best_word


def filter_words(words, guess_word, guess_result, ignore_chars):
    """
    Filter remaining words based on the last guess and guess results, 
    and update ignored characters to include any new letters that are part of the solution.
    """
    new_ignore_chars = ignore_chars
    for i in range(len(guess_result)):
        if guess_result[i] != "x" and guess_word[i] not in ignore_chars:
            new_ignore_chars += guess_word[i]
        elif guess_result[i] == "x" and guess_word[i] in ignore_chars:
            new_ignore_chars = new_ignore_chars.replace(guess_word[i], "", 1)

    filtered_words = [word for word in words if match_guess_result(word, guess_word, guess_result)]
    return filtered_words, new_ignore_chars

def match_guess_result(word, guess_word, guess_result):
    """
    Return True if word fits the same pattern as the guess & guess results.
    """
    for i in range(len(guess_result)):
        if guess_result[i] == "g":
            if word[i] != guess_word[i]:
                return False
        elif guess_result[i] == "y":
            if guess_word[i] == word[i] or guess_word[i] not in word:
                return False
        elif guess_result[i] == "x":
            if word[i] == guess_word[i]:
                return False

            wrong_letter_instances_guess = find_letter_indexes_in_word(guess_word, guess_word[i])
            okCount = sum(1 for j in wrong_letter_instances_guess if guess_result[j] != "x")
            wrong_letter_instances_word = find_letter_indexes_in_word(word, guess_word[i])
            
            if len(wrong_letter_instances_word) > okCount:
                return False

    return True

def find_letter_indexes_in_word(word, letter):
    return [i for i, ltr in enumerate(word) if ltr == letter]

if __name__ == "__main__":
    total_guesses = 0
    max_guess_count = 0
    random.seed(1)

    current_guess_count = play()
    total_guesses += current_guess_count
    if current_guess_count > max_guess_count:
        max_guess_count = current_guess_count

    print(f"\n[green3]Solved in[/green3] [light_slate_blue1]{total_guesses}[light_slate_blue1] [green3]guesses[/green3]")