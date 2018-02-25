######################################################################################
#                                                                                    #
# TIM ANDREWS / 2017-02-26        (test from new pc                                  #   
# An implementation of Conway's Game of Life.                                        #   
# For rules of the game, see https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life   #
# This application provides a tkinter user interface to simulate cellular automation.#
# A vector is stored to reprsent a life-or-death property for each cell.             #
# The vector is then translated into rows and columns which are printed on a canvas. #
# Included options are simulation speed, and number of cells.                        #
#                                                                                    #   
######################################################################################


#imports
from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import *
from random import randint
from time import *

_RESET = False
_ALIVE = 'white'
_DEAD = 'black'
_GRID = [_DEAD]

#Event handler for start button / recursive function to continue calculating the life and death process
def start(*args):
    global _RESET
    global _GRID
    global _GENERATION
    if(_RESET):
        _GRID = [_DEAD]*int(_ROWS.get())*int(_COLUMNS.get())
        generateStartingGrid(_GRID)
        _GENERATION.set(0)
        _RESET = False
    start_button.config(state='disabled')
    calculateGrid(int(_ROWS.get()), int(_COLUMNS.get()), _GRID)
    _GENERATION.set(int(_GENERATION.get()) + 1)
    printGrid()
    root.simulation = root.after(201 - int(float(_SPEED.get())), start)

#Event handler for stop button
def stop(*args):
    global _RESET
    global _GENERATION
    if (root.simulation is not None):
        root.after_cancel(root.simulation)
        root.simulation = None
        _RESET = True
    start_button.config(state='normal')
    
#Event handler to choose an alive color
def chooseForeColor(*args):
    global _ALIVE
    color = askcolor(_ALIVE)
    _ALIVE = color[1]

#Event handler to choose a dead color
def chooseBackColor(*args):
    global _DEAD
    color = askcolor(_DEAD)
    _DEAD = color[1]


#print the grid to the screen
def printGrid(*args):
    global _CAN
    global _RENDERING
    global _GRID
    global _ROWS
    global _COLUMNS
    val = 0
    tempString = ""
    _CAN.delete("all")
    for row in range(0,int(_ROWS.get())-0):
        for column in range(0,int(_COLUMNS.get())-0):
            _CAN.create_rectangle(column * 5, row * 5, (column * 5) + 5, (row * 5) + 5, fill=_GRID[val])
            val += 1
 
  
#Fill each space in the grid randomly with either a DEAD or a ALIVE
#DEAD is a black by deault, and ALIVE is white by default.  ALIVE # will represent live cells
#We will initially seed 1/8 of the cells with live cells  
def generateStartingGrid(gr):
    for i in range(0, len(gr) - 1):
        if(randint(0,1000) <= 125): 
            gr[i] = _ALIVE
        else:
            gr[i] = _DEAD


#Given a cell, determine how many neighbors are alive.  
#Neighbors can be one of eight directions from the given cell:
#North, south, east, west, northwest, northeast, southwest, southeast
def getLiveNeighborCount(rows, columns, grid, cellIndex):
    liveNeighbors = 0
    
    #Does this cell have a living west neighbor?
    if(cellIndex % columns != 0 and  grid[cellIndex - 1] == _ALIVE):
        liveNeighbors += 1
    
    
    #Does this cell have a living east neighbor?
    if(cellIndex % columns != (columns - 1) and  grid[cellIndex + 1] == _ALIVE):
        liveNeighbors += 1
    
    
    #Does this cell have a living south neighbor?
    #print(len(grid))
    if(cellIndex < ((rows * columns) - columns) and grid[cellIndex + columns] == _ALIVE):
        liveNeighbors += 1
    
    #Does this cell have a living southwest neighbor?
    if(cellIndex < ((rows * columns) - columns) and cellIndex % columns != 0 and grid[cellIndex + columns - 1] == _ALIVE):
        liveNeighbors += 1
    
    
    #Does this cell have a living southeast neighbor?
    if(cellIndex < ((rows * columns) - columns - 1) and cellIndex % columns != (columns - 1) and grid[cellIndex + columns + 1] == _ALIVE):
        liveNeighbors += 1
    
    
    #Does this cell have a living north neighbor?
    if(cellIndex >= columns and grid[cellIndex - columns] == _ALIVE):
        liveNeighbors += 1
    
    
    #Does this cell have a living northwest neighbor?
    if(cellIndex >= columns + 1 and cellIndex % columns != 0 and grid[cellIndex - columns - 1] == _ALIVE):
        liveNeighbors += 1
    
    
    #Does this cell have a living northeast neighbor?
    if(cellIndex >= columns and cellIndex % columns != (columns - 1) and grid[cellIndex - columns + 1] == _ALIVE):
        liveNeighbors += 1  
    
    
    return liveNeighbors



#For each living cell - ALIVE # sign - we will determine
#If it will remain living.  We will also determine if each
#dead cell will come to life.
def calculateGrid(rows, columns, grid):
    i = 0
    tempGrid = [None]*rows*columns #Temporary grid to store the results if each cell is going to live or die
    tempGrid[:] = grid[:]
    
    for i in range(0, len(grid)):
        neighborCount = getLiveNeighborCount(rows, columns, grid, i)
        #Cell is alive
        if(grid[i] == _ALIVE):
            if(neighborCount < 2 or neighborCount > 3):
                tempGrid[i] = _DEAD
        #Cell is dead
        else:
            if(neighborCount == 3):
                tempGrid[i] = _ALIVE           
    
    grid[:] = tempGrid[:]
    tempGrid = None


        
####USER INTERFACE
root = Tk()
root.title("Conway's Game of Life in Python")


mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#Add a new frame to have the header controls
headerframe = ttk.Frame(mainframe, padding = "3 3 3 3", width=300, height=60)
headerframe.grid(column=0, row=0, sticky=(N, W, E, S))

#Add a new frame to house the grid
gridframe = ttk.Frame(mainframe, padding = "3 3 3 3", width=300, height=300)
gridframe.grid(column=0, row=1, sticky = (N, W, E, S))

#canvas for the grid
_CAN = Canvas(gridframe, height=700, width=900)
_CAN.pack()
_RENDERING = PhotoImage(height=700, width=900)

#Data entry for rows and columns
_ROWS = StringVar(value=120)
_COLUMNS = StringVar(value=120)
_SPEED = StringVar(value = 100)
_GENERATION= IntVar(value = 0)

#Row and column count
ttk.Label(headerframe, text="Columns").grid(column=1, row=1, sticky=E)
column_entry = ttk.Entry(headerframe, width=7, textvariable=_COLUMNS)
column_entry.grid(column=2, row=1, sticky=(W))
ttk.Label(headerframe, text="Rows").grid(column=3, row=1, sticky=E)
row_entry = ttk.Entry(headerframe, width=7, textvariable=_ROWS)
row_entry.grid(column=4, row=1, sticky=(W))


#Speed
ttk.Label(headerframe, text="").grid(column=1, row=2, sticky=E)
ttk.Label(headerframe, text="Speed").grid(column=1, row=3, sticky=E)
speed_scale = ttk.Scale(headerframe,  from_=1, to=200, variable=_SPEED).grid( column=2, row=3)

#Start button
ttk.Label(headerframe, text="").grid(column=1, row=4, sticky=E)
start_button = ttk.Button(headerframe, text="Start", command=start)
start_button.grid(column=1, row=5, sticky=W)

#Stop button
ttk.Label(headerframe, text="", width=3).grid(column=2, row=5, sticky=E)
stop_button = ttk.Button(headerframe, text="Stop", command=stop)
stop_button.grid(column=3, row=5, sticky=W)
ttk.Label(headerframe, text="Generation:  ").grid(column=4, row=5, sticky=E)
ttk.Label(headerframe, textvariable = _GENERATION).grid(column=5, row=5, sticky=E)

#Color chooser buttons
ttk.Label(headerframe, text="", width=3).grid(column=6, row=5, sticky=E)
foreColor_button = ttk.Button(headerframe, text="Forecolor", command=chooseForeColor)
foreColor_button.grid(column=7, row=5, sticky=W)
backColor_button = ttk.Button(headerframe, text="Backcolor", command=chooseBackColor)
backColor_button.grid(column=8, row=5, sticky=W)


column_entry.focus()
root.bind('<Return>', start)



####MAIN LOGIC
_GRID = [_DEAD]*int(_ROWS.get())*int(_COLUMNS.get())
_RESET = True
generateStartingGrid(_GRID)


root.mainloop()