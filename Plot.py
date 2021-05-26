
import csv
from pprint import pprint
import matplotlib.pyplot as plt

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

entry = { key: 0 for key in ['Answered', 'Expired', '%Expired', 'MRT', 'MRT1', 'MRT2', 'MRT3', 'MRT4'] }
averageData = { runKey: { totalKey : entry.copy() for totalKey in data[runKey]} for runKey in data }
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

