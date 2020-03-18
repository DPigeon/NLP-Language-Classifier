import language
import math
import numpy as np
import string

class Vocabulary:
    low_letters = list(string.ascii_lowercase)
    up_letters = list(string.ascii_uppercase)

    characters = [] # List of sentence of characters
    training_table_chars = []
    training_table_classes = []
    scores = []

    # 0: Fold the corpus to lowercase and use only the 26 letters of the alphabet [a-z]
    # 1: Distinguish up and low cases and use only the 26 letters of the alphabet [a-z, A-Z]
    # 2: Distinguish up and low cases and use all characters accepted by the built-in isalpha() method
    def __init__(self, v, tweets): # Initialize by getting all characters
        for i in range(len(tweets)): 
                self.characters.append([])
                for letter in tweets[i].get_message():
                    if v == '0':
                        if letter.islower():
                            self.characters[i].append(letter)
                    elif v == '1':
                        if letter.islower() or letter.isupper():
                            self.characters[i].append(letter)
                    elif v == '2':
                        if letter.islower() or letter.isupper() or letter.isalpha():
                            self.characters[i].append(letter)

    def class_probability(self, i, tweets): # example: compute P('eu') = count('eu) / count(all docs)
        count_doc_i = 0
        count_all_doc = len(tweets)
        prob_i = 0
        for t in range(len(self.characters)):
            if tweets[t].get_language() == i.value:
                count_doc_i = count_doc_i + 1
        prob_i = count_doc_i / count_all_doc
        return prob_i

    def cond_probability(self, i, j, tweets, letters, lang): # example: compute P('a'|eu) = count('a', eu) / sum(count('a', eu))
        count_j_i = 0
        sum_j_i = 0
        prob_j_i = 0
        for t in range(len(self.characters)):
            if tweets[t].get_language() == i.value: 
                count_j_i = count_j_i + self.characters[t].count(letters[j]) # Getting the number of characters in each languages class
                sum_j_i = sum_j_i + len(self.characters[t]) # Getting the sum of all characters in each language class
        prob_j_i = count_j_i / sum_j_i
        return prob_j_i
    
    def determite_vocabulary(self, v):
        char_size = 0
        letters = []

        if v == '0':
            char_size = len(self.low_letters)
            letters = self.low_letters.copy()
        elif v == '1' or v == '2':
            char_size = len(self.low_letters) + len(self.up_letters)
            letters = (self.low_letters + self.up_letters).copy() # Merge the two

        info = dict()
        info['char_size'] = char_size
        info['letters'] = letters
        return info

    def train(self, v, tweets):
        lang = language.Language
        info = self.determite_vocabulary(v)
        char_size = info.get("char_size")
        letters = info.get("letters")
        
        print("Training the model with vocabulary type V = " + v + " and " + str(len(tweets)) + " tweets...")
        for i in iter(lang): # For all classes i
            self.training_table_classes.append(self.class_probability(i, tweets))
            for j in range(char_size): # For all characters in vocabulary j
                self.training_table_chars.append(self.cond_probability(i, j, tweets, letters, lang))

    def test(self, v):
        info = self.determite_vocabulary(v)
        lang = language.Language
        char_size = info.get("char_size")
        score = 0
        maxScore = 0 # We get it with argmax in the end

        print("Testing the model...")
        for i in range(len(lang)): # For all classes i
            score = math.log10(self.training_table_classes[i])
            for j in range(char_size):
                score = score + math.log10(self.training_table_chars[j])
            self.scores.append(score)
        index = np.argmax(self.scores) # Gets the index of the maximum score
        print(self.scores)
                       
    def get_characters(self):
        return self.characters

    def get_score(self):
        return self.score

    