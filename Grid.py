
from Agents import AgentType

class Grid:

    def __init__(self, rows, columns):

        # emergencies
        self.activeEmergencies = []
        self.answeredEmergencies = []
        self.expiredEmergencies = []

        # agents
        self.fireStations = []
        self.hospitals = []
        self.policeStations = []

        # grid 
        self.size = (rows, columns)


    def inBounds(self, position):
        return all(x < y for x, y in zip(self.size, position))


    def addEmergency(self, emergency):
        assert inBounds(emergency.position)
        self.activeEmergencies.add(emergency)
    
    
    def addDispatcher(self, dispatcher):
        assert inBounds(dispatcher.position)
        if (dispatcher.agentType == AgentType.FIRE):
            self.fireStations.add(dispatcher)
        elif (dispatcher.agentType == AgentType.MEDICAL):
            self.hospitals.add(dispatcher)
        elif (dispatcher.agentType == AgentType.POLICE):
            self.policeStations.add(dispatcher)
    


