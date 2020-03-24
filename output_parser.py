import os


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
            file_name = "output/trace_myModel.txt" # May have to change that name later
        return file_name