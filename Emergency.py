
class Emergency:

    def __init__(self, position, fire=False, medical=False, police=False, severityLevel=1, timeLimit=100):
        self.position = position
        self.fire = fire
        self.medical = medical
        self.police = police
        self.severityLevel = severityLevel
        self.timeLimit = timeLimit

        # IDEA: time limit calculated based on emergency characteristics, eg.:
        # (num of types * severity lvl * multiplicative factor * random factor)

        # TODO: determine number of resources needed (number of units of each type)

        # TODO: method of resolving an emergency
        #   - number of units needed vs received?
        #   - time it takes to resolve given number of units?
        #   - always a success?
