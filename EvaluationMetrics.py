
class EvaluationMetrics:

    def __init__(self, grid):
        self.totalEmergencies = len(grid.answeredEmergencies) + len(grid.expiredEmergencies)
        self.answeredEmergencies = len(grid.answeredEmergencies)
        self.expiredEmergencies = len(grid.expiredEmergencies)

        self.MRT = 0
        self.MRTperSeverity = ()
        self.percentageExpiredEmergencies = 0
        self.fireEffort = []
        self.hospitalsEffort = []
        self.policeEffort = []

    def evaluateGrid(self, grid):
        self.calculateMRT(grid)
        self.calculateMRTperSeverity(grid)
        self.calculateExpiredEmergencies(grid)
        self.calculateDistributionOfEffort(grid)
        self.printMetrics()

    def calculateMRT(self, grid):
        total = 0
        for e in grid.answeredEmergencies:
            total += e.responseTime #FIXME what to do with active and expired?
        if len(grid.answeredEmergencies) != 0:
            self.MRT = round( total / len(grid.answeredEmergencies), 2)

    def calculateMRTperSeverity(self, grid):
        totalTime = [0,0,0,0]
        count = [0,0,0,0]
        MRTperSeverity = []
        for e in grid.answeredEmergencies:
            totalTime[e.severityLevel - 1] += e.responseTime
            count[e.severityLevel - 1] += 1
        for i in range(4):
            if count[i] == 0:
                MRTperSeverity.append(0)
                continue
            MRTperSeverity.append( round( totalTime[i] / count[i], 2) )
        self.MRTperSeverity = tuple(MRTperSeverity)
            

    def calculateExpiredEmergencies(self, grid):
        totalEmergencies = len(grid.expiredEmergencies) + len(grid.answeredEmergencies) #FIXME do active emergencies count?
        if totalEmergencies != 0:
            self.percentageExpiredEmergencies = round( len(grid.expiredEmergencies) / totalEmergencies * 100, 2 )

    def calculateDistributionOfEffort(self, grid):
        # fire
        total = 0
        for a in grid.fireStations:
            total += a.answeredEmergencies
        for a in grid.fireStations:
            if total == 0:
                self.fireEffort.append(0)
                continue
            self.fireEffort.append( round( a.answeredEmergencies / total * 100, 2) )            

        # medical
        total = 0
        for a in grid.hospitals:
            total += a.answeredEmergencies
        for a in grid.hospitals:
            if total == 0:
                self.hospitalsEffort.append(0)
                continue
            self.hospitalsEffort.append( round( a.answeredEmergencies / total * 100, 2) )

        # police
        total = 0
        for a in grid.policeStations:
            total += a.answeredEmergencies
        for a in grid.policeStations:
            if total == 0:
                self.policeEffort.append(0)
                continue
            self.policeEffort.append( round( a.answeredEmergencies / total * 100, 2) )
        

    def printMetrics(self):
        # General
        print("RESULTS")
        print(" Total Emergencies ..................... ", self.totalEmergencies)
        print(" Answered Emergencies .................. ", self.answeredEmergencies)
        print(" Expired Emergencies ................... ", self.expiredEmergencies)

        # Percentage expired emergencies
        print(" Percentage of Expired Emergencies ..... ", self.percentageExpiredEmergencies, "%")
        
        # MRT
        print(" Mean Response Time .................... ", self.MRT, "s")

        # MRT per severity
        print("  - MRT Severity lvl.1 ................... ", self.MRTperSeverity[0], "s")
        print("  - MRT Severity lvl.2 ................... ", self.MRTperSeverity[1], "s")
        print("  - MRT Severity lvl.3 ................... ", self.MRTperSeverity[2], "s")
        print("  - MRT Severity lvl.4 ................... ", self.MRTperSeverity[3], "s")

        # Distribution of effort
        print(" Distribution of Effort")
        print("  - Fire stations ....................... ", self.fireEffort, "%")
        print("  - Hospitals ........................... ", self.hospitalsEffort, "%")
        print("  - Police stations ..................... ", self.policeEffort, "%")
               
