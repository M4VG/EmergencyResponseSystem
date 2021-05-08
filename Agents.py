
from enum import Enum


class AgentType(Enum):
    FIRE = 1
    MEDICAL = 2
    POLICE = 3


class Agent:

    def __init__(self, agentType, position, numberOfUnits):
        self.type = agentType
        self.position = position # position on the grid
        self.units = [ResponseUnit(agentType, position) for i in range(numberOfUnits)] # array of units

    def sendUnits(self, numberOfUnits, targetPosition):
        pass


class FireStation(Agent):

    def __init__(self, position, numberOfUnits):
        Agent.__init__(self, AgentType.FIRE, position, numberOfUnits)


class Hospital(Agent):

    def __init__(self, position, numberOfUnits):
        Agent.__init__(self, AgentType.MEDICAL, position, numberOfUnits)


class PoliceStation(Agent):

    def __init__(self, position, numberOfUnits):
        Agent.__init__(self, AgentType.POLICE, position, numberOfUnits)


class ResponseUnit:

    def __init__(self, unitType, homePosition):
        self.type = unitType
        self.homePosition = homePosition
        self.currentPosition = homePosition
