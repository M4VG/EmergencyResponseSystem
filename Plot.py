
import csv
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import scipy.optimize as opt;

STATS_FILE = 'statistics.csv'


### 1. Store the samples into a compact data structure

with open(STATS_FILE, newline='') as f:

    csv_reader = csv.DictReader(f, delimiter=',')
    # header: Total,Answered,Expired,%Expired,MRT,MRT1,MRT2,MRT3,MRT4,#Runs

    data = dict()
    # {
    #   50_RUNS : {
    #       41_TOTAL : [rowData1, rowData2, ...],
    #       43_TOTAL : ...,
    #       ...
    #   },
    #   ...
    # }

    sample_size = 1
    for row in csv_reader:

        rowData = { key: row[key] for key in ['Answered', 'Expired', '%Expired', 'MRT', 'MRT1', 'MRT2', 'MRT3', 'MRT4'] }

        if row['#Runs'] in data:

            if row['Total'] in data[row['#Runs']]:
                data[row['#Runs']][row['Total']].append(rowData)

            else:
                data[row['#Runs']][row['Total']] = [rowData, ]

        else:
            data[row['#Runs']] = { row['Total'] : [rowData, ] }


        sample_size += 1

    print(f'Processed {sample_size} samples.')
    # pprint(data)


### 2. Average the samples for each Total, for each Run

entry = { key : 0 for key in ['Answered', 'Expired', '%Expired', 'MRT', 'MRT1', 'MRT2', 'MRT3', 'MRT4'] }
averageData = { runKey : { totalKey : entry.copy() for totalKey in data[runKey]} for runKey in data }
# pprint(averageData)

for run in data:

    for total in data[run]:

        nsamples = 0

        for sample in data[run][total]:

            for key in sample:
                averageData[run][total][key] += float(sample[key])

            nsamples += 1
        
        for key in averageData[run][total]:
            averageData[run][total][key] = averageData[run][total][key] / nsamples
        
pprint(averageData)


### 3. Plot the data

def getPoints(data, run, key):
    def sort(x, y):
        return zip(*sorted(zip(x,y)))
    run = str(run)
    x, y = [], []
    for total in data[run]:
        x.append(int(total))
        y.append(float(data[run][total][key]))
    return sort(x, y)


def smoothPlot(x, y, num=200, k=3):
    # create data
    x = np.array(x)
    y = np.array(y)

    # define x as 200 evenly spaced values between the min and max of original x 
    xnew = np.linspace(x.min(), x.max(), num) 

    # define spline
    spl = make_interp_spline(x, y, k=k)
    y_smooth = spl(xnew)

    # create smooth line chart 
    plt.plot(xnew, y_smooth)


def fitPlot(x, y):
    pass


# NOTE: Dont forget to fix the labels/title when changing the key
keyToPlot = '%Expired' 

x, y = getPoints(averageData, 50, keyToPlot)
# plt.plot(x, y, marker='o') # plot line with points
plt.plot(x, y, 'o')        # plot points
smoothPlot(x, y)           # plot smooth line
plt.xlabel('Ammount of Emergencies')
plt.ylabel('Percentage of Expired Emergencies')
plt.title('%Expired per #Emergencies')
plt.show()
