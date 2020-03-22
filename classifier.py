import input_parser
import vocabulary
import n_gram
import tweet

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

    tweet_training_ids = the_input.get_tweet_training_ids()
    tweet_training_usernames = the_input.get_tweet_training_usernames()
    tweet_training_languages = the_input.get_tweet_training_languages()
    tweet_training_messages = the_input.get_tweet_training_messages()

    # Reading the testing set
    the_input.read_set_file("testing")

    tweet_testing_ids = the_input.get_tweet_testing_ids()
    tweet_testing_usernames = the_input.get_tweet_testing_usernames()
    tweet_testing_languages = the_input.get_tweet_testing_languages()
    tweet_testing_messages = the_input.get_tweet_testing_messages()

    # Creating the tweets with the training set
    training_tweets = []
    for i in range(len(tweet_training_ids)):
        training_tweets.append(tweet.Tweet(tweet_training_ids[i], tweet_training_usernames[i], tweet_training_languages[i], tweet_training_messages[i]))
    
    # Creating the tweets with the testing set
    testing_tweets = []
    for i in range(len(tweet_testing_ids)):
        testing_tweets.append(tweet.Tweet(tweet_testing_ids[i], tweet_testing_usernames[i], tweet_testing_languages[i], tweet_testing_messages[i]))

    # Vocabulary
    vocab = vocabulary.Vocabulary(v, training_tweets)
    vocab.train(v, d, training_tweets)
    vocab.test(v, testing_tweets)

    ngram = n_gram.Ngram(n, training_tweets, d)
    tweet1 = tweet.Tweet(0, 0, 'en', 'hello i\'m a dude and I want to know if it\'s ok yeeeeee')
    tweet2 = tweet.Tweet(0, 0, 'es', 'buenos dias, donde estas el cuarto de bano')
    ngram.test(tweet1)
    ngram.test(tweet2)

main()
