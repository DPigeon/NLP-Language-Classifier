class InputParser:
    vocabulary = 0 # Vocabulary to use (0, 1 or 2)
    n_gram_size = 0 # Size of n-grams (1, 2 or 3)
    smoothing_value = 0 # Smoothing value between 0 and 1
    training_file = "" # File used for training
    testing_file = "" # File used for testing

    # Tweets for training (id, username, language, post)
    tweet_training_ids = []
    tweet_training_usernames = []
    tweet_training_languages = []
    tweet_training_messages = []

    # Tweets for testing (id, username, language, post)
    tweet_testing_ids = []
    tweet_testing_usernames = []
    tweet_testing_languages = []
    tweet_testing_messages = []

    def __init__(self, file_path):
        with open(file_path) as file:
            for line in file:
                number = line.split()  # Becoming strings. We have to convert to integer
                # Storing into separate lists
                self.vocabulary = number[0]
                self.n_gram_size = number[1]
                self.smoothing_value = number[2]
                self.training_file = number[3]
                self.testing_file = number[4]
    
    def read_set_file(self, mode): # Two read modes: Mode 1: training, Mode 2: test
        if mode == "training":
            read_file = "input/" + self.training_file + ".txt"
            with open(read_file, encoding="utf8") as file:
                for line in file:
                    tweet = line.split("\t") # Each line is a tweet
                    self.tweet_training_ids.append(tweet[0])
                    self.tweet_training_usernames.append(tweet[1])
                    self.tweet_training_languages.append(tweet[2])
                    self.tweet_training_messages.append(tweet[3])
        else:
            read_file = "input/" + self.testing_file + ".txt"
            with open(read_file, encoding="utf8") as file:
                for line in file:
                    tweet = line.split("\t")
                    self.tweet_testing_ids.append(tweet[0])
                    self.tweet_testing_usernames.append(tweet[1])
                    self.tweet_testing_languages.append(tweet[2])
                    self.tweet_testing_messages.append(tweet[3])
    
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
        
    def get_tweet_training_ids(self):
        return self.tweet_training_ids

    def get_tweet_training_usernames(self):
        return self.tweet_training_usernames

    def get_tweet_training_languages(self):
        return self.tweet_training_languages

    def get_tweet_training_messages(self):
        return self.tweet_training_messages
    
    def get_tweet_testing_ids(self):
        return self.tweet_testing_ids

    def get_tweet_testing_usernames(self):
        return self.tweet_testing_usernames

    def get_tweet_testing_languages(self):
        return self.tweet_testing_languages

    def get_tweet_testing_messages(self):
        return self.tweet_testing_messages

