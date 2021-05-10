
from enum import Enum


class AgentType(Enum):
    FIRE = 1
    MEDICAL = 2
    POLICE = 3


class Agent:

    def __init__(self, agentType, position, numberOfUnits):
        self.type = agentType
        self.position = position    # position on the grid
        self.units = [ResponseUnit(agentType, position) for i in range(numberOfUnits)]  # array of units

    def findFreeUnits(self):
        units = []
        for unit in self.units:
            if unit.isFree():
                units.append(unit)
        return units

    def canHelp(self, emergency):
        neededUnits = emergency.getNeededUnits(self.type)
        units = self.findFreeUnits()
        if len(units) < neededUnits:
            return False    # not enough units available
        else:
            return True

    def sendUnits(self, emergency):
        neededUnits = emergency.getNeededUnits(self.type)
        units = self.findFreeUnits()
        if len(units) < neededUnits:
            return  # not enough units available
        for i in range(neededUnits):
            units[i].setEmergency(emergency)

    def step(self):    
        for unit in self.units:
            unit.step()
                

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
        self.currentPosition = homePosition
        self.homePosition = homePosition
        self.goalEmergency = None

    def isActive(self):
        return not self.isFree()

    def isFree(self):
        return self.currentPosition == self.homePosition and self.goalEmergency is None

    def setEmergency(self, emergency):
        assert self.goalEmergency is None
        self.goalEmergency = emergency

    def reachedEmergency(self):
        return self.goalEmergency is not None and self.currentPosition == self.goalEmergency.position

    def help(self):
        self.goalEmergency.help(self)

    def getGoalPosition(self):
        if self.goalEmergency is not None:
            return self.goalEmergency.position
        else:
            return self.homePosition

    # -------------- MOBILITY FUNCTIONS -------------- #

    def moveRight(self):
        self.currentPosition = (self.currentPosition[0] + 1, self.currentPosition[1])

    def moveLeft(self):
        self.currentPosition = (self.currentPosition[0] - 1, self.currentPosition[1])

    def moveUp(self):
        self.currentPosition = (self.currentPosition[0], self.currentPosition[1] + 1)
        
    def moveDown(self):
        self.currentPosition = (self.currentPosition[0], self.currentPosition[1] - 1)

    def step(self):
        if self.isActive():
            if self.reachedEmergency():
                self.help()
                self.goalEmergency = None
            
            else:
                goalPosition = self.getGoalPosition()
                distanceX = goalPosition[0] - self.currentPosition[0]
                distanceY = goalPosition[1] - self.currentPosition[1]
                
                if distanceX > 0:
                    self.moveRight()
                elif distanceX < 0:
                    self.moveLeft()
                elif distanceY > 0:
                    self.moveUp()
                elif distanceY < 0:
                    self.moveDown()
