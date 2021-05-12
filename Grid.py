
from Agents import AgentType
import random
import math


class Grid:

    def __init__(self, rows, columns):
        # grid 
        self.grid = [[False for _ in range(columns)] for _ in range(rows)]  # true if occupied, false otherwise
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
        return all(i >= 0 for i in position) and all(i < j for i, j in zip(position, self.size))

    def positionFree(self, position):
        return not self.grid[position[0]][position[1]]

    def getRandomPosition(self):
        return tuple(random.randint(0, i-1) for i in self.size)

    def fullBoard(self):
        return all([all(x) for x in self.grid])

    def getFreePosition(self):
        if self.fullBoard():
            return None
        pos = self.getRandomPosition()
        while not self.positionFree(pos):
            pos = self.getRandomPosition()
        return pos

    def occupyPosition(self, position):
        assert self.positionInBounds(position)
        assert self.positionFree(position)
        self.grid[position[0]][position[1]] = True

    def clearPosition(self, position):
        self.grid[position[0]][position[1]] = False

    def addDispatcher(self, dispatcher):
        self.occupyPosition(dispatcher.position)
        if dispatcher.type == AgentType.FIRE:
            self.fireStations.append(dispatcher)
        elif dispatcher.type == AgentType.MEDICAL:
            self.hospitals.append(dispatcher)
        elif dispatcher.type == AgentType.POLICE:
            self.policeStations.append(dispatcher)

    def findNearestAgents(self, emergency):
        nearestAgents = [None, None, None]

        # fire stations
        if emergency.getNeededUnits(AgentType.FIRE) > 0:
            minDistance = math.inf
            for agent in self.fireStations:
                distance = math.sqrt((agent.position[0] - emergency.position[0]) ** 2 +
                                     (agent.position[1] - emergency.position[1]) ** 2)
                if distance < minDistance:
                    minDistance = distance
                    nearestAgents[0] = agent

        # hospitals
        if emergency.getNeededUnits(AgentType.MEDICAL) > 0:
            minDistance = math.inf
            for agent in self.hospitals:
                distance = math.sqrt((agent.position[0] - emergency.position[0]) ** 2 +
                                     (agent.position[1] - emergency.position[1]) ** 2)
                if distance < minDistance:
                    minDistance = distance
                    nearestAgents[1] = agent

        # police stations
        if emergency.getNeededUnits(AgentType.POLICE) > 0:
            minDistance = math.inf
            for agent in self.policeStations:
                distance = math.sqrt((agent.position[0] - emergency.position[0]) ** 2 +
                                     (agent.position[1] - emergency.position[1]) ** 2)
                if distance < minDistance:
                    minDistance = distance
                    nearestAgents[2] = agent

        return nearestAgents

    def contactAgents(self, emergency):
        # assign emergency to nearest agent of each type
        nearestAgents = self.findNearestAgents(emergency)
        for agent in nearestAgents:
            if agent is not None:
                agent.assignEmergency(emergency)
        emergency.assigned = True

    def addEmergency(self, emergency):
        self.occupyPosition(emergency.position)
        self.activeEmergencies.append(emergency)
    
    def step(self):
        for emergency in self.activeEmergencies:
            # check for answered emergencies
            if emergency.isAnswered():
                self.activeEmergencies.remove(emergency)
                self.answeredEmergencies.append(emergency)
                self.clearPosition(emergency.position)

            # check for expired emergencies
            elif emergency.isExpired():
                self.activeEmergencies.remove(emergency)
                self.expiredEmergencies.append(emergency)
                self.clearPosition(emergency.position)

            # check for unassigned emergencies
            elif not emergency.isAssigned():
                self.contactAgents(emergency)
                emergency.step()

            # decrement remaining steps for already assigned emergencies
            else:
                emergency.step()

        # step agents
        for agent in self.getAllAgents():
            agent.step()
