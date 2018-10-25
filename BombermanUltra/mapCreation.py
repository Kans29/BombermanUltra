from random import randint

class GameMap(object):
	"""docstring for GameMap"""
	"""
	0 -> Walking path
	1 -> Player 1
	2 -> Player 2
	3 -> Player 3
	4 -> Player 4
	5 -> Bomb
	6 -> Breackable wall
	7 -> Not breackable wall
	8 and later -> PowerUp item
	"""
	def __init__(self, width,heigth,players):
		if width%2 == 0:
			width+=1
		if heigth%2 == 0:
			heigth+=1
		self.size = (width,heigth)
		self.maze = [[-1 for i in range(heigth)] for j in range(width)]
		self.numPlayer = players
		self.generate()
		

	def generate(self):
		width = self.size[0]
		heigth = self.size[1]
		for i in range(width):
			for j in range(heigth):
				if (i == 0 or i == width-1 or j == 0 or j == heigth-1) or ( i%2 == 0 and j%2 == 0):
					self.maze[i][j] = 7
				elif (i == 1 and j == 1) or (i == width-2 and j == heigth-2) or (i == width-2 and j == 1) or (i == 1 and j == heigth-2):
					self.maze[i][j] = 0
					if self.maze[i+1][j] != 0:
						self.maze[i+1][j] = 0
					if self.maze[i-1][j] != 0:
						self.maze[i-1][j] = 0
					if self.maze[i][j+1] != 0:
						self.maze[i][j+1] = 0
					if self.maze[i][j-1] != 0:
						self.maze[i][j-1] = 0
				elif self.maze[i][j] == -1:
					valor = randint(0,100)
					if valor <=50:
						self.maze[i][j] = 0
					else:
						self.maze[i][j] = 6
		for i in range(self.numPlayer):
			if i == 0:
				self.maze[1][1] = 1
			if i == 1:
				self.maze[1][heigth-2] = 2
			if i == 2:
				self.maze[width-2][1] = 3
			if i == 3:
				self.maze[width-2][heigth-2] = 4

	def printMaze(self):
		for i in self.maze:
			print(i)
	def getMaze(self):
		return self.maze

		