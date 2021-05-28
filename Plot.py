
import os
import csv
import sys
import json
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


# ----------------- calculate averages ----------------- #

def writeAverages(csv_file):

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
        

    ### 2. Write the averages to a new csv file

    csv_file = csv_file[:-4] + '_average.csv'

    with open(csv_file, 'w', newline='') as f:

        csv_writer = csv.writer(f)

        header = data.keys()
        row = data.values()
        
        csv_writer.writerow(header)
        csv_writer.writerow(row)


# --------------- main program execution --------------- #

### 0. Calculate and Store the averages, if not already done

try:
    if not os.path.exists('r_average.csv') or os.stat('r_average.csv').st_size == 0:
        writeAverages('r.csv')
    if not os.path.exists('d_average.csv') or os.stat('d_average.csv').st_size == 0:
        writeAverages('d.csv')
    if not os.path.exists('dc_average.csv') or os.stat('dc_average.csv').st_size == 0:
        writeAverages('dc.csv')
except:
    print('Files not found.')
    sys.exit(1) # error


### 1. Read the average values

def convertToFloat(dictionary):
    for key in dictionary:
        if key == 'Help':
            value = dictionary['Help']
            dictionary['Help'] = list( map(float, value.strip('][').split(' ')) )
        else:
            dictionary[key] = float(dictionary[key])
    return dictionary


with open('r_average.csv', newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',')
    csv_dict = list(csv_reader)[0]
    r = convertToFloat(csv_dict)
    headers_r = list(csv_dict.keys())
    values_r = list(csv_dict.values())

with open('d_average.csv', newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',')
    csv_dict = list(csv_reader)[0]
    d = convertToFloat(csv_dict)
    headers_d = list(csv_dict.keys())
    values_d = list(csv_dict.values())

with open('dc_average.csv', newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',')
    csv_dict = list(csv_reader)[0]
    dc = convertToFloat(csv_dict)
    headers_dc = list(csv_dict.keys())
    values_dc = list(csv_dict.values())

assert headers_r == headers_d == headers_dc

# pprint(headers_r)
# print('\n\n', 'Reactive', '\n')
# pprint(values_r)
# print('\n\n', 'Deliberative', '\n')
# pprint(values_d)
# print('\n\n', 'Social Deliberative', '\n')
# pprint(values_dc)


### 2. Plot the average values

def mrtPerSeverity(r, d, dc):
    data_r = [r['MRT1'], r['MRT2'], r['MRT3'], r['MRT4']]
    data_d = [d['MRT1'], d['MRT2'], d['MRT3'], d['MRT4']]
    data_dc = [dc['MRT1'], dc['MRT2'], dc['MRT3'], dc['MRT4']]

    x = np.arange(4)
    fig, ax = plt.subplots()

    ax.bar(x + 0.00, data_r, color='b', width=0.25)
    ax.bar(x + 0.25, data_d, color='g', width=0.25)
    ax.bar(x + 0.50, data_dc, color='r', width=0.25)
    ax.set_yticks(np.arange(0, 15, 2))
    ax.legend(labels=['Reactive', 'Deliberative', 'Social Deliberative'], bbox_to_anchor=(1, 1))
    plt.title('Mean Response Time (seconds) per Severity')
    plt.xticks(x + 0.25, ['Level 1', 'Level 2', 'Level 3', 'Level 4'])
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()


def expiredPerSeverity(r, d, dc):
    # Expired1Percentage
    data_r = [r['Expired1Percentage'], r['Expired2Percentage'], r['Expired3Percentage'], r['Expired4Percentage']]
    data_d = [d['Expired1Percentage'], d['Expired2Percentage'], d['Expired3Percentage'], d['Expired4Percentage']]
    data_dc = [dc['Expired1Percentage'], dc['Expired2Percentage'], dc['Expired3Percentage'], dc['Expired4Percentage']]

    x = np.arange(4)
    fig, ax = plt.subplots()

    ax.bar(x + 0.00, data_r, color='b', width=0.25)
    ax.bar(x + 0.25, data_d, color='g', width=0.25)
    ax.bar(x + 0.50, data_dc, color='r', width=0.25)
    ax.set_yticks(np.arange(0, 50, 5))
    ax.legend(labels=['Reactive', 'Deliberative', 'Social Deliberative'], bbox_to_anchor=(1, 1))
    plt.title('Percentage of Expired per Severity')
    plt.xticks(x + 0.25, ['Level 1', 'Level 2', 'Level 3', 'Level 4'])
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()


if len(sys.argv) != 2:
    print('Please indicate the type of plot.')
    sys.exit(1) # error

if sys.argv[1].lower() == 'mrt':
    mrtPerSeverity(r, d, dc)
elif sys.argv[1].lower() == 'exp':
    expiredPerSeverity(r, d, dc)
else:
    print('Plot type not correctly specified.')
    sys.exit(1) # error
