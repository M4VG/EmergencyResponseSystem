
from enum import Enum


class AgentType(Enum):
    FIRE = 1
    MEDICAL = 2
    POLICE = 3


# ------------------ General agent class ------------------ #

class Agent:

    def __init__(self, agentType, position, numberOfUnits):
        self.type = agentType
        self.position = position    # position on the grid
        self.units = [ResponseUnit(agentType, position) for i in range(numberOfUnits)]  # array of units
        self.assignedEmergencies = []       # new emergencies assigned to agent
        self.dispatchedEmergencies = []     # emergencies already responded to (sent units)

    def assignEmergency(self, emergency):
        self.assignedEmergencies.append(emergency)

    def findFreeUnits(self):
        units = []
        for unit in self.units:
            if unit.isFree():
                units.append(unit)
        return units

    # --------------- Actuators --------------- #

    def sendUnits(self, emergency, numberOfUnits):
        units = self.findFreeUnits()
        for i in range(numberOfUnits):
            units[i].setEmergency(emergency)
            emergency.help(units[i])    # decrement needed units

    def retrieveUnits(self, emergency):
        for unit in self.units:
            if unit.goalEmergency == emergency:
                unit.retrieve()

    # ------------ Main agent cycle ------------ #

    def step(self):

        for emergency in self.assignedEmergencies:
            # check for expired emergencies
            if emergency.isExpired():
                self.dispatchedEmergencies.remove(emergency)
                self.retrieveUnits(emergency)

        for emergency in self.dispatchedEmergencies:
            # check for answered emergencies
            if emergency.isAnswered():
                self.dispatchedEmergencies.remove(emergency)

            # check for expired emergencies
            if emergency.isExpired():
                self.dispatchedEmergencies.remove(emergency)
                self.retrieveUnits(emergency)

        # send available units to assigned emergencies
        numFreeUnits = len(self.findFreeUnits())
        while numFreeUnits > 0 and len(self.assignedEmergencies) > 0:
            emergency = self.assignedEmergencies[0]
            numNeededUnits = emergency.getNeededUnits(self.type)

            if numFreeUnits < numNeededUnits:
                self.sendUnits(emergency, numFreeUnits)
                numFreeUnits = 0
            else:
                self.sendUnits(emergency, numNeededUnits)
                numFreeUnits -= numNeededUnits
                self.assignedEmergencies.remove(emergency)
                self.dispatchedEmergencies.append(emergency)

        for unit in self.units:
            unit.step()


# ----------------- Specific agent classes ----------------- #

class FireStation(Agent):

    def __init__(self, position, numberOfUnits):
        Agent.__init__(self, AgentType.FIRE, position, numberOfUnits)


class Hospital(Agent):

    def __init__(self, position, numberOfUnits):
        Agent.__init__(self, AgentType.MEDICAL, position, numberOfUnits)


class PoliceStation(Agent):

    def __init__(self, position, numberOfUnits):
        Agent.__init__(self, AgentType.POLICE, position, numberOfUnits)


# ------------------ Response unit class ------------------ #

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

    def retrieve(self):
        self.goalEmergency = None

    def reachedEmergency(self):
        return self.goalEmergency is not None and self.currentPosition == self.goalEmergency.position

    def getGoalPosition(self):
        if self.goalEmergency is not None:
            return self.goalEmergency.position
        else:
            return self.homePosition

    # -------------- Mobility functions -------------- #

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
                self.goalEmergency.answer()
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
