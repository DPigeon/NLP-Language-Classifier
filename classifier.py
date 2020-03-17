import input_parser

# The main file
inputPath = "input/input.txt"

def main():
    the_input = input_parser.InputParser(inputPath)

    # Getting hyper=parameters
    v = the_input.get_vocabulary()
    n = the_input.get_n_gram_size()
    d = the_input.get_smoothing_value()
    training_file = the_input.get_training_file()
    testing_file = the_input.get_testing_file()

    # Reading the training set
    the_input.read_set_file("training")

    tweet_ids = the_input.get_tweet_training_ids()
    tweet_usernames = the_input.get_tweet_training_usernames()
    tweet_languages = the_input.get_tweet_training_languages()
    tweet_messages = the_input.get_tweet_training_messages()

main()
