import numpy as np
import os

class spmean:
    def __init__(self, directory_str):
        self.names = []
        self.directory_str = directory_str
    # The dataMean() function will compute the mean of a set of data column between two dates.
    # Loops through every file within the datasets folder.
    # Main Goal: Calculate the mean within a dataset in txt format and optionally between two dates.
    def dataMean(self, *argarrs):
        directory = os.fsencode(self.directory_str)
        # If input of 4 args, should be two. If input of 5, 3.
        timePeriods = []
        # Create var with the name of file w/o extension. Then append it to the names array
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                namesAdd = filename.replace(".txt", "")
                self.names.append(namesAdd.capitalize())
        global count
        count = 1
        for arg in argarrs:
            if (count%2==0):
                print("not")
            else:
                argArrArr = []
                for file in os.listdir(directory):
                    filename = os.fsdecode(file)
                    if filename.endswith(".txt"):
                        # Open and remove double quotes from txt file.
                        with open(self.directory_str + filename, 'r+') as f:
                            text = f.read()
                            text = text.replace("\"", "")
                            f.seek(0)
                            f.write(text)
                            f.truncate()
                        # Load up data-set data into a num py n-d array.
                        data_file = np.loadtxt(self.directory_str + filename, dtype=str, delimiter=',')

                        def avgCalc(x, y):
                            avgArr = []
                            # For row in data files check if the date w/o slashes is within range of dates needed.
                            for i in range(len(data_file)):
                                if (np.char.replace(data_file[i, 0], "/", "").astype(np.float) > x and np.char.replace(
                                        data_file[i, 0], "/", "").astype(np.float) < y):
                                    # If true then add the date's data number into the array that stores these numbers.
                                    avgArr.append(data_file[i, 4])
                            # calulate average after converting array to the float type as opposed to str.
                            avg = np.mean(np.array(avgArr).astype(np.float), dtype=float)
                            # add average to array of averages in the array period.
                            return avg

                        argArrArr.append(avgCalc(np.char.replace(arg, "/", "").astype(np.float),
                                                 np.char.replace(argarrs[count], "/", "").astype(np.float)))


                    else:
                        continue
                timePeriods.append(argArrArr)
            count = count + 1
        return timePeriods