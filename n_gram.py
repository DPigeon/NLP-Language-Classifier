import math
import string
import language
import copy


class Ngram:

    def __init__(self, n, tweets, smoothing, v):
        self.smoothing = float(smoothing)
        self.n = int(n)
        self.scores = []
        self.v = v
        print("Training the data by calculating the frequencies of each characters")

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
            message = [x for x in list(message) if self.check_in_vocab(x)]

            for character_count in range(len(message) - gram + 1):  # Getting one character at a time
                token = message[character_count:character_count + gram]
                token = "".join(token)  # Lower casing everything
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
        gram_model_fetched = self.build_gram_frequency(tweets, n)

        # Given a character, what's the probability that this character is of a language
        gram_model = copy.deepcopy(gram_model_fetched)
        for entry in gram_model_fetched:
            for l in iter(language.Language):
                gram_model[entry][l] = (gram_model_fetched[entry][l] / sum(gram_model_fetched[entry].values()))

        return gram_model

    def calculate_score(self, current_score_dict, token):

        if token in self.model.keys():  # If exist
            score_token = self.model[token]
        else:
            score_token = language.to_dict(self.smoothing)

        score_to_add = {}
        # Adding the dicts together by key
        for k in current_score_dict:
            if score_token[k] != 0:
                score_to_add[k] = math.log10(score_token[k]) + current_score_dict[k]
            else:
                score_to_add[k] = score_token[k] + current_score_dict[k]

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
        message = [x for x in list(message) if self.check_in_vocab(x)]  # Ignore character not in vocabulary

        for character_count in range(len(message) - self.n + 1):  # Getting one character_count at a time
            token = message[character_count:character_count + self.n]
            token = "".join(token)
            score = self.calculate_score(score, token)

        return score

    def determine_language_result(self, score_dict):
        print(score_dict)
        return max(score_dict, key=lambda key: score_dict[key])  # Returns the highest key value

    def get_scores(self):
        return self.scores

    def check_in_vocab(self, letter):
        if self.v == '0' and letter.islower():
            return True

        if self.v == '1' and (letter.islower() or letter.isupper()):
            return True

        if self.v == '2' and (letter.islower() or letter.isupper() or letter.isalpha()):
            return True

        return False
