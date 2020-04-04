import os
from dataclasses import dataclass

import language


@dataclass
class Trace:
    tweet_id: float
    supposed_class: language.Language
    score: float
    evaluated_class: language.Language
    trace_output: str


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict."""
    z = language.to_dict(0)
    for f, b in zip(x.items(), y.items()):
        z[f[0]] = f[1] + b[1]
    return z


def division(n, d):
    return n / d if d else 0


class EvaluationOutputFile:
    entries = []
    accuracy = 0
    precision_dict = {}
    recall_dict = {}
    true_positive_dict = language.to_dict(0)
    false_negative_dict = language.to_dict(0)
    false_positive_dict = language.to_dict(0)
    suppose_precision_dict = language.to_dict(0)
    f1_measure_dict = language.to_dict(0)
    weighted_values_dict = language.to_dict(0)

    def __init__(self, model, v, n, d):
        super().__init__()
        self.model = model
        self.v = v
        self.n = n
        self.d = d
        self.init_evaluation_file(model, v, n, d)

    def calculate_accuracy(self, number_of_wrong_label):

        if number_of_wrong_label != 0:
            self.accuracy = 1 - (number_of_wrong_label / len(self.entries))
        else:
            self.accuracy = 1

    # e.g. For each english tweet how many were evaluated as english tweet
    def calculate_precision(self):
        total_dict = merge_two_dicts(self.true_positive_dict, self.false_negative_dict)
        self.precision_dict = {x: division(float(self.true_positive_dict[x]), total_dict[x]) for x in total_dict}

    def calculate_recall(self):
        total_dict = merge_two_dicts(self.true_positive_dict, self.false_positive_dict)
        self.recall_dict = {x: division(float(self.true_positive_dict[x]), total_dict[x]) for x in total_dict}

    # 2PR/P+R
    def calculate_f1_measure(self):
        self.f1_measure_dict = {x: division(2 * self.recall_dict[x] * self.precision_dict[x], (self.recall_dict[x] + self.precision_dict[x]))
                                for x in self.precision_dict}
        return self.f1_measure_dict

    def calculate_macro_f1(self):
        return sum(self.f1_measure_dict.values()) / len(self.f1_measure_dict)

    def calculate_weighted_f1(self):
        calculated_weight = {x: self.f1_measure_dict[x] * self.weighted_values_dict[x] for x in self.f1_measure_dict}
        return sum(calculated_weight.values()) / sum(self.weighted_values_dict.values())

    # What proportion of the instances in the class of interest are labelled correctly?
    # e.g. How many english were actually english
    def add_tp_fn_fp(self, actual, suppose, is_correct):
        self.weighted_values_dict[actual] = self.true_positive_dict[suppose] + 1
        if is_correct == "correct":
            self.true_positive_dict[suppose] = self.true_positive_dict[suppose] + 1
        else:  # Then it's incorrect
            self.false_negative_dict[actual] = self.false_negative_dict[actual] + 1
            self.false_positive_dict[suppose] = self.false_positive_dict[suppose] + 1

    def read_affilated_trace_file(self):
        accuracy_count = 0

        if self.model == "normal":
            trace_file = "output/trace_" + self.v + "_" + self.n + "_" + self.d + ".txt"
        else:
            trace_file = "output/trace_myModel.txt"  # May have to change that name later

        with open(trace_file, mode='r', encoding='utf-8-sig') as file:
            for line in file:
                if line.strip():
                    output = line.split()

                    if output[4] == "wrong":
                        accuracy_count += 1

                    self.add_tp_fn_fp(language.Language(output[1]), language.Language(output[3]), output[4])
                    self.entries.append(
                        Trace(float(output[0]), language.Language(output[1]), float(output[2]),
                              language.Language(output[3]),
                              output[4]))

        self.calculate_accuracy(accuracy_count)
        self.calculate_recall()
        self.calculate_precision()

        return self.entries

    def init_evaluation_file(self, model, v, n, d):
        file_name = self.get_file_name()

        if os.path.exists(file_name):  # Delete it
            os.remove(file_name)
            file = open(file_name, "w")
            file.close()
        else:
            file = open(file_name, "w")
            file.close()

    def get_file_name(self):
        if self.model == "normal":
            file_name = "output/eval_" + self.v + "_" + self.n + "_" + self.d + ".txt"
        else:
            file_name = "output/trace_myModel.txt"  # May have to change that name later

        return file_name

    def create_evaluation_file(self):
        file_name = self.get_file_name()
        self.read_affilated_trace_file()
        if os.path.exists(file_name):
            message = str(self.accuracy) + "\n" + self.convert_lang_dict_to_str(
                self.precision_dict) + "\n" + self.convert_lang_dict_to_str(self.recall_dict) + "\n" + \
                      self.convert_lang_dict_to_str(self.calculate_f1_measure()) + "\n" + str(
                self.calculate_macro_f1()) + "  " + str(self.calculate_weighted_f1())
            file = open(file_name, "a")
            file.write(str(message))
            file.close()

    def convert_lang_dict_to_str(self, my_dict):
        message = ""
        for i in iter(my_dict):
            message += str(my_dict[i]) + " "
        return message


class OutputParser:

    def __init__(self):
        super().__init__()

    def init_trace_file(self, model, v, n, d):
        file_name = self.get_file_name(model, v, n, d)

        if os.path.exists(file_name):  # Delete it
            os.remove(file_name)
            file = open(file_name, "w")
            file.close()
        else:
            file = open(file_name, "w")
            file.close()

    def create_trace_file(self, model, v, n, d, tweetId, likelyClass, score, correctClass, label):
        file_name = self.get_file_name(model, v, n, d)

        if os.path.exists(file_name):
            parameters = tweetId + "  " + likelyClass + "  " + str(score) + "  " + correctClass + "  " + label + "\n"
            file = open(file_name, "a")
            file.write(parameters)
            file.close()

    def get_file_name(self, model, v, n, d):
        file_name = ""
        if model == "normal":
            file_name = "output/trace_" + v + "_" + n + "_" + d + ".txt"
        else:
            file_name = "output/trace_myModel.txt"  # May have to change that name later
        return file_name

    def create_evaluation_file(self, model, v, n, d):
        evaluation_file = EvaluationOutputFile(model, v, n, d)
        evaluation_file.create_evaluation_file()
