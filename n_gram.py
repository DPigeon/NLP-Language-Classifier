import math
import string
import language
import copy


def generate_isalpha():
    isalpha_list = list()
    for codepoint in range(17 * 2 ** 16):
        ch = chr(codepoint)
        if ch.isalpha():
            isalpha_list.append(ch)
    return isalpha_list


class Ngram:

    def __init__(self, n, tweets, smoothing, v):
        self.smoothing = float(smoothing)
        self.n = int(n)
        self.scores = []
        self.v = int(v)
        self.chosen_alphabet = {}
        self.total_tweets_per_language = language.to_dict(0)
        self.total_number_of_character = {}
        self.priors = {}

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

    # function optimized to run on gpu
    # @jit
    def generate_vocab(self, gram, v):
        vocab = {}

        chosen_alphabet = list()
        if v == 0:
            chosen_alphabet = list(string.ascii_lowercase)
        elif v == 1:
            chosen_alphabet = list(string.ascii_letters)
        elif v == 2:
            chosen_alphabet = generate_isalpha()
            if gram != 1:
                return vocab
        self.chosen_alphabet = dict.fromkeys(chosen_alphabet)
        if gram == 1:
            vocab = {k: dict.fromkeys(language.to_dict(self.smoothing), self.smoothing) for k in chosen_alphabet}
        elif gram == 2:
            merged_char = []
            for char in chosen_alphabet:
                for char2 in chosen_alphabet:
                    merged_char.append(char + char2)

            vocab = {k: dict.fromkeys(language.to_dict(self.smoothing), self.smoothing) for k in merged_char}
        elif gram == 3:
            merged_char = []
            for char in chosen_alphabet:
                for char2 in chosen_alphabet:
                    for char3 in chosen_alphabet:
                        merged_char.append(char + char2 + char3)
            vocab = {k: dict.fromkeys(language.to_dict(self.smoothing), self.smoothing) for k in merged_char}

        return vocab

        # Generates the possible vocab

    def build_priors(self):
        priors = copy.deepcopy(self.total_tweets_per_language)
        for entry in self.total_tweets_per_language:
            priors[entry] = (self.total_tweets_per_language[entry] / sum(self.total_tweets_per_language.values()))
        return priors

    # Build the gram frequency in order to build the model based on the corpus
    def build_gram_frequency(self, tweets, gram):
        gram_frequency = self.generate_vocab(gram, self.v)
        total_gram_frequency = language.to_dict(0)
        for tweet in tweets:
            message = tweet.get_message().translate(
                str.maketrans('', '', string.punctuation))  # Removes all punctuation
            if self.v == 2 and gram != 1:
                message = [x for x in list(message) if x.isalpha()]
            else:
                message = [x for x in list(message) if x in self.chosen_alphabet]
            self.total_tweets_per_language[language.Language(tweet.get_language())] += 1

            for character_count in range(len(message) - gram + 1):  # Getting one character at a time
                token = message[character_count:character_count + gram]
                token = "".join(token)  # Lower casing everything
                if token in gram_frequency.keys():
                    total_gram_frequency[language.Language(tweet.get_language())] += 1
                    gram_frequency[token][language.Language(tweet.get_language())] = gram_frequency.get(
                        token).get(language.Language(tweet.get_language())) + 1
                else:
                    gram_frequency[token] = language.to_dict(self.smoothing)
                    gram_frequency[token][language.Language(tweet.get_language())] = gram_frequency.get(
                        token).get(language.Language(tweet.get_language())) + 1
        self.total_number_of_character = {key: total_gram_frequency[key] + self.smoothing * len(gram_frequency) for key
                                          in
                                          total_gram_frequency.keys()}
        return gram_frequency

    """ Method that trains models based on the n provided to the gram """

    def build_gram_model(self, n, tweets):
        gram_model_fetched = self.build_gram_frequency(tweets, n)
        self.priors = self.build_priors()
        # Given a character, what's the probability that this character is of a language
        gram_model = copy.deepcopy(gram_model_fetched)
        for entry in gram_model_fetched:
            for l in iter(language.Language):
                gram_model[entry][l] = (gram_model_fetched[entry][l] / self.total_number_of_character[l])

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
        score = {k: math.log10(self.priors[k]) for k in self.priors}

        message = tweet.get_message().translate(str.maketrans('', '', string.punctuation))  # Removes all punctuation

        if self.v == 2 and self.n != 1:
            message = [x for x in list(message) if x.isalpha()]
        else:
            message = [x for x in list(message) if x in self.chosen_alphabet]

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
