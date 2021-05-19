
from Grid import Grid
from Agents import *
from GUI import GUI
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
        # start timer
        start = time.time()

        # print("main cycle started")

        # if step % 2 == 0:
        grid.step()
            # printGrid()

        # print("grid updated")

        try:
            guiInstance.updateBoard()
            pass
        except TclError:
            break

        # print("board updated")

        step += 1
        delta = time.time() - start
        print(delta)
        print(step)
        if delta < 0.50:
            time.sleep(0.50 - delta)

    stopAgents()

    # close window
    try:
        guiInstance.window.destroy()
    except TclError:
        pass

    print("Simulation over.")


def startAgents():
    for thread in agentThreads:
        thread.start()
    for agent in agents:
        agent.startUnits()
        #pass


def stopAgents():
    for agent in agents:
        agent.stop()


def printGrid():
    print('\n====== GRID STATUS ======\n')
    for row in grid.grid:
        for element in row:
            print(int(element), ' ', end='')
        print()
    for fireStation in grid.fireStations:
        print('\nFire station at ', fireStation.position)
    for hospital in grid.hospitals:
        print('Hospital at ', hospital.position)
    for policeStation in grid.policeStations:
        print('Police station at ', policeStation.position)
    for emergency in grid.activeEmergencies:
        print('Emergency at ', emergency.position)
    print('\n=========================\n')


# --------------- Main program execution --------------- #

# create grid
grid = Grid(10, 10)
maxSteps = 50

# create agents
agents = [
    FireStation((2, 3), 3),
    FireStation((7, 8), 5),
    Hospital((4, 1), 4),
    Hospital((3, 8), 3),
    PoliceStation((8, 4), 4),
    PoliceStation((1, 6), 4)
]
agentThreads = []

# add agents to grid and create agent threads
for agent in agents:
    grid.addDispatcher(agent)
    agentThreads.append(Thread(target=agent.run))

# create GUI
guiInstance = GUI(grid)

# run simulation
run()
