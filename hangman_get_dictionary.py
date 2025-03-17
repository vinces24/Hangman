from nltk.corpus import words
import os

# common words dictionary

save_path = "Hangman"
file_name = "commonWords.csv"
completeName = os.path.join(save_path, file_name)

c = open(completeName, "r")
common_word_list = c.read().split()
c.close()

save_path = "Hangman"
file_name = "hangman_common_words_dictionary.txt"
completeName = os.path.join(save_path, file_name)

t = open(completeName, "w")
t.close()

t = open(completeName, "w")
x = [i.lower() for i in common_word_list if len(i) >= 6]
for i in x:
    t.write(i + "\n")
t.close()