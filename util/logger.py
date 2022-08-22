import datetime
import os
from pathlib import Path

class Logger:
    def __init__(self, log_file=None, file_expiry=7):

        if log_file is None:
            # check if logs folder exists, if not, make it
            logspath = Path(os.path.dirname(os.path.abspath(__file__))).parent.__str__() + "/logs"
            if not os.path.exists(logspath):
                os.makedirs(logspath)
            self.log_file = logspath + "/victorbot_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".log"
            self.log_folder = logspath
            self.file_expiry = file_expiry
        else:
            self.log_file = log_file
        self.cleanup()

    def cleanup(self):
        self.log("Checking for old log files...")
        # get all files in the logs folder
        files = os.listdir(self.log_folder)
        # delete all files that are older than 1 day
        for file in files:
            filetime = datetime.datetime.strptime(file.split("_")[1].split(".")[0], "%Y-%m-%d-%H-%M-%S")
            if filetime.timestamp() < (datetime.datetime.now() - datetime.timedelta(days=self.file_expiry)).timestamp():
                os.remove(self.log_folder + "/" + file)
                self.log("Deleted " + file)

    def log(self, string):
        string = "["+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]: " + string
        with open(self.log_file, 'a') as f:
            f.write(string + '\n')
        print(string)