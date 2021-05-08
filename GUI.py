
from tkinter import *
from Grid import Grid
from Emergency import Emergency
from os import environ
from random import randint

# Colors
LIGHT_RED  = '#EE7E77'
LIGHT_BLUE = '#67B0CF'

EMERGENCY_FREQUENCY = 2 * 1000 # 2 second

class GUI:

    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------

    def __init__(self, grid, screenSize=600):
        self.grid = grid
        self.emergencyObjects = []

        self.screenSize = screenSize
        self.window = Tk()
        self.window.title('Emergency Response System')
        self.canvas = Canvas(self.window, width=self.screenSize, height=self.screenSize)
        self.canvas.pack()

        self.initBoard()
        self.window.after(EMERGENCY_FREQUENCY, self.spawnEmergency)
    

    def initBoard(self):
        self.board = []
        rows, columns = self.grid.size

        for i in range(rows):
            for j in range(columns):
                self.board.append((i, j))

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

    
    def mainloop(self):
        while True:
            self.window.update()


    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def placeEmergency(self, emergency):
        # NOTE : See place_apple (https://github.com/aqeelanwar/Snake-And-Apple/blob/master/main.py)

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

    
    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def step(self):
        pass


    def spawnEmergency(self):
        rows, columns = self.grid.size
        position = (randint(0,rows-1), randint(0,columns-1))
        emergency = Emergency(position)
        self.placeEmergency(emergency)
                                
        self.window.after(EMERGENCY_FREQUENCY, self.spawnEmergency)




grid = Grid(10, 10)
gameInstance = GUI(grid)
gameInstance.mainloop()
