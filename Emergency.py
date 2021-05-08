
from Agents import AgentType

class Emergency:

    UNITSPERSEVERITY = 1

    def __init__(self, position, fire=False, medical=False, police=False, severityLevel=1, timeLimit=100):
        self.position = position
        self.severityLevel = severityLevel
        self.timeLimit = timeLimit

        # needed units depends on severity level
        neededUnits = severityLevel * self.UNITSPERSEVERITY
        self.fire = neededUnits if fire == True else 0
        self.medical = neededUnits if medical == True else 0
        self.police = neededUnits if police == True else 0

        self.assigned = False # if help is coming

        # IDEA: time limit calculated based on emergency characteristics, eg.:
        # (num of types * severity lvl * multiplicative factor * random factor)

        # TODO: determine number of resources needed (number of units of each type)

        # TODO: method of resolving an emergency
        #   - number of units needed vs received?
        #   - time it takes to resolve given number of units?
        #   - always a success?

    def isAnswered(self):
        return self.fire == 0 and self.medical == 0 and self.police == 0

    def help(self, unit):
        if (unit.type == AgentType.FIRE and self.fire > 0):
            self.fire -= 1
        elif (unit.type == AgentType.MEDICAL and self.medical > 0):
            self.medical -= 1
        elif (unit.type == AgentType.POLICE and self.police > 0):
            self.police -= 1
