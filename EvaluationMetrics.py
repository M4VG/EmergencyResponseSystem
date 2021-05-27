
import os
import csv

class EvaluationMetrics:

    STATS_FILE = 'statistics.csv'

    def __init__(self, grid):
        self.totalEmergencies = len(grid.answeredEmergencies) + len(grid.expiredEmergencies)
        self.answeredEmergencies = len(grid.answeredEmergencies)
        self.expiredEmergencies = len(grid.expiredEmergencies)

        self.percentageExpiredEmergencies = 0
        self.expiredPerSeverity = ()
        self.MRT = 0
        self.MRTperSeverity = ()
        self.fireEffort = []
        self.hospitalsEffort = []
        self.policeEffort = []
        self.agentUnits = []
        self.callsForHelp = []

    def evaluateGrid(self, grid):
        self.calculateExpiredEmergencies(grid)
        self.calculateExpiredEmergenciesPerSeverity(grid)
        self.calculateMRT(grid)
        self.calculateMRTperSeverity(grid)
        self.calculateDistributionOfEffort(grid)
        self.calculateCallsForHelp(grid)
        self.printMetrics()

    def calculateExpiredEmergencies(self, grid):
        totalEmergencies = len(grid.expiredEmergencies) + len(grid.answeredEmergencies)
        if totalEmergencies != 0:
            self.percentageExpiredEmergencies = round( len(grid.expiredEmergencies) / totalEmergencies * 100, 2 )

    def calculateExpiredEmergenciesPerSeverity(self, grid):
        totalEmergencies = [0,0,0,0]
        expiredEmergencies = [0,0,0,0]
        expiredPerSeverity = [0,0,0,0]
        for e in grid.answeredEmergencies:
            totalEmergencies[e.severityLevel - 1] += 1
        for e in grid.expiredEmergencies:
            totalEmergencies[e.severityLevel - 1] += 1
            expiredEmergencies[e.severityLevel - 1] += 1
        for i in range(4):
            if totalEmergencies[i] != 0:
                expiredPerSeverity[i] = round( expiredEmergencies[i] / totalEmergencies[i] * 100, 2)
        self.expiredPerSeverity = tuple(expiredPerSeverity)

    def calculateMRT(self, grid):
        total = 0
        for e in grid.answeredEmergencies:
            total += e.responseTime
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

    def calculateCallsForHelp(self, grid):
        for a in grid.getAllAgents():
            self.callsForHelp.append(a.helpCalls)

    def printMetrics(self):
        # General
        print("RESULTS")
        print(" Total Emergencies ..................... ", self.totalEmergencies)
        print(" Answered Emergencies .................. ", self.answeredEmergencies)
        print(" Expired Emergencies ................... ", self.expiredEmergencies)

        # Percentage expired emergencies
        print(" Percentage of Expired Emergencies ..... ", self.percentageExpiredEmergencies, "%")

        # Percentage expired emergencies per severity
        print("  - Expired Severity lvl.1 ............. ", self.expiredPerSeverity[0], "%")
        print("  - Expired Severity lvl.2 ............. ", self.expiredPerSeverity[1], "%")
        print("  - Expired Severity lvl.3 ............. ", self.expiredPerSeverity[2], "%")
        print("  - Expired Severity lvl.4 ............. ", self.expiredPerSeverity[3], "%")
        
        # MRT
        print(" Mean Response Time .................... ", self.MRT, "s")

        # MRT per severity
        print("  - MRT Severity lvl.1 ................. ", self.MRTperSeverity[0], "s")
        print("  - MRT Severity lvl.2 ................. ", self.MRTperSeverity[1], "s")
        print("  - MRT Severity lvl.3 ................. ", self.MRTperSeverity[2], "s")
        print("  - MRT Severity lvl.4 ................. ", self.MRTperSeverity[3], "s")

        # Distribution of effort
        print(" Distribution of Effort:")
        print("  - Fire stations ...................... ", self.fireEffort, "%")
        print("  - Hospitals .......................... ", self.hospitalsEffort, "%")
        print("  - Police stations .................... ", self.policeEffort, "%")

        # Calls for help
        print(" Calls for help per agent .............. ", self.callsForHelp)


    def saveStatistics(self, nruns):

        # if the statistics file doesnt exits
        if not os.path.exists(self.STATS_FILE) or os.stat(self.STATS_FILE).st_size == 0:

            # open the file in the write mode
            with open(self.STATS_FILE, 'w', newline='') as f:
                # create the csv writer
                writer = csv.writer(f)

                header = ['Total', 'Answered', 'Expired', '%Expired', 'MRT', 'MRT1', 'MRT2', 'MRT3', 'MRT4', '#Runs']

                # write the header to the csv file
                writer.writerow(header)
            
            # change access permissions
            os.chmod(self.STATS_FILE, 0o777)

        # open the file in the append mode
        with open(self.STATS_FILE, 'a', newline='') as f:
            # create the csv writer
            writer = csv.writer(f)

            row = [self.totalEmergencies, self.answeredEmergencies, self.expiredEmergencies, self.percentageExpiredEmergencies, self.MRT, self.MRTperSeverity[0], self.MRTperSeverity[1], self.MRTperSeverity[2], self.MRTperSeverity[3], nruns]

            # write a row to the csv file
            writer.writerow(row)
