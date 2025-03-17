import random
import collections
import os

save_path = "Hangman"
file_name = "hangman_common_words_dictionary.txt"
completeName = os.path.join(save_path, file_name)

c = open(completeName, "r")
word_list = c.read().split()
c.close()

# gets user input and returns error if input isn't a single letter or an entire word 
def userInput(word):
    while True:
        try:
            user = (input("Enter your guess: ")).lower()
            if not(user.isalpha()) or len(user) != 1 and len(user) != len(word):
                raise ValueError
        except ValueError:
            print("Error, please enter a valid letter")
            continue
        return user

def letterCount(word):
    count = {}
    for s in word:
        if s in count: count[s] += 1
        else: count[s] = 1
    return count

def letterIndex(word, count):
    ind = {}
    for i in word:
        if count[i] > 1:
            if i in ind.keys(): ind[i].append(word.index(i, (ind[i][-1]+1)))
            else: ind[i] = [word.index(i)]
        else: ind[i] = word.index(i)
    return ind

def answerCompare(word, answer, count, reveal_letter, lguesses, wguesses):
    index = letterIndex(word, count)
    more_than_one = [key for key in count if count[key] > 1]
    if len(answer) == len(word):
        if answer == word: return answer, lguesses, wguesses
        else:
            if answer not in wguesses:
                wguesses.append(answer)
                wguesses.sort()
    if answer in word:
        if answer in more_than_one:
            for i in index[answer]: reveal_letter[i] = answer       
        else: reveal_letter[index[answer]] = answer
    else:
        if answer not in lguesses and answer not in wguesses:
            lguesses.append(answer)
            lguesses.sort()
    reveal_letter = collections.OrderedDict(sorted(reveal_letter.items()))
    return reveal_letter, lguesses, wguesses

def formatAnswer(word, answer, count_word, reveal_letter, letter_guesses, word_guesses):
    final, lguesses, wguesses = answerCompare(word, answer, count_word, reveal_letter, letter_guesses, word_guesses)
    tries = len(lguesses) + len(wguesses)
    if isinstance(final, str): pass
    else: final = " ".join([i for i in final.values()])
    print("")
    print("Guess: {}".format(answer))
    print("Correct Guesses: {}".format(final))
    if len(lguesses) > 0: print("Incorrect Letters: {}".format(lguesses))
    if len(wguesses) > 0: print("Incorrect Words: {}".format(wguesses))
    print("Tries Left: {}".format(10-tries))
    print("")
    return final.replace(" ", ""), tries

word = word_list[random.randint(0, (len(word_list) - 1))]
count_word = letterCount(word)
letter_guesses = []
word_guesses = []
reveal_letter = {}
for i in range(len(word)): reveal_letter[i] = "_"
print("Word: {}".format(" ".join([i for i in reveal_letter.values()])))
print("")
answer = userInput(word)
final, tries = formatAnswer(word, answer, count_word, reveal_letter, 
        letter_guesses, word_guesses)
while final != word:
    answer = userInput(word)
    final, tries = formatAnswer(word, answer, count_word, reveal_letter, 
        letter_guesses, word_guesses)
    if tries == 10:
        print("You lost! Better luck next time!")
        break

if final == word: print("You win!")

print("Answer: {}".format(word))