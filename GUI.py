
from typing    import Callable

from tkinter   import *

from Emergency import Emergency
from Grid      import Grid
from Agents    import *


# Colors
LIGHT_RED  = '#EE7E77'
LIGHT_BLUE = '#67B0CF'

# Constants
EMERGENCY_FREQUENCY = 2 * 1000 # 2 Seconds



class GUI:

    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------

    def __init__(self, grid: Grid, stepFunction: Callable, screenSize=600):
        self.grid = grid
        self.dispatcherPositions = []
        self.emergencyPositions  = []
        self.emergencyObjects    = []

        self.screenSize = screenSize
        self.window = Tk()
        self.window.title('Emergency Response System')
        self.canvas = Canvas(self.window, width=self.screenSize, height=self.screenSize)
        self.canvas.pack()

        self.stepFunction = stepFunction
        self.drawBoard()
        self.step()
        self.window.bind('<space>', self.step)


    def drawBoard(self):
        rows, columns = self.grid.size

        for i in range(rows):
            self.canvas.create_line(
                i * self.screenSize / rows,
                0,
                i * self.screenSize / rows,
                self.screenSize,
            )

        for i in range(columns):
            self.canvas.create_line(
                0,
                i * self.screenSize / columns,
                self.screenSize,
                i * self.screenSize / columns,
            )
    
    
    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def placeEmergency(self, emergency: Emergency):
        self.emergencyPositions.append(emergency.position)

        rows, columns = self.grid.size
        rowHeight = int(self.screenSize / rows)
        colWidth  = int(self.screenSize / columns)

        x1 = emergency.position[0] * rowHeight
        y1 = emergency.position[1] * colWidth
        x2 = x1 + rowHeight
        y2 = y1 + colWidth

        self.emergencyObjects.append(
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=LIGHT_RED)
        )


    def placeDispatcher(self, dispatcher: Agent):
        self.dispatcherPositions.append(dispatcher.position)

        rows, columns = self.grid.size
        rowHeight = int(self.screenSize / rows)
        colWidth  = int(self.screenSize / columns)

        x1 = dispatcher.position[0] * rowHeight
        y1 = dispatcher.position[1] * colWidth
        x2 = x1 + rowHeight
        y2 = y1 + colWidth

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=LIGHT_BLUE)
        self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=self.agentText(dispatcher.type))
        

    def agentText(self, agent: AgentType):
        # FIXME : substitute with Agent toString method -> def __str__(self):
        if (agent == AgentType.FIRE):
            return 'F' # Fire Station
        elif (agent == AgentType.MEDICAL):
            return 'H' # Hospital
        elif (agent == AgentType.POLICE):
            return 'P' # Police Station
        else:
            return '?' # Unknown

    
    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def step(self, key=None):
        self.stepFunction()
        self.updateBoard()
        

    def updateBoard(self):
        for emergency in self.grid.activeEmergencies:
            if emergency.position not in self.emergencyPositions:
                self.placeEmergency(emergency)
        for dispatcher in self.grid.getAllAgents():
            if dispatcher.position not in self.dispatcherPositions:
                self.placeDispatcher(dispatcher)
