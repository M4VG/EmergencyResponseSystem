from typing import Callable

from tkinter import *

from Emergency import Emergency
from Grid import Grid
from Agents import *
import time

# Colors
BLACK = '#000000'
DARK_GREY = '#565656'
LIGHT_RED = '#EE7E77'
LIGHT_BLUE = '#67B0CF'


class GUI:

    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------

    def __init__(self, grid: Grid, units: list, screenSize=600):
        self.grid = grid
        self.units = units
        self.emergencyObjects = []
        self.unitObjects = []

        self.screenSize = screenSize
        self.window = Tk()
        self.window.title('Emergency Response System')
        self.canvas = Canvas(self.window, width=self.screenSize, height=self.screenSize)
        self.canvas.pack()
        self.window.resizable(False, False)

        self.drawBoard()
        self.updateBoard()

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

        self.drawDispatchers()

        for agent in self.grid.getAllAgents():
            for unit in agent.units:
                self.placeUnit(unit)

    def drawDispatchers(self):
        for dispatcher in self.grid.getAllAgents():
            self.placeDispatcher(dispatcher)

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def placeUnit(self, unit: ResponseUnit):
        rows, columns = self.grid.size
        rowHeight = int(self.screenSize / rows)
        colWidth = int(self.screenSize / columns)

        # Top-Left
        pos = unit.getCurrentPosition()
        x1 = pos[0] * rowHeight + rowHeight / 3
        y1 = pos[1] * colWidth + rowHeight / 3

        # Bottom-Right
        x2 = x1 + rowHeight - 2 * (rowHeight / 3)
        y2 = y1 + colWidth - 2 * (rowHeight / 3)

        self.unitObjects.append((
            self.canvas.create_rectangle(y1, x1, y2, x2, fill=DARK_GREY),
            self.canvas.create_text((y1 + y2) / 2, (x1 + x2) / 2, text=self.agentText(unit.type)),
        ))

    def agentText(self, agent):
        # FIXME : substitute with Agent toString method -> def __str__(self):
        if agent == AgentType.FIRE:
            return 'F'  # Fire Station
        elif agent == AgentType.MEDICAL:
            return 'H'  # Hospital
        elif agent == AgentType.POLICE:
            return 'P'  # Police Station
        else:
            return '?'  # Unknown

    def placeEmergency(self, emergency: Emergency):
        rows, columns = self.grid.size
        rowHeight = int(self.screenSize / rows)
        colWidth = int(self.screenSize / columns)

        # Top-Left
        x1 = emergency.position[0] * rowHeight
        y1 = emergency.position[1] * colWidth
        # Bottom-Right
        x2 = x1 + rowHeight
        y2 = y1 + colWidth

        self.emergencyObjects.append(
            self.canvas.create_rectangle(y1, x1, y2, x2, fill=LIGHT_RED)
        )

    def placeDispatcher(self, dispatcher: Agent):
        rows, columns = self.grid.size
        rowHeight = int(self.screenSize / rows)
        colWidth = int(self.screenSize / columns)

        # Top-Left
        x1 = dispatcher.position[0] * rowHeight
        y1 = dispatcher.position[1] * colWidth

        # Bottom-Right
        x2 = x1 + rowHeight
        y2 = y1 + colWidth

        self.canvas.create_rectangle(y1, x1, y2, x2, fill=LIGHT_BLUE)
        self.canvas.create_text((y1 + y2) / 2, (x1 + x2) / 2, text=self.agentText(dispatcher.type))

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def updateBoard(self):
        start = time.time()

        # Re-draw emergencies every step
        for emergency in self.emergencyObjects:
            self.canvas.delete(emergency)
        for emergency in self.grid.activeEmergencies:
            self.placeEmergency(emergency)

        end = time.time()
        delta1 = end - start
        print("d1:", delta1)

        # Re-draw units every step
        for unit in self.unitObjects:
            self.canvas.delete(unit[0])
            self.canvas.delete(unit[1])
        for unit in self.units:
            if unit.isActive():
                self.placeUnit(unit)

        # update window
        self.window.update()

        delta2 = time.time() - end
        print("d2:", delta2)
