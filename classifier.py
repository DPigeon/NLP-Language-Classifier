import corpus_training
import corpus_testing
import input_parser
import output_parser
import naive_bayes
import n_gram
import tweet
import language

# The main file
inputPath = "input/input.txt"
model = 2 # if 1 --> Model 1, if 2 --> Model 2


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict."""
    z = language.to_dict(0)
    for f, b in zip(x.items(), y.items()):
        z[f[0]] = f[1] + b[1]
    return z

def generate_trace_file(v, n, d, output, tweets, scores, model_type):
    for i in range(len(tweets)):
        dict_scores = scores[i]
        likelyClass = max(dict_scores, key=dict_scores.get).value
        maxScore = max(dict_scores.values())
        correctClass = tweets[i].get_language()
        label = ""

        if likelyClass == correctClass:
            label = "correct"
        else:
            label = "wrong"
        output.create_trace_file(model_type, v, n, d, tweets[i].get_id(), likelyClass, maxScore, tweets[i].get_language(), label)


def main():
    the_input = input_parser.InputParser(inputPath)

    # Getting hyper-parameters
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
        training_tweets.append(
            tweet.Tweet(tweet_training_ids[i], tweet_training_usernames[i], tweet_training_languages[i],
                        tweet_training_messages[i]))

    # Creating the tweets with the testing set
    testing_tweets = []
    for i in range(len(tweet_testing_ids)):
        testing_tweets.append(tweet.Tweet(tweet_testing_ids[i], tweet_testing_usernames[i], tweet_testing_languages[i],
                                          tweet_testing_messages[i]))

    if model == 1:
        # Creating the trace file for Model 1
        output = output_parser.OutputParser()
        output.init_trace_file("normal", v, n, d)  # For our first model with hyper-parameters

        # MODEL 1
        ngram = n_gram.Ngram(n, training_tweets, d, v)
        ngram.test_all(testing_tweets)
        ngram_scores = ngram.get_scores()

        # Writing track file for model 1
        generate_trace_file(v, n, d, output, testing_tweets, ngram_scores, "normal")

        # Writing evaluation file for model 1
        output.create_evaluation_file("normal", v, n, d)
        print("Writing the evaluation file for Model 1...")

    if model == 2:
        # Creating the trace file for Model 2
        output = output_parser.OutputParser()
        output.init_trace_file("other", v, n, d)  # For our first model with hyper-parameters

        # MODEL 2
        corpus_training_info = corpus_training.Corpus(v, training_tweets)
        model_2 = naive_bayes.NaiveBayes(v, d, training_tweets, corpus_training_info)
        corpus_testing_info = corpus_testing.Corpus(v, testing_tweets)
        model_2.test(v, testing_tweets, corpus_testing_info)

        # Writing track file for model 2
        naive_scores = model_2.init_dict(model_2.get_scores())
        generate_trace_file(v, n, d, output, testing_tweets, naive_scores, "other")
        
        # Writing evaluation file for model 2
        output.create_evaluation_file("other", v, n, d)
        print("Writing the evaluation file for Model 2...")

    print("Completed both classification!")


main()
