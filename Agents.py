
from enum import Enum


class AgentType(Enum):
    FIRE = 1
    MEDICAL = 2
    POLICE = 3


class Agent:

    def __init__(self, agentType, grid, position, numberOfUnits):
        self.grid = grid
        self.type = agentType
        self.position = position # position on the grid
        self.units = [ResponseUnit(agentType, position) for i in range(numberOfUnits)] # array of units

        self.grid.addDispatcher(self)


    def sendUnits(self, numberOfUnits, targetPosition):
        pass


class FireStation(Agent):

    def __init__(self, grid, position, numberOfUnits):
        Agent.__init__(self, AgentType.FIRE, grid, position, numberOfUnits)


class Hospital(Agent):

    def __init__(self, grid, position, numberOfUnits):
        Agent.__init__(self, AgentType.MEDICAL, grid, position, numberOfUnits)


class PoliceStation(Agent):

    def __init__(self, grid, position, numberOfUnits):
        Agent.__init__(self, AgentType.POLICE, grid, position, numberOfUnits)


class ResponseUnit:

    def __init__(self, unitType, homePosition):
        self.type = unitType
        self.homePosition = homePosition
        self.currentPosition = homePosition
