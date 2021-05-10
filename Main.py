import random
from Grid import Grid
from Agents import *
from Emergency import Emergency
from GUI import GUI
import sys

# main function - create grid and agents, function step to advance time


def addAgent(agent):
    if grid.fullBoard():
        sys.exit('Board is full')

    grid.addDispatcher(agent)


def step():
    emergencies = 1 if random.random() < 0.3 else 0
    for _ in range(emergencies):
        position = grid.getFreePosition()
        if position is None:
            continue    # Board is full
        t = random.randint(1, 3) # only simple ones for now
        emergency = Emergency(position, fire=(t == 1), medical=(t == 2), police=(t == 3))   # default severity and time limit
        grid.addEmergency(emergency)
        print('New emergency: fire', emergency.fire, 'medical', emergency.medical, 'police', emergency.police)
    grid.step()
    printGrid()
    

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

# create grid and agents
grid = Grid(10, 10)
addAgent(FireStation((2, 3), 3))
addAgent(FireStation((7, 8), 5))
addAgent(Hospital((4, 1), 4))
addAgent(Hospital((3, 8), 3))
addAgent(PoliceStation((8, 4), 4))
addAgent(PoliceStation((1, 6), 4))

printGrid()
print('> Press space ingame to step')

# create GUI
guiInstance = GUI(grid, step)
guiInstance.window.mainloop()
