
from Agents import AgentType


class Emergency:

    UNITSPERSEVERITY = 1

    def __init__(self, position, fire=False, medical=False, police=False, severityLevel=1, stepLimit=10):
        self.position = position
        self.severityLevel = severityLevel
        self.stepsRemaining = stepLimit

        # needed units depends on severity level
        neededUnits = severityLevel * self.UNITSPERSEVERITY
        self.fire = neededUnits if fire else 0
        self.medical = neededUnits if medical else 0
        self.police = neededUnits if police else 0
        self.totalRemainingUnits = self.fire + self.medical + self.police   # needed to mark emergency as answered only
                                                                            # when all units arrive

        self.assigned = False  # if agents already assigned to help

        # IDEA: time limit calculated based on emergency characteristics, eg.:
        # (num of types * severity lvl * multiplicative factor * random factor)

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

    def step(self):
        self.stepsRemaining -= 1
