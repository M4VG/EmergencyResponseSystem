
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

        print("STEP ", step)
        # start timer
        start = time.time()

        # print("main cycle started")

        # if step % 2 == 0:
        grid.step()
        print(grid.toString())

        # print("grid updated")

        try:
            # guiInstance.updateBoard()
            pass
        except TclError:
            break

        # print("board updated")

        step += 1
        delta = time.time() - start
        print(delta)
        if delta < 1:
            time.sleep(1 - delta)
        else:
            print("-------------------- DELTA TOO LONG ------------------------")
        print()

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
    for agent in agents:
        agent.startUnits()


def stopAgents():
    for agent in agents:
        agent.stop()


# --------------- Main program execution --------------- #

# create grid
grid = Grid(10, 10)
maxSteps = 50

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

social = True
if social:
    # add references to each others
    agentCount = len(deliberativeAgents)
    for iCurrent in range(agentCount):
        for iAppend in range(agentCount):
            if iCurrent == iAppend: # skip itself
                continue
            deliberativeAgents[iCurrent].addAgent(deliberativeAgents[iAppend])

# agents = reactiveAgents
agents = deliberativeAgents
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
evaluationSystem = EvaluationMetrics(grid)
evaluationSystem.evaluateGrid(grid)
print()
