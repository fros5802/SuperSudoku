# Sudoku Game created my Mike Frost
# January 7th, 2023
	

import pygame, time
from random import randint, shuffle

class Sudoku:
	
	# Class scope coordinate variables
	x = 0  	# Horizontal location in grid
	y = 0	# Vertical location in grid
	dif = 500 / 9	# Conversion from pixel to grid square
	val = 0	# Storage spot for key values entered

	# Initialize pygame window size and title
	pygame.font.init()
	screen = pygame.display.set_mode((500, 600))
	pygame.display.set_caption("Super Sudoku")

	# Two fonts used to place text on the game board
	font1 = pygame.font.SysFont("comicsans", 40)
	font2 = pygame.font.SysFont("comicsans", 20)

	# Initialize the game by generating a solved board, remove entries based on the difficulty selection, 
	# then ensure there is only one valid solution, then let the player take over and try to solve.
	def __init__(self):

		# This is the game grid and it has scope throughout the entire Sudoku game class
		self.grid = [
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		# Let user select difficulty level
		self.level = self.selectLevel()
		# Find a complete solution for puzzle
		self.grid = self.solveGrid(self.grid, True)
		# Remove values to make the puzzle challenging
		self.grid = self.removeValues(self.grid, self.level)
	
	# Allow user to select level of difficulty
	def selectLevel(self):
		clickFlag = 0
		run = True
		grid = [
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[1, 0, 0, 0, 0, 0, 0, 0, 0],
		[2, 0, 0, 0, 0, 0, 0, 0, 0],
		[3, 0, 0, 0, 0, 0, 0, 0, 0],
		[4, 0, 0, 0, 0, 0, 0, 0, 0],
		[5, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		# Start event loops waiting for mouse click on the level number
		while run:
			# White color background
			self.screen.fill((255, 255, 255))
			# Loop through the events stored in event.get()
			for event in pygame.event.get():
				# Quit the game window
				if event.type == pygame.QUIT:
					run = False 
				# Get the mouse position to insert number   
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					self.get_cord(pos)
					clickFlag = 1

			# Draw the grid and place red box if the directional or mouse click happened
			self.draw(grid)
			promptOne = "Select level of difficulty by clicking one to five."
			promptTwo = ""
			self.instruction(promptOne, promptTwo)

			# On mouse click grab the number selected and exit
			if clickFlag == 1:
				self.draw_box()
				level = grid[int(self.x)][int(self.y)]
				run = False

			# Update window
			pygame.display.update()

		# Sleep for a moment so level selection is visible
		time.sleep(1)
		return level

	# Build coordinate location from pygame mouse location to which square in grid
	def get_cord(self, pos):
		self.x = pos[0]//self.dif
		self.y = pos[1]//self.dif
	
	# Highlight the cell selected
	def draw_box(self):
		for i in range(2):
			pygame.draw.line(self.screen, (255, 0, 0), (self.x * self.dif-3, (self.y + i)*self.dif), (self.x * self.dif + self.dif + 3, (self.y + i)*self.dif), 7)
			pygame.draw.line(self.screen, (255, 0, 0), ( (self.x + i)* self.dif, self.y * self.dif ), ((self.x + i) * self.dif, self.y * self.dif + self.dif), 7)  

	# Draw required lines for making Sudoku grid        
	def draw(self, grid):
		# Draw the lines
		for i in range (9):
			for j in range (9):
				if grid[i][j]!= 0:
	
					# Fill blue color in already numbered grid
					pygame.draw.rect(self.screen, (0, 153, 153), (i * self.dif, j * self.dif, self.dif + 1, self.dif + 1))
	
					# Fill grid with default numbers specified
					text1 = self.font1.render(str(grid[i][j]), 1, (0, 0, 0))
					self.screen.blit(text1, (i * self.dif + 15, j * self.dif))
		# Draw lines horizontally and verticallyto form grid          
		for i in range(10):
			if i % 3 == 0 :
				thick = 7
			else:
				thick = 1
			pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.dif), (500, i * self.dif), thick)
			pygame.draw.line(self.screen, (0, 0, 0), (i * self.dif, 0), (i * self.dif, 500), thick) 

	# Fill value entered in cell     
	def draw_val(self):
		text1 = self.font1.render(str(self.val), 1, (0, 0, 0))
		self.screen.blit(text1, (self.x * self.dif + 15, self.y * self.dif + 15))
	
	# Check if the value entered in board is valid
	def valid(self, grid, i, j):
		for it in range(9):
			if grid[i][it]== self.val:
				return False
			if grid[it][j]== self.val:
				return False
		it = i//3
		jt = j//3
		for i in range(it * 3, it * 3 + 3):
			for j in range (jt * 3, jt * 3 + 3):
				if grid[i][j]== self.val:
					return False
		return True

	# Display text on game board
	def instruction(self, stringOne, stringTwo):
		text1 = self.font2.render(stringOne, 1, (0, 0, 0))
		text2 = self.font2.render(stringTwo, 1, (0, 0, 0))
		self.screen.blit(text1, (20, 520))       
		self.screen.blit(text2, (20, 540))

	# Display options when solved
	def result(self):
		text1 = self.font1.render("FINISHED PRESS R or D", 1, (0, 0, 0))
		self.screen.blit(text1, (20, 570)) 

	# Tests to see if the current attempt successfully filled the grid.
	def checkGrid(self, grid):
		for row in range(0,9):
			for col in range(0,9):
				if grid[row][col] == 0:
					return False
		#We have a complete grid!  
		return True

	# Copy a grid
	def copyGrid(self, grid):	
		gridNew = []
		for r in range(0,9):
			gridNew.append([])
			for c in range(0,9):
				gridNew[r].append(grid[r][c])
		return gridNew

		#We have a complete grid!  
		return True
	
	# Checks if two grids are the same
	def compareGrid(self, gridOne, gridTwo):
		for row in range(0,9):
			for col in range(0,9):
				if gridOne[row][col] != gridTwo[row][col]:
					return False
		return True

	# Reinitializes the grid after a failed attempt to populate it with a good solution.
	def resetGrid(self):
		for row in range(0,9):
			for col in range(0,9):
				self.grid[row][col] = 0

	# Attempts to fill the grid with a random solution
	def solveGrid(self, grid, firstSolve):
		numberList=[1,2,3,4,5,6,7,8,9]
		gridComplete = False
		attempts = 0

		gridBackup = self.copyGrid(grid)

		while(gridComplete == False):

			#Find next empty cell
			for i in range(0,81):
				row=i//9
				col=i%9

				if grid[row][col]==0:
					shuffle(numberList)

					for value in numberList:

						#Check that this value has not already be used on this row
						if not(value in grid[row]):

							#Check that this value has not already be used on this column
							if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
								
								#Identify which of the 9 squares we are working on
								square=[]
								if row<3:
									if col<3:
										square=[grid[i][0:3] for i in range(0,3)]
									elif col<6:
										square=[grid[i][3:6] for i in range(0,3)]
									else:  
										square=[grid[i][6:9] for i in range(0,3)]
								elif row<6:
									if col<3:
										square=[grid[i][0:3] for i in range(3,6)]
									elif col<6:
										square=[grid[i][3:6] for i in range(3,6)]
									else:  
										square=[grid[i][6:9] for i in range(3,6)]
								else:
									if col<3:
										square=[grid[i][0:3] for i in range(6,9)]
									elif col<6:
										square=[grid[i][3:6] for i in range(6,9)]
									else:  
										square=[grid[i][6:9] for i in range(6,9)]
								
								#Check that this value has not already be used on this 3x3 square
								if not value in (square[0] + square[1] + square[2]):
									grid[row][col]=value
									break

			if self.checkGrid(grid):
				gridComplete = True
			else:
				if firstSolve:
					self.screen.fill((255, 255, 255))
					promptOne = "Solution Generation Attempts:"
					promptTwo = str(attempts)
									
					self.draw(grid)
					self.instruction(promptOne, promptTwo)
					pygame.display.update()

				grid = self.copyGrid(gridBackup)
			
			attempts = attempts + 1
		return grid.copy()

	# Remove values from the grid and make sure that it is still solvable via one solution
	def removeValues(self, grid, attempts):
		#A higher number of attempts will end up removing more numbers from the grid
		#Potentially resulting in more difficiult grids to solve!

		counter = 1
		while attempts > 0:
			#Select a random cell that is not already empty
			row = randint(0,8)
			col = randint(0,8)
			while grid[row][col] == 0:
				row = randint(0,8)
				col = randint(0,8)
			#Remember its cell value in case we need to put it back  
			backup = grid[row][col]
			grid[row][col] = 0

			#Take a full copy of the grid
			copyGridOne = self.copyGrid(grid)
			copyGridTwo = self.copyGrid(grid)

			gridOne = self.solveGrid(copyGridOne, True)
			gridTwo = self.solveGrid(copyGridTwo, True)

			#If two different solutions were found, then restore the original grid
			if (self.compareGrid(gridOne, gridTwo) == False):
				grid[row][col] = backup
				#We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
				attempts -= 1
		return grid.copy()

	# Check to see if the grid has been fully filled, if it has this is a solution
	def checkWin(self, grid):
		for row in range(0,9):
			for col in range(0,9):
				if grid[row][col] == 0:
					return False
		return True

	# Main control function for script, looks for key and mouse events and triggers functional code
	def eventLoop(self, grid):
		run = True
		flag1 = 0
		pause = False

		#make a copy of the grid for restoring start point if need be
		restoreGrid = self.copyGrid(grid)

		while run:
			# White color background
			self.screen.fill((255, 255, 255))
			# Loop through the events stored in event.get()
			for event in pygame.event.get():
				# Quit the game window
				if event.type == pygame.QUIT:
					run = False 
				# Get the mouse position to insert number   
				if event.type == pygame.MOUSEBUTTONDOWN:
					flag1 = 1
					pos = pygame.mouse.get_pos()
					self.get_cord(pos)
				# Get the number to be inserted if key pressed   
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.x-= 1
						flag1 = 1
					if event.key == pygame.K_RIGHT:
						self.x+= 1
						flag1 = 1
					if event.key == pygame.K_UP:
						self.y-= 1
						flag1 = 1
					if event.key == pygame.K_DOWN:
						self.y+= 1
						flag1 = 1

					if event.key == pygame.K_1:
						self.val = 1
					if event.key == pygame.K_2:
						self.val = 2   
					if event.key == pygame.K_3:
						self.val = 3
					if event.key == pygame.K_4:
						self.val = 4
					if event.key == pygame.K_5:
						self.val = 5
					if event.key == pygame.K_6:
						self.val = 6
					if event.key == pygame.K_7:
						self.val = 7
					if event.key == pygame.K_8:
						self.val = 8
					if event.key == pygame.K_9:
						self.val = 9

					# if enter is pressed solve the remaining spaces
					if event.key == pygame.K_RETURN:
						grid = self.solveGrid(grid, False)
					# If esc is pressed reset the board to start
					if event.key == pygame.K_ESCAPE:
						grid = self.copyGrid(restoreGrid)

			# If a value has been entered, place it in the grid
			if self.val != 0:
				if restoreGrid[int(self.x)][int(self.y)] != 0:
					self.val = restoreGrid[int(self.x)][int(self.y)]
				self.draw_val()
				if self.valid(grid, int(self.x), int(self.y))== True:
					grid[int(self.x)][int(self.y)]= self.val
					flag1 = 0
				else:
					if restoreGrid[int(self.x)][int(self.y)] == 0:
						grid[int(self.x)][int(self.y)]= 0
				self.val = 0

			# Draw the grid and place red box if the directional or mouse click happened
			self.draw(grid)
			if flag1 == 1:
				self.draw_box()

			# Check to see if the puzzle is complete
			if self.checkWin(grid):
				promptOne = "You've won the game!"
				promptTwo = "Nice work, press Space to exit."
				self.instruction(promptOne, promptTwo)
				run = False
				pause = True
			else:
				promptOne = "Press ESC to reset the puzzle"
				promptTwo = "Press Enter to see the solution"
				self.instruction(promptOne, promptTwo)

			# Update window
			pygame.display.update()
		
		# When the puzzle is complete, wait for exit key before closing the window
		while pause:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						pause = False
				if event.type == pygame.QUIT:
					pause = False

		# Quit pygame window   
		pygame.quit()    

def main():

	mySudoku = Sudoku()
	mySudoku.eventLoop(mySudoku.grid)

if __name__ == "__main__":
	main()