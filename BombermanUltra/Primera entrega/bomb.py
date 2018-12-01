class Bomb(object):
	"""docstring for Bomb"""
	def __init__(self, posx,posy):
		self.posX = posx
		self.posY = posy
		self.range = 1
		self.time = 1000

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
		
		