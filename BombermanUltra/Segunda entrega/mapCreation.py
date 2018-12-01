from random import randint

class GameMap(object):
	"""docstring for GameMap"""
	"""
	every matrix value is a 2 element list [-,-], where the first covers constant rendering elements like walls, walkways and players
	 and de second one represents if there is active bombs, active bomb explosion, or powerups.
	 for the first rvalue:
	0 -> Walking path
	1 -> Player 1
	2 -> Player 2
	3 -> Player 3
	4 -> Player 4
	5 -> Breackable wall
	6 -> Not breackable wall
	for the second value:
	0 -> nothing
	1 -> Bomb
	2 -> bomb explosion
	3 -> powerup
	"""
	def __init__(self, width,heigth,players):
		if width%2 == 0:
			width+=1
		if heigth%2 == 0:
			heigth+=1
		self.size = (width,heigth)
		self.maze = [[[-1,0] for i in range(heigth)] for j in range(width)]
		self.numPlayer = players
		self.generate()
		

	def generate(self):
		width = self.size[0]
		heigth = self.size[1]
		for i in range(width):
			for j in range(heigth):
				if (i == 0 or i == width-1 or j == 0 or j == heigth-1) or ( i%2 == 0 and j%2 == 0):
					self.maze[i][j] = [6,0]
				elif (i == 1 and j == 1) or (i == width-2 and j == heigth-2) or (i == width-2 and j == 1) or (i == 1 and j == heigth-2):
					self.maze[i][j] = [0,0]
					if self.maze[i+1][j][0] != 0 and self.maze[i+1][j][0] != 6:
						self.maze[i+1][j] = [0,0]
					if self.maze[i-1][j][0] != 0 and self.maze[i-1][j][0] != 6:
						self.maze[i-1][j] = [0,0]
					if self.maze[i][j+1][0] != 0 and self.maze[i][j+1][0] != 6:
						self.maze[i][j+1] = [0,0]
					if self.maze[i][j-1][0] != 0 and self.maze[i][j-1][0] != 6:
						self.maze[i][j-1] = [0,0]
				elif self.maze[i][j][0] == -1:
					valor = randint(0,100)
					if valor <=50:
						self.maze[i][j] = [0,0]
					else:
						self.maze[i][j] = [5,0]
		for i in range(self.numPlayer):
			if i == 0:
				self.maze[1][1] = [1,0]
			if i == 1:
				self.maze[1][heigth-2] = [2,0]
			if i == 2:
				self.maze[width-2][1] = [3,0]
			if i == 3:
				self.maze[width-2][heigth-2] = [4,0]

	def printMaze(self):
		for i in self.maze:
			print(i)
	def getMaze(self):
		return self.maze

	def endingMaze(self,direct,maze,times):
		
		if direct == 1:
			i = self.size[0]-1-times
			j = self.size[1]-1-times
			while j >= 0+times :
				if maze[i][j][0] != 6:
					return i,j,direct,times
				j-=1
		elif direct == 0:
			i = 0+times
			j = self.size[1]-1-times
			while i < self.size[0]-1-times :
				if maze[i][j][0] != 6:
					return i,j,direct,times
				i+=1
		elif direct == 3:
			i = 0+times
			j = 0+times
			while j < self.size[1]-1-times  :
				if maze[i][j][0] != 6:
					return i,j,direct,times
				j+=1
		elif direct == 2:
			i = self.size[0]-1-times
			j = 0+times
			while i >= 0+times :
				if maze[i][j][0] != 6:
					return i,j,direct,times
				i-=1
		direct+=1
		if direct == 4:
			direct = 0
			times+=1
		return -1,-1,direct,times


		