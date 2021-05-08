
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

    
    def getAllAgents(self):
        return self.fireStations + self.hospitals + self.policeStations


    def positionInBounds(self, position):
        return all(x >= 0 for x in position) and all(x < y for x, y in zip(position, self.size))

    def positionFree(self, position):
        return not self.grid[position[0]][position[1]]

    def makeRandomPosition(self):
        return tuple(random.randint(0, x-1) for x in self.size)

    def getFreePosition(self): #FIXME when its full
        pos = self.makeRandomPosition()
        while (not self.positionFree(pos)):
            pos = self.makeRandomPosition()
        return pos

    def occupyPosition(self, position):
        assert self.positionInBounds(position)
        assert self.positionFree(position)
        self.grid[position[0]][position[1]] = True

    def clearPosition(self, position):
        self.grid[position[0]][position[1]] = False

    def addDispatcher(self, dispatcher):
        self.occupyPosition(dispatcher.position)
        if (dispatcher.type == AgentType.FIRE):
            self.fireStations.append(dispatcher)
        elif (dispatcher.type == AgentType.MEDICAL):
            self.hospitals.append(dispatcher)
        elif (dispatcher.type == AgentType.POLICE):
            self.policeStations.append(dispatcher)


    def findNearestAgent(self, emergency, agents): #FIXME nearest not first!
        for agent in agents:
            if agent.canHelp(emergency):
                return agent
        return None

    def contactAgents(self, emergency):
        fire = self.findNearestAgent(emergency, self.fireStations)
        hospital = self.findNearestAgent(emergency, self.hospitals)
        police = self.findNearestAgent(emergency, self.policeStations)
        if fire != None and hospital != None and police != None:
            fire.sendUnits(emergency)
            hospital.sendUnits(emergency)
            police.sendUnits(emergency)
            emergency.assigned = True

    def addEmergency(self, emergency):
        self.occupyPosition(emergency.position)
        self.activeEmergencies.append(emergency)
    
    def step(self):
        # step agents
        for fireStation in self.fireStations:
            fireStation.step()
        for hospital in self.hospitals:
            hospital.step()
        for policeStation in self.policeStations:
            policeStation.step()

        # check for answered emergencies
        for emergency in self.activeEmergencies:
            if emergency.isAnswered():
                self.activeEmergencies.remove(emergency)
                self.answeredEmergencies.append(emergency)
                self.clearPosition(emergency.position)

        # check for unassigned emergencies
        for emergency in self.activeEmergencies:
            if not emergency.assigned:
                self.contactAgents(emergency)

        # TODO check for expired emergencies
