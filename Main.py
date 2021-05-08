import random
from Grid import Grid
from Agents import *
from Emergency import Emergency

# main function - create grid and agents, function step to advance time

MAXUNITS = 1
MAXEMERGENCIES = 1
MAXAGENTS = 3

def generateAgents(numAgents, constructor):
    for _ in range(numAgents):
        position = grid.getFreePostition()
        numUnits = random.randint(1, MAXUNITS)
        agent = constructor(position, numUnits)
        grid.addDispatcher(agent)

def step():
    emergencies = random.randint(0, MAXEMERGENCIES)
    for _ in range(emergencies):
        position = grid.getFreePostition()
        t = random.randint(1, 3) # only simple ones for now
        emergency = Emergency(position, fire=(t==1), medical=(t==2), police=(t==3)) # default severity and time limit
        grid.addEmergency(emergency)
    # call agent decision for all agents

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



print('\nWelcome to our high tech multi agent Emergency Reponse System!')

print('\nWhat size do you want for the squared grid today?')
side = int( input('> length of side: ') )

print('\nAnd how many agents should I spawn? Max.', MAXAGENTS, 'agent total')
fireStations = int( input('> number of fire stations: ') )
hospitals = int( input('> number of hospitals: ') )
policeStations = int( input('> number of police stations: ') )
print()

numAgents = fireStations + hospitals + policeStations
assert numAgents > 0 and numAgents <= MAXAGENTS

grid = Grid(side, side)

generateAgents(fireStations, FireStation)
generateAgents(hospitals, Hospital)
generateAgents(policeStations, PoliceStation)

#guiInstance = GUI(grid)
#guiInstance.mainloop()

printGrid()
