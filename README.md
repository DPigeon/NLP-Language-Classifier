# NLP Language Classifier

https://github.com/DPigeon/NLP-Language-Classifier

A Naive Bayes classification for NLP to determine the most likely language of a tweet

First, install Miniconda with Python 3.7 at

```
https://docs.conda.io/en/latest/miniconda.html
```

You also need NumPy to run the project.

Install NumPy with

```
conda install numpy
```

## Run

To run the program, you must create an output folder in the root of the project. Then, you must edit the input.txt file in input folder.
The input file text is made as follow:

```
vocabulary size_of_ngram smoothing_value training_file testing_file
```

Where the vocabulary is either

```
0
Fold the corpus to lowercase and use only the 26 letters of the alphabet [a-z]
```

```
1
Distinguish up and low cases and use only the 26 letters of the alphabet [a-z, A-Z]
```

```
2
Distinguish up and low cases and use all characters accepted by the built-in isalpha() method
```

Where the size of ngram is either

```
1
character unigrams
```

```
2
character bigrams
```

```
3
character trigrams
```

Smoothing value is a smoothing between [0, 1].

## Output Files

The trace file will give an output as follows:

```
tweet_id  most_likely_class  score_most_likely_class  correct_class  correct_wrong_label
```

Where the correct and wrong label.

The evaluation file will give an output as follows:

```
accuracy
eu_precision  ca_precision  gl_precision  es_precision  en_precision  pt_precision
eu_recal  ca_recall  gl_recall  es_recall  en_recall  pt_recall
eu_f1_measure  ca_f1_measure  gl_f1_measure  es_f1_measure  en_f1_measure  pt_f1_measure
macro_f1  weighted_average_f1
```
