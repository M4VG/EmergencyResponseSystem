
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

    # logic inside loop: double the number of steps, grid steps only on even steps
    # so the GUI updates twice as fast as the grid evolves
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
agents = [
    ReactiveFireStation((2, 3), 3),
    ReactiveFireStation((7, 8), 5),
    ReactiveHospital((4, 1), 4),
    ReactiveHospital((3, 8), 3),
    ReactivePoliceStation((8, 4), 4),
    ReactivePoliceStation((1, 6), 4)
]
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