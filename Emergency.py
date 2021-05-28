
from Agents import AgentType
import time


class Emergency:

    UNITSPERSEVERITY = 1

    def __init__(self, position, fire=False, medical=False, police=False, severityLevel=1):
        self.position = position
        self.severityLevel = severityLevel

        # needed units depends on severity level
        neededUnits = severityLevel * self.UNITSPERSEVERITY
        self.fire = neededUnits if fire else 0
        self.medical = neededUnits if medical else 0
        self.police = neededUnits if police else 0
        # needed to mark emergency as answered only when all units arrive
        self.totalRemainingUnits = self.fire + self.medical + self.police   

        # time limit calculated based on emergency characteristics
        self.stepsRemaining = 14 + ([fire, medical, police].count(True) * 4) - (2 * severityLevel)

        self.assigned = False  # if agents already assigned to help

        # metrics
        self.spawnTime = time.time()
        self.responseTime = None

    def getNeededUnits(self, agentType):
        if agentType == AgentType.FIRE:
            return self.fire
        elif agentType == AgentType.MEDICAL:
            return self.medical
        elif agentType == AgentType.POLICE:
            return self.police

    def isAssigned(self):
        return self.assigned

    def isAnswered(self):
        return self.totalRemainingUnits == 0

    def isExpired(self):
        return self.stepsRemaining <= 0

    def help(self, unit):
        if unit.type == AgentType.FIRE and self.fire > 0:
            self.fire -= 1
        elif unit.type == AgentType.MEDICAL and self.medical > 0:
            self.medical -= 1
        elif unit.type == AgentType.POLICE and self.police > 0:
            self.police -= 1

    def answer(self):
        self.totalRemainingUnits -= 1
        if (self.isAnswered()):
            self.responseTime = time.time() - self.spawnTime 

    def step(self):
        self.stepsRemaining -= 1

    def toString(self):
        return 'e'
