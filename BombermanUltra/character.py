class Player(object):
	"""docstring for Bomberman"""
	def __init__(self):
		self.posX = 1
		self.posY = 1
		self.width = 30
		self.height = 30
		self.bombCount = 1
	def renderValues(self):
		return (self.posX,self.posY,self.width,self.height)
