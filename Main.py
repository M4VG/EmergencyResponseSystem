
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
reactive = True
deliberative = False
deliberativeSocial = False
if int(reactive) + int(deliberative) + int(deliberativeSocial) != 1:
    print("Agent type not correctly specified!\n")
    exit()

# create agents
reactiveAgents = [
    ReactiveFireStation((2, 3), 6),
    ReactiveFireStation((7, 8), 6),
    ReactiveHospital((4, 1), 6),
    ReactiveHospital((3, 8), 6),
    ReactivePoliceStation((8, 4), 6),
    ReactivePoliceStation((1, 6), 6)
]
deliberativeAgents = [
    DeliberativeFireStation((2, 3), 6),
    DeliberativeFireStation((7, 8), 6),
    DeliberativeHospital((4, 1), 6),
    DeliberativeHospital((3, 8), 6),
    DeliberativePoliceStation((8, 4), 6),
    DeliberativePoliceStation((1, 6), 6)
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
