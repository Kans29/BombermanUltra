class Player(object):
	"""docstring for Bomberman"""
	def __init__(self):
		self.posX = 0
		self.posY = 0
		self.width = 40
		self.height = 40
		self.vel = 5
	def renderValues(self):
		return (self.posX,self.posY,self.width,self.height)
