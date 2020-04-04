import language
import math
import numpy as np
import string


class NaiveBayes:
    training_table_chars = []
    training_table_classes = []
    scores = []

    def __init__(self, v, d, tweets, corpus):  # Initialize by getting all characters
        self.train(v, d, tweets, corpus)

    def class_probability(self, i, tweets, characters):  # example: compute P('eu') = count('eu) / count(all docs)
        count_doc_i = 0
        count_all_doc = len(tweets)
        prob_i = 0
        for t in range(len(characters)):
            if tweets[t].get_language() == i.value:
                count_doc_i = count_doc_i + 1
        prob_i = count_doc_i / count_all_doc
        return prob_i

    def cond_probability(self, i, j, tweets, letters, characters, lang, d):  # example: compute P('a'|eu) = count('a', eu) / sum(count('a', eu))
        count_j_i = 0
        sum_j_i = 0
        prob_j_i = 0
        for t in range(len(characters)):
            if tweets[t].get_language() == i.value:
                count_j_i = count_j_i + characters[t].count(
                    letters[j])  # Getting the number of characters in each languages class
                sum_j_i = sum_j_i + len(characters[t])  # Getting the sum of all characters in each language class
        prob_j_i = (count_j_i + float(d)) / (sum_j_i + float(d) * len(letters))  # with smoothing d
        print(prob_j_i)
        return prob_j_i

    def train(self, v, d, tweets, corpus):
        lang = language.Language
        char_size = corpus.determite_vocabulary().get("char_size")
        letters = corpus.determite_vocabulary().get("letters")
        characters = corpus.get_characters()

        print("Training the model with vocabulary type V = " + v + " and " + str(len(tweets)) + " tweets...")
        for i in iter(lang):  # For all classes i
            self.training_table_classes.append(self.class_probability(i, tweets, characters))
            for j in range(char_size):  # For all characters in vocabulary j
                self.training_table_chars.append(self.cond_probability(i, j, tweets, letters, characters, lang, d))
        #print(self.training_table_chars)

    def test(self, v, tweets, corpus):
        lang = language.Language
        char_size = corpus.determite_vocabulary().get("char_size")
        letters = corpus.determite_vocabulary().get("letters")
        characters = corpus.get_characters()
        score = 0

        print("Testing the model...")
        languages = ['eu', 'ca', 'gl', 'es', 'en', 'pt']
        for i in range(len(characters)):
            sentence = ''.join(characters[i])  # Putting back into strings
            for j in range(len(languages)):
                if tweets[i].get_language() == languages[j]:
                    score = math.log10(self.training_table_classes[j])
                for k in range(char_size):
                    if letters[k] in sentence:
                        score = score + math.log10(self.training_table_chars[k])
                self.scores.append(score)
        #self.printScores(characters)

    def printScores(self, characters):
        languages = ['Basque', 'Catalan', 'Galican', 'Spanish', 'English', 'Portuguese']  # for better printing
        topIndex = 0

        newArray = np.reshape(self.scores, (len(characters), len(languages)))
        for i in range(len(characters)):
            print("\n")
            print('The scores for tweet #' + str(i + 1) + ' are...')
            for j in range(len(languages)):
                topIndex = np.argmax(newArray[i])
                print(languages[j] + ': ' + str(newArray[i][j]) + ", ")
            print("The most likely language for this tweet is " + languages[topIndex] + " with score: " + str(
                newArray[i][topIndex]) + ".")

    def get_score(self):
        return self.score

    def get_scores(self):
        return self.scores

    def init_dict(self, score_tweets):
        score_array = []
        for i in range(0, len(score_tweets), 6):
            score_dict = language.to_dict(0)
            for l in score_dict:
                score_dict[l] = score_tweets[i]
                i += 1
            score_array.append(score_dict)

        return score_array
