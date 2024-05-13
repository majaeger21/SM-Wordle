import random
import sys
from time import sleep
import nltk
from nltk.corpus import brown


# from rich import print
# from rich.prompt import Prompt


def load_words():
    words = []
    with open("words.txt", "r", newline="") as f:
        for word in f:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                words.append(word)
    return words

def past_words():
    words = []
    with open("pastwords.txt", "r", newline="") as f:
        for word in f:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                words.append(word)
    return words


def find_letter_indexes_in_word(word, letter):
    return [i for i, ltr in enumerate(word) if ltr == letter]


def main():
    words = list(set(load_words()) - set(past_words()))
    my_word = "house"
    solution = "bears"
    output = '-----'
    i = 1
    while (output != 'ggggg'):
        # print(len(words))
        words, output = check(words, my_word, solution)
        output = ''.join(output)
        # print(output)
        # print(len(words))
        print( "#", i, "\tguess:", my_word, "\toutput", output, "\t words left", len(words) )
        i+=1
        my_word = next_word(words)


def check(words, input, solution):  # green>yellow>grey
    output = [];
    for i in range(5):
        if input[i] == solution[i]:
            output.append('g')
            words = update_words_green(words, input[i], i)
        elif input[i] in solution:
            output.append('y')
            words = update_words_yellow(words, input[i], i)

        else:
            output.append('-')
            words = update_words_grey(words, input[i])

    return words, output


def update_words_green(words, letter, index):
    return [x for x in words if x[index] == letter]


def update_words_yellow(words, letter, index):
    return [x for x in words if (x[index] != letter) and letter in x]


def update_words_grey(words, letter):
    return [x for x in words if letter not in x]

def next_word(words):
    # freqs = nltk.FreqDist([w.lower() for w in brown.words()])
    # words = sorted(words, key=lambda x: freqs[x.lower()], reverse=True)
    return words[0];


main();
