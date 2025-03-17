import random
import collections
import os
import pygame
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox
from typing import Union

pygame.init()

# access list of all hangman word choices
save_path = "Hangman"
file_name = "hangman_common_words_dictionary.txt"
completeName = os.path.join(save_path, file_name)

c = open(completeName, "r")
word_list = c.read().split()
c.close()

# all lower case letters in ascii as pygame needs
allowed_list = [i for i in range(97, 123)]
# enter = 13, escape = 27, space = 32
other_list = [13, 27, 32] 

def letterCount(word: str) -> dict:
    """returns the counts of the letters in a word"""
    count = {}
    for s in word:
        if s in count: count[s] += 1
        else: count[s] = 1
    return count

def letterIndex(word: str, count: dict) -> dict:
    """returns the index of each letter in a word"""
    ind = {}
    for i in word:
        if count[i] > 1:
            if i in ind.keys(): ind[i].append(word.index(i, (ind[i][-1]+1)))
            else: ind[i] = [word.index(i)]          
        else: ind[i] = word.index(i)
    return ind

def messageBox(subject: str, content: str):
    """displays information in a pop-up window"""
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try: root.destroy()
    except: pass

def playAgain() -> bool:
    """asks user to play again"""
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    play_again = messagebox.askyesno("Play Again", "Do you want to play again?")
    try: root.destroy()
    except: pass
    return play_again

def answerCompare(word: str, count: dict, reveal_letter: dict, guesses: list, 
                allowed_list: list, other_list: list, window: pygame.Surface) -> Union[collections.OrderedDict, list]:
    """compares user input to the word"""
    # gets index of each letter in the word
    index = letterIndex(word, count)
    # if letter appears more than once, is in this list
    more_than_one = [key for key in count if count[key] > 1]
    for event in pygame.event.get():
        # quit game if closed out of
        if event.type == pygame.QUIT: pygame.quit()
        # if key is pressed, do this
        if event.type == pygame.KEYDOWN:
            # transforms ascii value to character
            x = pygame.key.name(event.key)
            # if the key pressed is a lower case letter
            if event.key in allowed_list:
                # completely resets screen
                # need to do so I can rewrite items on screen
                # easier than erasing specific parts,
                # although that would be more efficient
                window.fill((0,0,0))
                pygame.display.update()
                if x in word:
                    if x in more_than_one:
                        # cycle through indexes and show each one
                        for z in index[x]:
                            reveal_letter[z] = x
                    else:
                        # show the letter in the correct position
                        reveal_letter[index[x]] = x
                else:
                    # if letter is not in the word and not already in guesses
                    # append letter to guesses
                    if x not in guesses:
                        guesses.append(x)
                        guesses.sort()
            # if the key pressed is not a character
            # but is a space, enter, or escape
            # then don't do anything
            # (this is notably used when error is shown and user wants
            # to close box without using a mouse and using keyboard instead)
            elif event.key in other_list: pass
            # if key pressed is neither character not space, enter, or escape
            # then show error and don't count keypress as guess
            else: messageBox("Incorrect input", "Please enter a lowercase letter")
    reveal_letter = collections.OrderedDict(sorted(reveal_letter.items()))
    return reveal_letter, guesses

def writeText(string: str, window: pygame.Surface, pos: tuple, font: int):
    """displays text on screen"""
    font = pygame.font.SysFont('arial', font) 
    text = font.render(string, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = pos
    window.blit(text, textRect)
    pygame.display.update()

def changePic(window: pygame.Surface, letter_guesses: list):
    """changes the hangman picture displayed"""
    image = pygame.image.load(r"Hangman/Hangman {}.jpg".format(len(letter_guesses)))
    window.blit(image, (500,177))
    pygame.display.update()

def reset() -> Union[pygame.Surface, str, list, dict]:
    """resets the game (starts a new one)"""
    # resets window
    window = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Hangman")
    # chooses a random word from the list of possible answers
    word = word_list[random.randint(0, (len(word_list) - 1))]
    # resets guesses
    letter_guesses = []
    reveal_letter = {}
    for i in range(len(word)): reveal_letter[i] = "_"
    # resets picture of hangman
    changePic(window, letter_guesses)
    return window, word, letter_guesses, reveal_letter

def main():
    # set up game
    win, word, letter_guesses, reveal_letter = reset()
    messageBox("How to play", "Pick a letter Guess the word Before the man is hung")
    flag = True
    clock = pygame.time.Clock()
    writeText(" ".join(reveal_letter.values()), win, (500, 100), 45)
    while flag:
        pygame.time.delay(10)
        clock.tick(5)
        reveal_letter, letter_guesses = answerCompare(word, letterCount(word), reveal_letter, 
                        letter_guesses, allowed_list, other_list, win)
        # changes hangman picture and letter guesses
        changePic(win, letter_guesses)
        writeText(" ".join(reveal_letter.values()), win, (500, 100), 45)
        writeText(", ".join(letter_guesses), win, (260, 325), 45)
        if len(letter_guesses) > 0: writeText("Incorrect guesses: ", win, (260, 260), 45)
        # if user guesses the word, then end game
        if "".join(reveal_letter.values()) == word: 
            messageBox("Game Over!", "Congrats on guessing the word! The word was {}".format(word))
            play_again = playAgain()
            if play_again: win, word, letter_guesses, reveal_letter = reset()
            else: break
        # if tries run out (man is hanged), then end game
        if len(letter_guesses) == 10: 
            messageBox("Game Over!", "You ran out of tries! The word was {}".format(word))
            play_again = playAgain()
            if play_again: win, word, letter_guesses, reveal_letter = reset()
            else: break
    
main()