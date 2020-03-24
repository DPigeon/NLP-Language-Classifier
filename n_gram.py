import math
import string
import language
import tweet


class Ngram:

    def __init__(self, n, tweets, smoothing):
        self.smoothing = float(smoothing)
        self.n = int(n)
        self.scores = []
        self.vocabulary = self.build_gram_model(1, tweets)
        print("Training the data by calculating the frequencies of each words")

        if self.n == 1:
            print("Building unigram model...")
            self.model = self.build_gram_model(self.n, tweets)
        elif self.n == 2:
            print("Building bigram model...")
            self.model = self.build_gram_model(self.n, tweets)
        elif self.n == 3:
            print("Building trigram model...")
            self.model = self.build_gram_model(self.n, tweets)
        else:
            print("Can't build", n, "gram -> only supports uni (1), bi (2), tri (3) grams")

    # Build the gram frequency in order to build the model based on the corpus
    def build_gram_frequency(self, tweets, gram):
        gram_frequency = dict()

        for tweet in tweets:
            message = tweet.get_message().translate(
                str.maketrans('', '', string.punctuation))  # Removes all punctuation
            message = message.split()

            for word_count in range(len(message) - gram + 1):  # Getting one word at a time
                token = message[word_count:word_count + gram]
                token = " ".join(token).lower()  # Lower casing everything
                if token in gram_frequency.keys():
                    gram_frequency[token][language.Language(tweet.get_language())] = gram_frequency.get(
                        token).get(language.Language(tweet.get_language())) + 1
                else:
                    gram_frequency[token] = language.to_dict(self.smoothing)
                    gram_frequency[token][language.Language(tweet.get_language())] = gram_frequency.get(
                        token).get(language.Language(tweet.get_language())) + 1

        return gram_frequency

    """ Method that trains models based on the n provided to the gram """

    def build_gram_model(self, n, tweets):
        gram_model = self.build_gram_frequency(tweets, n)

        # Given a word, what's the probability that this word is
        for entry in gram_model:
            for l in iter(language.Language):
                gram_model[entry][l] = (gram_model[entry][l] / sum(gram_model[entry].values()))

        return gram_model

    def calculate_score(self, current_score_dict, token):

        if token in self.model.keys():  # If exist
            score_token = self.model[token]
        else:
            score_token = language.to_dict(self.smoothing)

        if sum(current_score_dict.values()) == 0:
            score_to_add = {k: math.log10(score_token[k]) for k in current_score_dict}  # If first time initialize
        else:
            score_to_add = {k: math.log10(score_token[k]) + (current_score_dict[k]) for k in
                            current_score_dict}  # Add two dict together by their log value

        return score_to_add

    def test_all(self, tweets):
        for element in tweets:
            self.scores.append(self.test(element))
        return self.scores

    # Method that takes in a tweet and outputs a score, from the score you can calculate which language is most
    # probable.
    def test(self, tweet):
        score = language.to_dict(0)  # initialize the score table

        message = tweet.get_message().translate(str.maketrans('', '', string.punctuation))  # Removes all punctuation
        message = message.split()
        message = [x.lower() for x in message if x.lower() in self.vocabulary]  # Ignore character not in vocabulary

        for word_count in range(len(message) - self.n + 1):  # Getting one word at a time
            token = message[word_count:word_count + self.n]
            token = " ".join(token)
            score = self.calculate_score(score, token)

        return score

    def determine_language_result(self, score_dict):
        print(score_dict)
        return max(score_dict, key=lambda key: score_dict[key])  # Returns the highest key value

    def get_scores(self):
        return self.scores
