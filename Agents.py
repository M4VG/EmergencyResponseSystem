
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

    def findFreeUnits(self):
        units = []
        for unit in self.units:
            if unit.isFree(): units.append(unit)
        return units

    def getNeededUnits(self, emergency):
        pass

    def canHelp(self, emergency):
        neededUnits = self.getNeededUnits(emergency)
        units = self.findFreeUnits()
        if len(units) < neededUnits:
            return False # not enough units available
        else:
            return True

    def sendUnits(self, emergency):
        neededUnits = self.getNeededUnits(emergency)
        units = self.findFreeUnits()
        if len(units) < neededUnits:
            return # not enough units available
        for i in range(neededUnits):
            units[i].setEmergency(emergency)

    def step(self):    
        for unit in self.units:
            unit.step()
                


class FireStation(Agent):

    def __init__(self, position, numberOfUnits):
        Agent.__init__(self, AgentType.FIRE, position, numberOfUnits)

    def getNeededUnits(self, emergency):
        return emergency.fire


class Hospital(Agent):

    def __init__(self, position, numberOfUnits):
        Agent.__init__(self, AgentType.MEDICAL, position, numberOfUnits)

    def getNeededUnits(self, emergency):
        return emergency.medical


class PoliceStation(Agent):

    def __init__(self, position, numberOfUnits):
        Agent.__init__(self, AgentType.POLICE, position, numberOfUnits)

    def getNeededUnits(self, emergency):
        return emergency.police


class ResponseUnit:

    def __init__(self, unitType, homePosition):
        self.type = unitType
        self.currentPosition = homePosition
        self.homePosition = homePosition
        self.goalEmergency = None

    def isActive(self):
        return not self.isFree()

    def isFree(self):
        return self.currentPosition == self.homePosition and self.goalEmergency == None

    def setEmergency(self, emergency):
        assert self.goalEmergency == None
        self.goalEmergency = emergency

    def reachedEmergency(self):
        return self.goalEmergency != None and self.currentPosition == self.goalEmergency.position

    def moveRight(self):
        self.currentPosition = (self.currentPosition[0] + 1, self.currentPosition[1])

    def moveLeft(self):
        self.currentPosition = (self.currentPosition[0] - 1, self.currentPosition[1])

    def moveUp(self):
        self.currentPosition = (self.currentPosition[0], self.currentPosition[1] + 1)
        
    def moveDown(self):
        self.currentPosition = (self.currentPosition[0], self.currentPosition[1] - 1)

    def getGoalPosition(self):
        if self.goalEmergency != None:
            return self.goalEmergency.position
        else:
            return self.homePosition

    def step(self):
        if self.isActive():
            if self.reachedEmergency():
                self.goalEmergency.help(self)
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

            
