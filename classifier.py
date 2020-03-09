import input_parser

# The main file
inputPath = "input/input.txt"

def main():
    the_input = input_parser.InputParser(inputPath)

    v = the_input.get_vocabulary()
    n = the_input.get_n_gram_size()
    d = the_input.get_smoothing_value()
    training_file = the_input.get_training_file()
    testing_file = the_input.get_testing_file()

    print(v, n, d, training_file, testing_file)

main()
