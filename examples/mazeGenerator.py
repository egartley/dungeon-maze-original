#Author Cameron Gower
# Purpose show the maze generation process
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve import BacktrackingSolver


#playerSelectedDiffuclty = float(input("Enter a number  that is greater than 0 and less than or equal to 1.0 ex 0.29 or 1.0"))
#playerSelectedRows = int(input("enter an integer number of rows in the maze"))
#playerSelectedCols = int(input("enter an integer number of columns in the maze/n"))

m = Maze()

m.generator= Prims(10,15)
m.generate()
m.generate_entrances()
#m.generate_monte_carlo(100, 10, 1.0)

print(m)