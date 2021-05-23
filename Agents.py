
from enum import Enum
import time
from threading import Thread, Lock


class AgentType(Enum):
    FIRE = 1
    MEDICAL = 2
    POLICE = 3


# ------------------ General agent class ------------------ #

class Agent:

    def __init__(self, agentType, position, numberOfUnits):

        self.type = agentType
        self.position = position    # position on the grid

        self.units = [ResponseUnit(agentType, position) for _ in range(numberOfUnits)]  # array of units
        self.unitThreads = [Thread(target=unit.run) for unit in self.units]

        self.assignedEmergencies = []           # new emergencies assigned to agent
        self.dispatchedEmergencies = []         # emergencies already responded to (sent units)
        self.assignedEmergenciesLock = Lock()   # concurrency lock

        self.halt = False

        self.answeredEmergencies = 0

    def startUnits(self):
        for thread in self.unitThreads:
            thread.start()

    def stop(self):
        self.halt = True
        for unit in self.units:
            unit.stop()

    def assignEmergency(self, emergency):
        with self.assignedEmergenciesLock:
            self.assignedEmergencies.append(emergency)

    def removeAssignedEmergency(self, emergency):
        with self.assignedEmergenciesLock:
            self.assignedEmergencies.remove(emergency)

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
            if unit.getGoalEmergency() == emergency:
                unit.retrieve()


# ------------------ Reactive agent class ------------------ #

class ReactiveAgent(Agent):

    def __init__(self, agentType, position, numberOfUnits):
        Agent.__init__(self, agentType, position, numberOfUnits)

    def run(self):
        # print("agent running")

        while not self.halt:

            with self.assignedEmergenciesLock:
                assignedEmergenciesCopy = self.assignedEmergencies

            for emergency in assignedEmergenciesCopy:
                # check for expired emergencies
                if emergency.isExpired():
                    self.removeAssignedEmergency(emergency)
                    self.retrieveUnits(emergency)

            for emergency in self.dispatchedEmergencies:
                # check for answered emergencies
                if emergency.isAnswered():
                    self.dispatchedEmergencies.remove(emergency)
                    self.answeredEmergencies += 1

                # check for expired emergencies
                elif emergency.isExpired():
                    self.dispatchedEmergencies.remove(emergency)
                    self.retrieveUnits(emergency)

            # send available units to assigned emergencies
            numFreeUnits = len(self.findFreeUnits())
            while numFreeUnits > 0 and len(assignedEmergenciesCopy) > 0:
                emergency = assignedEmergenciesCopy[0]
                numNeededUnits = emergency.getNeededUnits(self.type)

                if numFreeUnits < numNeededUnits:
                    self.sendUnits(emergency, numFreeUnits)
                    numFreeUnits = 0
                else:
                    self.sendUnits(emergency, numNeededUnits)
                    numFreeUnits -= numNeededUnits
                    with self.assignedEmergenciesLock:
                        self.assignedEmergencies.remove(emergency)
                    self.dispatchedEmergencies.append(emergency)


# ---------------- Deliberative agent class ---------------- #

class DeliberativeAgent(Agent):

    def __init__(self, agentType, position, numberOfUnits):
        Agent.__init__(self, agentType, position, numberOfUnits)

        self.desires = []
        self.intentions = []

    def brf(self):
        # beliefs revision function

        with self.assignedEmergenciesLock:
            assignedEmergenciesCopy = self.assignedEmergencies

        for emergency in assignedEmergenciesCopy:
            # check for expired emergencies
            if emergency.isExpired():
                self.removeAssignedEmergency(emergency)
                self.retrieveUnits(emergency)

        for emergency in self.dispatchedEmergencies:
            # check for answered emergencies
            if emergency.isAnswered():
                self.dispatchedEmergencies.remove(emergency)

            # check for expired emergencies
            elif emergency.isExpired():
                self.dispatchedEmergencies.remove(emergency)
                self.retrieveUnits(emergency)

    def options(self):
        # choose desires from beliefs and intentions
        pass

    def filter(self):
        # choose intentions from desires and current intentions
        pass

    def plan(self):
        # make a plan to achieve intentions
        pass

    def run(self):

        # Deliberative loop:
        #   1. update beliefs
        #       - what will the beliefs be? just the assigned emergencies?
        #   2. deliberate to decide intentions:
        #       - determine available options
        #       - filter
        #   3. means-end reasoning: plan
        #   4. execute plan (give plan to units - maybe included in 3?)

        while not self.halt:

            # 1. update beliefs
            self.brf()

            # 2. deliberate
            self.options()
            self.filter()

            # 3. means-end reasoning
            self.plan()


# ------------- Specific reactive agent classes ------------ #

class ReactiveFireStation(ReactiveAgent):

    def __init__(self, position, numberOfUnits):
        ReactiveAgent.__init__(self, AgentType.FIRE, position, numberOfUnits)
    
    def toString(self):
        return 'F'


class ReactiveHospital(ReactiveAgent):

    def __init__(self, position, numberOfUnits):
        ReactiveAgent.__init__(self, AgentType.MEDICAL, position, numberOfUnits)

    def toString(self):
        return 'H'

class ReactivePoliceStation(ReactiveAgent):

    def __init__(self, position, numberOfUnits):
        ReactiveAgent.__init__(self, AgentType.POLICE, position, numberOfUnits)

    def toString(self):
        return 'P'

# ----------- Specific deliberative agent classes ---------- #

class DeliberativeFireStation(DeliberativeAgent):

    def __init__(self, position, numberOfUnits):
        DeliberativeAgent.__init__(self, AgentType.FIRE, position, numberOfUnits)


class DeliberativeHospital(DeliberativeAgent):

    def __init__(self, position, numberOfUnits):
        DeliberativeAgent.__init__(self, AgentType.MEDICAL, position, numberOfUnits)


class DeliberativePoliceStation(DeliberativeAgent):

    def __init__(self, position, numberOfUnits):
        DeliberativeAgent.__init__(self, AgentType.POLICE, position, numberOfUnits)


# ------------------ Response unit class ------------------ #

class ResponseUnit:

    def __init__(self, unitType, homePosition):
        self.type = unitType
        self.currentPosition = homePosition
        self.homePosition = homePosition
        self.goalEmergency = None
        self.halt = False
        self.goalEmergencyLock = Lock()     # concurrency lock
        self.currentPositionLock = Lock()   # concurrency lock

    def stop(self):
        self.halt = True

    def isActive(self):
        return not self.isFree()

    def isFree(self):
        return self.getCurrentPosition() == self.homePosition and self.getGoalEmergency() is None

    def getCurrentPosition(self):
        with self.currentPositionLock:
            position = self.currentPosition
        return position

    def setCurrentPosition(self, newPosition):
        with self.currentPositionLock:
            self.currentPosition = newPosition

    def getGoalEmergency(self):
        with self.goalEmergencyLock:
            emergency = self.goalEmergency
        return emergency

    def setEmergency(self, emergency):
        with self.goalEmergencyLock:
            self.goalEmergency = emergency

    def retrieve(self):
        self.setEmergency(None)

    def reachedEmergency(self):
        return self.getGoalEmergency() is not None and self.getCurrentPosition() == self.getGoalEmergency().position

    def getGoalPosition(self):
        if self.getGoalEmergency() is not None:
            return self.getGoalEmergency().position
        else:
            return self.homePosition

    # -------------- Mobility functions -------------- #

    def moveRight(self):
        currentPosition = self.getCurrentPosition()
        self.setCurrentPosition((currentPosition[0] + 1, currentPosition[1]))

    def moveLeft(self):
        currentPosition = self.getCurrentPosition()
        self.setCurrentPosition((currentPosition[0] - 1, currentPosition[1]))

    def moveUp(self):
        currentPosition = self.getCurrentPosition()
        self.setCurrentPosition((currentPosition[0], currentPosition[1] + 1))
        
    def moveDown(self):
        currentPosition = self.getCurrentPosition()
        self.setCurrentPosition((currentPosition[0], currentPosition[1] - 1))

    def run(self):

        # print("unit running")

        while not self.halt:

            start = time.time()

            if self.isActive():

                if self.reachedEmergency():
                    self.getGoalEmergency().answer()
                    self.setEmergency(None)

                else:
                    goalPosition = self.getGoalPosition()
                    currentPosition = self.getCurrentPosition()
                    distanceX = goalPosition[0] - currentPosition[0]
                    distanceY = goalPosition[1] - currentPosition[1]

                    if distanceX > 0:
                        self.moveRight()
                    elif distanceX < 0:
                        self.moveLeft()
                    elif distanceY > 0:
                        self.moveUp()
                    elif distanceY < 0:
                        self.moveDown()

            delta = time.time() - start
            if delta > 1:
                print("DELTA UNIT TOO LONG")
            time.sleep(1 - delta)
