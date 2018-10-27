from collections import deque

class Player(object):
	"""docstring for Bomberman"""
	def __init__(self,posx,posy,sizew,sizeh):
		self.posX = posx
		self.posY = posy
		self.width = sizew
		self.height = sizeh
		self.bombCount = 1
		self.direct = 0
	def renderValues(self):
		return (self.posX,self.posY,self.width,self.height)
	def getPos(self):
		return [self.posX,self.posY]

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
	def __init__(self, posx,posy,sizew,sizeh,iaType,playerPos):
		Player.__init__(self, posx,posy,sizew,sizeh)
		self.iaType = iaType
		self.playerPos = playerPos

	def pathfinding(self,posFin,maze):
		startNode = Node(self.getPos(),None,-1)
		endNode = Node(posFin,None,-1)
		openList = []
		closedList = []
		openList.append((startNode,startNode.f))
		while len(openList) > 0:
			openList.sort(key=lambda x: x[1])
			currentNode = openList[0][0]
			closedList.append(currentNode)
			openList.pop(0)

			if currentNode.equal(endNode):
				path = []
				newCurrent = currentNode
				while newCurrent != None:
					path.append(newCurrent.direction)
					newCurrent = newCurrent.parent
				path.pop(len(path)-1)
				return path[::-1]

			children = []
			for direction,iteratingPositions in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0)]):
				nextPositions = (currentNode.posX + iteratingPositions[0], currentNode.posY + iteratingPositions[1])
				if not (maze[nextPositions[0]][nextPositions[1]][0] == 5 or maze[nextPositions[0]][nextPositions[1]][0] == 6 ):
					newNode = Node(nextPositions,currentNode,direction)
					if newNode not in closedList:
						children.append(newNode)

			for child in children:
				if not(child in closedList):
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

	def pathclosing(self,playerDir,maze,mazeSize):

		playerPos = self.playerPos[:]
		if playerDir == 0:
			while playerPos[1] > 1:
				playerPos[1]-=1
		elif playerDir == 1:
			while playerPos[0] < mazeSize[0]-2:
				playerPos[0]+=1
		elif playerDir == 2:
			while playerPos[1] < mazeSize[1]-2:
				playerPos[1]+=1
		elif playerDir == 3:
			while playerPos[0] > 1:
				playerPos[0]-=1
		return self.pathfinding(playerPos,maze)