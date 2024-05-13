import random
import sys
from time import sleep
from rich import print
from rich.prompt import Prompt



def load_words():
    words = []

    with open("words.txt", "r", newline="") as f:
        for word in f:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                words.append(word)

    return words

def find_letter_indexes_in_word(word, letter):
    return [i for i, ltr in enumerate(word) if ltr == letter]

