import language
import math
import numpy as np
import string


class Vocabulary:
    low_letters = list(string.ascii_lowercase)
    up_letters = list(string.ascii_uppercase)

    characters = []  # List of sentence of characters for training
    characters_testing = [] # List of sentences of characters for testing

    training_table_chars = []
    training_table_classes = []
    scores = []

    # 0: Fold the corpus to lowercase and use only the 26 letters of the alphabet [a-z]
    # 1: Distinguish up and low cases and use only the 26 letters of the alphabet [a-z, A-Z]
    # 2: Distinguish up and low cases and use all characters accepted by the built-in isalpha() method
    def __init__(self, v, tweets):  # Initialize by getting all characters
        self.construct_corpus(v, tweets, self.characters) # Training
    
    def construct_corpus(self, v, tweets, chars): # chars can be used for the training of testing
        for i in range(len(tweets)):
            chars.append([])
            for letter in tweets[i].get_message():
                if v == '0':
                    if letter.islower():
                        chars[i].append(letter)
                elif v == '1':
                    if letter.islower() or letter.isupper():
                        chars[i].append(letter)
                elif v == '2':
                    if letter.islower() or letter.isupper() or letter.isalpha():
                        chars[i].append(letter)

    def class_probability(self, i, tweets):  # example: compute P('eu') = count('eu) / count(all docs)
        count_doc_i = 0
        count_all_doc = len(tweets)
        prob_i = 0
        for t in range(len(self.characters)):
            if tweets[t].get_language() == i.value:
                count_doc_i = count_doc_i + 1
        prob_i = count_doc_i / count_all_doc
        return prob_i

    def cond_probability(self, i, j, tweets, letters, lang,
                         d):  # example: compute P('a'|eu) = count('a', eu) / sum(count('a', eu))
        count_j_i = 0
        sum_j_i = 0
        prob_j_i = 0
        for t in range(len(self.characters)):
            if tweets[t].get_language() == i.value:
                count_j_i = count_j_i + self.characters[t].count(
                    letters[j])  # Getting the number of characters in each languages class
                sum_j_i = sum_j_i + len(self.characters[t])  # Getting the sum of all characters in each language class
        prob_j_i = (count_j_i + float(d)) / (sum_j_i + float(d) * len(letters))  # with smoothing d
        return prob_j_i

    def determite_vocabulary(self, v):
        char_size = 0
        letters = []

        if v == '0':
            char_size = len(self.low_letters)
            letters = self.low_letters.copy()
        elif v == '1' or v == '2':
            char_size = len(self.low_letters) + len(self.up_letters)
            letters = (self.low_letters + self.up_letters).copy()  # Merge the two

        info = dict()
        info['char_size'] = char_size
        info['letters'] = letters
        return info

    def train(self, v, d, tweets):
        lang = language.Language
        info = self.determite_vocabulary(v)
        char_size = info.get("char_size")
        letters = info.get("letters")

        print("Training the model with vocabulary type V = " + v + " and " + str(len(tweets)) + " tweets...")
        for i in iter(lang):  # For all classes i
            self.training_table_classes.append(self.class_probability(i, tweets))
            for j in range(char_size):  # For all characters in vocabulary j
                self.training_table_chars.append(self.cond_probability(i, j, tweets, letters, lang, d))

    def test(self, v, tweets):
        self.construct_corpus(v, tweets, self.characters_testing)
        info = self.determite_vocabulary(v)
        lang = language.Language
        char_size = info.get("char_size")
        letters = info.get("letters")
        score = 0

        print("Testing the model...")

        languages = ['eu', 'ca', 'gl', 'es', 'en', 'pt']
        for i in range(len(tweets)):
            for j in range(len(languages)):
                if tweets[i].get_language() == languages[j]:
                    score = math.log10(self.training_table_classes[j])
                for k in range(char_size):
                    if letters[k] == self.characters_testing[i]:
                        score = score + math.log10(self.training_table_chars[j][k])
                self.scores.append(score)
            self.printScores(i)

    def printScores(self, i):
        languages = ['Basque', 'Catalan', 'Galican', 'Spanish', 'English', 'Portuguese']  # for better printing
        index = np.argmax(self.scores)  # Gets the index of the maximum score
        print('The scores for tweet #' + str(i) + ' are...')

        for i in range(len(language.Language)):
            print(languages[i] + ': ' + str(self.scores[i]) + ", ")

    def get_characters(self):
        return self.characters

    def get_score(self):
        return self.score
