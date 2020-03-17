

class InputParser:
    vocabulary = 0 # Vocabulary to use (0, 1 or 2)
    n_gram_size = 0 # Size of n-grams (1, 2 or 3)
    smoothing_value = 0 # Smoothing value between 0 and 1
    training_file = "" # File used for training
    testing_file = "" # File used for testing
    
    def __init__(self, file_path):
        with open(file_path) as file:
            for line in file:
                number = line.split() # Becoming strings. We have to convert to integer
				# Storing into separate lists
                self.vocabulary = number[0]
                self.n_gram_size = number[1]
                self.smoothing_value = number[2]
                self.training_file = number[3]
                self.testing_file = number[4]
    
    def get_vocabulary(self):
        return self.vocabulary
    
    def get_n_gram_size(self):
        return self.n_gram_size

    def get_smoothing_value(self):
        return self.smoothing_value

    def get_training_file(self):
        return self.training_file

    def get_testing_file(self):
        return self.testing_file