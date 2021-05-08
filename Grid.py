
from Agents import AgentType
import random

class Grid:

    def __init__(self, rows, columns):

        # grid 
        self.grid = [[False for y in range(columns)] for x in range(rows)] # true if occupied, false otherwise
        self.size = (rows, columns)

        # agents
        self.fireStations = []
        self.hospitals = []
        self.policeStations = []

        # emergencies
        self.activeEmergencies = []
        self.answeredEmergencies = []
        self.expiredEmergencies = []


    def positionInBounds(self, position):
        return all(x < y for x, y in zip(position, self.size))

    def positionFree(self, position):
        return not self.grid[position[0]][position[1]]

    def makeRandomPosition(self):
        return tuple(random.randint(0, x-1) for x in self.size)

    def getFreePostition(self):
        pos = self.makeRandomPosition()
        while (not self.positionFree(pos)):
            pos = self.makeRandomPosition()
        return pos

    def occupyPosition(self, position):
        assert self.positionInBounds(position)
        assert self.positionFree(position)
        self.grid[position[0]][position[1]] = True

    def addDispatcher(self, dispatcher):
        self.occupyPosition(dispatcher.position)
        if (dispatcher.type == AgentType.FIRE):
            self.fireStations.append(dispatcher)
        elif (dispatcher.type == AgentType.MEDICAL):
            self.hospitals.append(dispatcher)
        elif (dispatcher.type == AgentType.POLICE):
            self.policeStations.append(dispatcher)

    def addEmergency(self, emergency):
        self.occupyPosition(dispatcher.position)
        self.activeEmergencies.add(emergency)
    
