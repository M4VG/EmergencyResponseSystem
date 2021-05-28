
import csv
import sys
import json
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


if len(sys.argv) != 2:
    print('Please indicate the name of the .csv file.')
    sys.exit(1) # error

if sys.argv[1].endswith('.csv'):
    csv_file = sys.argv[1]
else:
    csv_file = sys.argv[1] + '.csv'


### 1. Read the samples and Store the averages

with open(csv_file, newline='') as f:

    csv_reader = csv.DictReader(f, delimiter=',')
    # fieldnames: Steps,Total,Answered,Expired,ExpiredPercentage,Expired1Percentage,ExpiredPercentage,Expired3Percentage,Expired4Percentage,MRT,MRT1,MRT2,MRT3,MRT4,Help

    data = { key : 0 for key in csv_reader.fieldnames }
    csv_list = list(csv_reader)

    agentCount = len(json.loads(csv_list[0]['Help']))
    data['Help'] = np.zeros(agentCount)
    
    sample_size = 0
    for row in csv_list:
        for column in row:
            if column == 'Help':
                value = np.array(json.loads(row['Help']))
                data[column] = data[column] + value
            else:
                data[column] += float(row[column])

        sample_size += 1
    
    for key in data:
        data[key] = data[key] / sample_size

    print(f'Processed {sample_size} samples.')
    pprint(data)
    

### 2. Plot the data


