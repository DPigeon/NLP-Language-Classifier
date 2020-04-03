import string

class Corpus:
    low_letters = list(string.ascii_lowercase)
    up_letters = list(string.ascii_uppercase)
    alpha_letters = dict()
    v = ''

    def __init__(self, v, tweets):
        self.v = v
        self.construct_corpus(tweets, self.characters)  # Training

    def construct_corpus(self, tweets, chars):  # chars can be used for the training of testing
        for i in range(len(tweets)):
            chars.append([])
            for letter in tweets[i].get_message():
                if self.v == '0':
                    if letter.islower():
                        chars[i].append(letter)
                elif self.v == '1':
                    if letter.islower() or letter.isupper():
                        chars[i].append(letter)
                elif self.v == '2':
                    if letter.islower() or letter.isupper() or letter.isalpha():
                        chars[i].append(letter)

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
            char_size = len(self.low_letters + len(self.up_letters) + len(self.alpha_letters))
            letters = (self.low_letters + self.up_letters + self.alpha_letters).copy() # Merge the three

        info = dict()
        info['char_size'] = char_size
        info['letters'] = letters
        return info