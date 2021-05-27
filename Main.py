
from Grid import Grid
from Agents import *
from GUI import GUI
from EvaluationMetrics import EvaluationMetrics
from threading import Thread
import time
from tkinter import TclError
import sys

# main function - create grid and agents, function step to advance time


def run():

    step = 0
    startAgents()

    while step < maxSteps:
        try:
            print("STEP ", step)
            do_step()
            step += 1
        except TclError:
            break

    grid.stopEmergencies()

    print("Finished steps, will keep running until there are no more emergencies.\n")

    while len(grid.activeEmergencies) > 0:
        try:
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
    print(delta)
    if delta < 1:
        time.sleep(1 - delta)
    else:
        print("-------------------- DELTA TOO LONG ------------------------")
    print()


# --------------- Main program execution --------------- #

# create grid
grid = Grid(10, 10)
maxSteps = 50

# agent type
reactive = False
deliberative = False
deliberativeSocial = True
if [reactive, deliberative, deliberativeSocial].count(True) != 1:
    print("Agent type not correctly specified!\n")
    exit()

# create agents
NUMUNITS1 = 7
NUMUNITS2 = 7
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
allUnits = []
for agent in agents:
    allUnits += agent.units
# guiInstance = GUI(grid, allUnits)

# run simulation
run()

print()
if reactive: print("[REACTIVE AGENT]")
elif deliberative: print("[DELIBERATIVE AGENT WITHOUT COMMUNICATION]")
else: print("[DELIBERATIVE AGENT WITH COMMUNICATION]")
evaluationSystem = EvaluationMetrics(grid)
evaluationSystem.evaluateGrid(grid)
evaluationSystem.saveStatistics(maxSteps)
print()
