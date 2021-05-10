import random
from Grid import Grid
from Agents import *
from Emergency import Emergency
from GUI import GUI
import sys

# main function - create grid and agents, function step to advance time

MAXUNITS = 1
MAXEMERGENCIES = 1
MAXAGENTS = 3


'''
def generateAgents(numAgents, constructor):
    for _ in range(numAgents):
        position = grid.getFreePosition()
        if position is None:
            sys.exit('Board is full')
        numUnits = random.randint(1, MAXUNITS)
        agent = constructor(position, numUnits)
        grid.addDispatcher(agent)
        for unit in agent.units:
            grid.addUnit(unit)
'''


def addAgent(agent):
    if grid.fullBoard():
        sys.exit('Board is full')

    grid.addDispatcher(agent)


def step():
    emergencies = 1 if random.random() < 0.3 else 0 # random.randint(0, MAXEMERGENCIES)
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


'''
print('\nWelcome to our high tech multi agent Emergency Reponse System!')

print('\nWhat size do you want for the squared grid today?')
side = int( input('> length of side: ') )

print('\nAnd how many agents should I spawn? Max.', MAXAGENTS, 'agents total')
fireStations = int( input('> number of fire stations: ') )
hospitals = int( input('> number of hospitals: ') )
policeStations = int( input('> number of police stations: ') )
print()
'''

grid = Grid(10, 10)

fireStations = hospitals = policeStations = 2
numAgents = fireStations + hospitals + policeStations
# assert numAgents > 0 and numAgents <= MAXAGENTS

# generateAgents(fireStations, FireStation)
# generateAgents(hospitals, Hospital)
# generateAgents(policeStations, PoliceStation)

addAgent(FireStation((2, 3), 3))
addAgent(FireStation((7, 8), 5))
addAgent(Hospital((4, 1), 4))
addAgent(Hospital((3, 8), 3))
addAgent(PoliceStation((8, 4), 4))
addAgent(PoliceStation((1, 6), 4))

printGrid()
print('> Press space ingame to step')

guiInstance = GUI(grid, step)
guiInstance.window.mainloop()
