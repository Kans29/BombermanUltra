class Player(object):
	"""docstring for Bomberman"""
	def __init__(self,posx,posy,sizew,sizeh):
		self.posX = posx
		self.posY = posy
		self.width = sizew
		self.height = sizeh
		self.bombCount = 1
	def renderValues(self):
		return (self.posX,self.posY,self.width,self.height)
		
class NPC(Player):
	"""docstring for NPC"""
	def __init__(self, arg):
		Player.__init__(self, posx,posy)
		