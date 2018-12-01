from random import randint
from math import sqrt

class Player(object):
	"""docstring for Bomberman"""
	def __init__(self,posx,posy,sizew,sizeh):
		self.posX = posx
		self.posY = posy
		self.width = sizew
		self.height = sizeh
		self.bombCount = 1
		self.bombRange = 1
		self.direct = 0
		self.lifes = 3
	def renderValues(self):
		return (self.posX,self.posY,self.width,self.height)
	def getPos(self):
		return [self.posX,self.posY]
	def realocate(self,mapa):
		ubicado = True	
		prob = 85
		while ubicado:
			i = 0
			while i < len(mapa)-1 and ubicado:
				j = 0
				while j < len(mapa[i])-1 and ubicado:
					if mapa[i][j][0] == 0:
						valor = randint(0,100)
						if valor >= prob:
							self.posX = i
							self.posY = j
							ubicado = False
					j+=1
				i+=1

class Node(object):
	"""docstring for Node"""
	def __init__(self,pos,parent,direction):
		self.parent = parent
		self.posX = pos[0]
		self.posY = pos[1]
		self.f = 0
		self.g = 0
		self.h = 0
		self.direction = direction
	def equal(self,node):
		if self.posX == node.posX and self.posY == node.posY:
			return True
		else:
			return False

class NPC(Player):
	"""docstring for NPC"""
	def __init__(self, posx,posy,sizew,sizeh,iaType,playerPos,dificulty,idI):
		Player.__init__(self, posx,posy,sizew,sizeh)
		self.iaType = iaType
		self.playerPos = playerPos
		self.area = 5
		self.level = dificulty
		self.estado = 1
		self.id = idI

	def muerte(self):
		self.estado = 0
	def pathfinding(self,posFin,maze):
		startNode = Node(self.getPos(),None,-1)
		endNode = Node(posFin,None,-1)
		openList = []
		closedList = []
		path = []
		openList.append((startNode,startNode.f))
		while len(openList) > 0:
			openList.sort(key=lambda x: x[1])
			currentNode = openList[0][0]
			closedList.append(currentNode)
			openList.pop(0)

			if currentNode.equal(endNode):
				
				newCurrent = currentNode
				while newCurrent != None:
					path.append(newCurrent.direction)
					newCurrent = newCurrent.parent
				path.pop(len(path)-1)
				path = path[::-1]
				return path

			children = []
			inVisited = False
			for direction,iteratingPositions in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0)]):
				nextPositions = (currentNode.posX + iteratingPositions[0], currentNode.posY + iteratingPositions[1])
				if not (maze[nextPositions[0]][nextPositions[1]][0] == 5 or maze[nextPositions[0]][nextPositions[1]][0] == 6 or maze[nextPositions[0]][nextPositions[1]][0] == 2 or maze[nextPositions[0]][nextPositions[1]][0] == 3 or maze[nextPositions[0]][nextPositions[1]][0] == 4 or maze[nextPositions[0]][nextPositions[1]][1] == 1 or maze[nextPositions[0]][nextPositions[1]][1] == 2):
					newNode = Node(nextPositions,currentNode,direction)
					inVisited = False
					for i in closedList:
						if i.equal(newNode):
							inVisited = True
							break
					if not(inVisited):
						children.append(newNode)
						
			inVisited = False
			for child in children:
				for i in closedList:
					if i.equal(child):
						inVisited = True
						break
				if inVisited:
					continue
				skip = False
				child.g = currentNode.g + 1
				child.h = ((child.posX - endNode.posX) ** 2) + ((child.posY - endNode.posY) ** 2)
				child.f = child.g + child.h
				for i in openList:
					if child.equal(i[0]):
						if child.g > i[0].g:
							skip = True
							break
				if not(skip):
					openList.append((child,child.f))
		return self.wandering(maze)

	def pathclosing(self,playerDir,maze,mazeSize,actualPos):

		playerPos = actualPos[:]
		if playerDir == 0:
			while playerPos[1] > 1 and maze[playerPos[0]][playerPos[1]-1][0] != 6 and  maze[playerPos[0]][playerPos[1]-1][0] != 5:
				playerPos[1]-=1
		elif playerDir == 1:
			while playerPos[0] < mazeSize[0]-2 and maze[playerPos[0]+1][playerPos[1]][0] != 6 and  maze[playerPos[0]+1][playerPos[1]][0] != 5:
				playerPos[0]+=1
		elif playerDir == 2:
			while playerPos[1] < mazeSize[1]-2 and maze[playerPos[0]][playerPos[1]+1][0] != 6 and  maze[playerPos[0]][playerPos[1]+1][0] != 5:
				playerPos[1]+=1
		elif playerDir == 3:
			while playerPos[0] > 1 and maze[playerPos[0]-1][playerPos[1]][0] != 6 and  maze[playerPos[0]-1][playerPos[1]][0] != 5:
				playerPos[0]-=1
		return self.pathfinding(playerPos,maze)

	def areaProtecting(self,posFin,maze):

		dist = sqrt((self.posX - posFin[0]) ** 2) + ((self.posY - posFin[1]) ** 2)

		if dist <= self.area:
			return self.pathfinding(posFin,maze)
		else:
			return self.wandering(maze)

	def bombDetect(self,bombs,maze):
		for i in bombs:
			if (i.posX == self.posX and abs(i.posY - self.posY) <= i.range) or (i.posY == self.posY and abs(i.posX - self.posX) <= i.range):
				
				return True,i.posX,i.posY,i.range
		return False,-1,-1,-1

	def bombAvoid(self,maze,x,y,r):
		ret = []
		if (x == self.posX and abs(y - self.posY) <= r): 
			if y > self.posY:
				if maze[self.posX][self.posY-1][0] == 0 and maze[self.posX][self.posY-1][1] != 2:
					ret.append(0)
				else:
					if maze[self.posX+1][self.posY][0] == 0 and maze[self.posX+1][self.posY][0] != 2:
						ret.append(3)
					elif maze[self.posX-1][self.posY][0] == 0 and maze[self.posX-1][self.posY][0] != 2:
						ret.append(2)

			elif y < self.posY:
				if maze[self.posX][self.posY+1][0] == 0 and maze[self.posX][self.posY+1][1] != 2:
					ret.append(1)
				else:
					if maze[self.posX+1][self.posY][0] == 0 and maze[self.posX+1][self.posY][1] != 2:
						ret.append(3)
					elif maze[self.posX-1][self.posY][0] == 0 and maze[self.posX-1][self.posY][1] != 2:
						ret.append(2)
			else:
				if maze[self.posX][self.posY+1][0] == 0 and  maze[self.posX][self.posY+1][1] != 2:
					ret.append(1)
				elif maze[self.posX][self.posY-1][0] == 0 and maze[self.posX][self.posY-1][1] != 2:
					ret.append(0)
				elif maze[self.posX+1][self.posY][0] == 0 and maze[self.posX+1][self.posY][1] != 2:
					ret.append(3)
				elif maze[self.posX-1][self.posY][0] == 0 and maze[self.posX-1][self.posY][1] != 2:
					ret.append(2)
				else:
					ret.append(4)

		elif (y == self.posY and abs(x - self.posX) <= r):
			if x > self.posX:
				if maze[self.posX-1][self.posY][0] == 0 and maze[self.posX-1][self.posY][1] != 2:
					ret.append(2)
				else:
					if maze[self.posX][self.posY+1][0] == 0 and maze[self.posX][self.posY+1][1] != 2:
						ret.append(1)
					elif maze[self.posX][self.posY-1][0] == 0 and maze[self.posX][self.posY-1][1] != 2:
						ret.append(0)

			elif x < self.posX:
				if maze[self.posX+1][self.posY][0] == 0 and maze[self.posX+1][self.posY][1] != 2:
					ret.append(3)
				else:
					if maze[self.posX+1][self.posY][0] == 0 and maze[self.posX+1][self.posY][1] != 2:
						ret.append(0)
					elif maze[self.posX-1][self.posY][0] == 0 and maze[self.posX-1][self.posY][1] != 2:
						ret.append(1)
			else:
				if maze[self.posX][self.posY+1][0] == 0 and maze[self.posX][self.posY+1][1] != 2:
					ret.append(1)
				elif maze[self.posX][self.posY-1][0] == 0 and maze[self.posX][self.posY-1][1] != 2:
					ret.append(0)
				elif maze[self.posX+1][self.posY][0] == 0 and maze[self.posX+1][self.posY][1] != 2:
					ret.append(3)
				elif maze[self.posX-1][self.posY][0] == 0 and maze[self.posX-1][self.posY][1] != 2:
					ret.append(2)
				else:
					ret.append(4)
		return ret

	def wandering(self,maze):
		ret = []
		random = randint(0,100)
		if self.direct == 0:
			probUp,probDown,probLeft,probRigth = 40,50,80,100
			if 0 <= random <= 40:
				if maze[self.posX][self.posY-1][1] != 2:
					ret.append(0)
			elif 41 <= random <= 50:
				if maze[self.posX][self.posY+1][1] != 2:
					ret.append(1)
			elif 51 <= random <= 75:
				if maze[self.posX-1][self.posY][1] != 2:
					ret.append(2)
			elif 76 <= random <= 100:
				if maze[self.posX+1][self.posY][1] != 2:
					ret.append(3)
		if self.direct == 1:
			probUp,probDown,probLeft,probRigth = 25,50,60,100
			if 0 <= random <= 25:
				if maze[self.posX][self.posY-1][1] != 2:
					ret.append(0)
			elif 26 <= random <= 50:
				if maze[self.posX][self.posY+1][1] != 2:
					ret.append(1)
			elif 51 <= random <= 60:
				if maze[self.posX-1][self.posY][1] != 2:
					ret.append(2)
			elif 61 <= random <= 100:
				if maze[self.posX+1][self.posY][1] != 2:
					ret.append(3)
		if self.direct == 2:
			probUp,probDown,probLeft,probRigth = 10,50,80,100
			if 0 <= random <= 10:
				if maze[self.posX][self.posY-1][1] != 2:
					ret.append(0)
			elif 11 <= random <= 50:
				if maze[self.posX][self.posY+1][1] != 2:
					ret.append(1)
			elif 51 <= random <= 75:
				if maze[self.posX-1][self.posY][1] != 2:
					ret.append(2)
			elif 75 <= random <= 100:
				if maze[self.posX+1][self.posY][1] != 2:
					ret.append(3)
		if self.direct == 3:
			probUp,probDown,probLeft,probRigth = 25,50,90,100
			if 0 <= random <= 25:
				if maze[self.posX][self.posY-1][1] != 2:
					ret.append(0)
			elif 26 <= random <= 50:
				if maze[self.posX][self.posY+1][1] != 2:
					ret.append(1)
			elif 51 <= random <= 90:
				if maze[self.posX-1][self.posY][1] != 2:
					ret.append(2)
			elif 91 <= random <= 100:
				if maze[self.posX+1][self.posY][1] != 2:
					ret.append(3)
		if len(ret) == 0:
			ret.append(4)
		return ret
