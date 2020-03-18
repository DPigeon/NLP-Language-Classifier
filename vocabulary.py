
class Vocabulary:
    characters = [] # List of sentence of characters

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

    def get_characters(self):
        return self.characters

    