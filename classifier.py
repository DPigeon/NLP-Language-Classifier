import input_parser
import output_parser
import vocabulary
import n_gram
import tweet
import language

# The main file
inputPath = "input/input.txt"


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict."""
    z = language.to_dict(0)
    for f, b in zip(x.items(), y.items()):
        z[f[0]] = f[1] + b[1]
    return z


def main():
    the_input = input_parser.InputParser(inputPath)

    # Getting hyper-parameters
    v = the_input.get_vocabulary()
    n = the_input.get_n_gram_size()
    d = the_input.get_smoothing_value()
    training_file = the_input.get_training_file()
    testing_file = the_input.get_testing_file()

    # Creating the trace file
    output = output_parser.OutputParser()
    output.init_trace_file("normal", v, n, d) # For our first model with hyper-parameters

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
        training_tweets.append(
            tweet.Tweet(tweet_training_ids[i], tweet_training_usernames[i], tweet_training_languages[i],
                        tweet_training_messages[i]))

    # Creating the tweets with the testing set
    testing_tweets = []
    for i in range(len(tweet_testing_ids)):
        testing_tweets.append(tweet.Tweet(tweet_testing_ids[i], tweet_testing_usernames[i], tweet_testing_languages[i],
                                          tweet_testing_messages[i]))

    # Vocabulary
    vocab = vocabulary.Vocabulary(v, training_tweets)
    vocab.train(v, d, training_tweets)
    vocab.test(v, testing_tweets)
    vocab_scores = vocab.init_dict(vocab.get_scores())

    # Ngram
    ngram = n_gram.Ngram(n, testing_tweets, d)
    ngram.test_all(testing_tweets)
    ngram_scores = ngram.get_scores()

    # Summing the two models
    merged_score_array = []
    for i in range(len(ngram_scores)):
        merged_scores = merge_two_dicts(ngram_scores[i], vocab_scores[i])
        merged_score_array.append(merged_scores)  

    # Writing trace file
    print("Writing the trace file...")
    for i in range(len(testing_tweets)):
        dict_scores = merged_score_array[i]
        likelyClass = max(dict_scores, key=dict_scores.get).value
        maxScore = max(dict_scores.values())
        correctClass = testing_tweets[i].get_language()
        label = ""

        if likelyClass == correctClass:
            label = "correct"
        else:
            label = "wrong"

        output.create_trace_file("normal", v, n, d, testing_tweets[i].get_id(), likelyClass, maxScore, testing_tweets[i].get_language(), label)
    print("Completed the classification!")


main()
