
from Grid import Grid
from Agents import *
from GUI import GUI
from EvaluationMetrics import EvaluationMetrics
from threading import Thread
import time
from tkinter import TclError
import sys
import os
import platform

# main function - create grid and agents, function step to advance time

if platform.system() == 'Linux':
    clear = lambda: os.system('clear')
elif platform.system() == 'Windows':
    clear = lambda: os.system('cls')
else:
    clear = lambda: None

def run():

    step = 0
    startAgents()

    while step < maxSteps:
        try:
            #clear()
            print("STEP ", step)
            do_step()
            step += 1
        except TclError:
            break

    grid.stopEmergencies()

    print("Finished steps, will keep running until there are no more emergencies.\n")

    while len(grid.activeEmergencies) > 0:
        try:
            #clear()
            print("STEP ", step)
            do_step()
            step += 1
        except TclError:
            break        

    stopAgents()

    # close window
    try:
        # guiInstance.window.destroy()
        pass
    except TclError:
        pass

    #clear()
    print("Simulation over.")

def startAgents():
    for thread in agentThreads:
        thread.start()

def stopAgents():
    for agent in agents:
        agent.stop()

def do_step():
    # start timer
    start = time.time()
    grid.step()
    print(grid.toString())

    # guiInstance.updateBoard()

    # print("board updated")
    delta = time.time() - start
    # print(delta)
    if delta < 1:
        time.sleep(1 - delta)
    else:
        # print("-------------------- DELTA TOO LONG ------------------------")
        pass
    print()



# --------------- command-line arguments --------------- #

if len(sys.argv) not in (2, 3):
    print('Please indicate the type of the agent.')
    print('Please indicate the name of the csv file.')
    sys.exit(1) # error

reactive = False
deliberative = False
deliberativeSocial = False

if sys.argv[1].lower() == 'r':
    reactive = True
elif sys.argv[1].lower() == 'd':
    deliberative = True
elif sys.argv[1].lower() == 'dc':
    deliberativeSocial = True
else:
    print('Agent type not correctly specified.')
    sys.exit(1) # error

csv_file = None

# if a csv file was specified
if len(sys.argv) == 3:
    if sys.argv[2].endswith('.csv'):
        csv_file = sys.argv[2]
    else:
        csv_file = sys.argv[2] + '.csv'


# --------------- main program execution --------------- #

# create grid
grid = Grid(10, 10)
maxSteps = 10

# create agents
NUMUNITS1 = 8
NUMUNITS2 = 6
reactiveAgents = [
    ReactiveFireStation((2, 3), NUMUNITS1),
    ReactiveFireStation((7, 8), NUMUNITS2),
    ReactiveHospital((4, 1), NUMUNITS1),
    ReactiveHospital((3, 8), NUMUNITS2),
    ReactivePoliceStation((8, 4), NUMUNITS1),
    ReactivePoliceStation((1, 6), NUMUNITS2)
]
deliberativeAgents = [
    DeliberativeFireStation((2, 3), NUMUNITS1),
    DeliberativeFireStation((7, 8), NUMUNITS2),
    DeliberativeHospital((4, 1), NUMUNITS1),
    DeliberativeHospital((3, 8), NUMUNITS2),
    DeliberativePoliceStation((8, 4), NUMUNITS1),
    DeliberativePoliceStation((1, 6), NUMUNITS2)
]

if deliberativeSocial:
    # add references to each others
    agentCount = len(deliberativeAgents)
    for iCurrent in range(agentCount):
        for iAppend in range(agentCount):
            if iCurrent == iAppend:     # skip itself
                continue
            deliberativeAgents[iCurrent].addAgent(deliberativeAgents[iAppend])

agents = reactiveAgents if reactive else deliberativeAgents

agentThreads = []
# add agents to grid and create agent threads
for agent in agents:
    grid.addDispatcher(agent)
    agentThreads.append(Thread(target=agent.run))

# create GUI
# allUnits = []
# for agent in agents:
#     allUnits += agent.units
# guiInstance = GUI(grid, allUnits)

# run simulation
run()

print()
if reactive: print("[REACTIVE AGENT]")
elif deliberative: print("[DELIBERATIVE AGENT WITHOUT COMMUNICATION]")
else: print("[DELIBERATIVE AGENT WITH COMMUNICATION]")
evaluationSystem = EvaluationMetrics(grid)
evaluationSystem.evaluateGrid(grid)
if csv_file != None: evaluationSystem.saveStatistics(csv_file, maxSteps)
print()
