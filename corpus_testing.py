import string

class Corpus:
    low_letters = list(string.ascii_lowercase)
    up_letters = list(string.ascii_uppercase)
    alpha_letters = dict()
    v = ''
    characters = []  # List of sentence of characters for training

    def __init__(self, v, tweets):
        self.v = v
        if v == '2':
            self.get_isalpha()
        self.construct_corpus(tweets)  # Training

    # 0: Fold the corpus to lowercase and use only the 26 letters of the alphabet [a-z]
    # 1: Distinguish up and low cases and use only the 26 letters of the alphabet [a-z, A-Z]
    # 2: Distinguish up and low cases and use all characters accepted by the built-in isalpha() method
    def construct_corpus(self, tweets):  # chars can be used for the training of testing
        for i in range(len(tweets)):
            self.characters.append([])
            for letter in tweets[i].get_message():
                if self.v == '0':
                    if letter.islower():
                        self.characters[i].append(letter)
                elif self.v == '1':
                    if letter.islower() or letter.isupper():
                        self.characters[i].append(letter)
                elif self.v == '2':
                    if self.check_isalpha(letter):
                        self.characters[i].append(letter)
        print(self.characters)

    def determite_vocabulary(self): # Used to get all the information needed in the corpus
        char_size = 0
        letters = []

        if self.v == '0':
            char_size = len(self.low_letters)
            letters = self.low_letters.copy()
        elif self.v == '1':
            char_size = len(self.low_letters) + len(self.up_letters)
            letters = (self.low_letters + self.up_letters).copy()  # Merge the two
        elif self.v == '2':
            list_isalpha = self.alpha_letters.values()
            char_size = len(list_isalpha)
            letters = (list(list_isalpha)).copy() # Merge the three

        info = dict()
        info['char_size'] = char_size
        info['letters'] = letters
        return info

    def get_isalpha(self):
        # unicode = 17 planes of 2**16 symbols
        for codepoint in range(17 * 2**16):
            ch = chr(codepoint)
            if ch.isalpha():
                self.alpha_letters[ch] = ch
    
    def check_isalpha(self, letter):
        if letter in self.alpha_letters:
            return True
        else:
            return False

    def get_characters(self):
        return self.characters