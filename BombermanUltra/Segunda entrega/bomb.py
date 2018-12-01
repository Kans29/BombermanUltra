class Bomb(object):
	"""docstring for Bomb"""
	def __init__(self, posx,posy,rangeB,idI):
		self.posX = posx
		self.posY = posy
		self.range = rangeB
		self.time = 1000
		self.id = idI

	def decreaseTime(self):
		self.time -= 100
	def exploded(self):
		if self.time <= 0:
			return True
		else:
			return False
class Explosion(object):
	"""docstring for Explosion"""
	def __init__(self, posx, posy):
		self.posX = posx
		self.posY = posy
		self.time = 600

	def decreaseTime(self):
		self.time -= 100

	def ended(self):
		if self.time <= 0:
			return True
		else:
			return False

		
		