import pygame
from character import Player
from mapCreation import GameMap
pygame.init()

winW,winH = 600,600
blockW,blockH,playerCant = 15,15,1
window = pygame.display.set_mode((winW,winH))
pygame.display.set_caption("Bomberman Ultra")

Bomberman = Player()
mainLoop = True

mainMaze = GameMap(blockW,blockH,playerCant)

mainMaze.printMaze()

mazeRender = mainMaze.getMaze()
i = 0
while i < len(mazeRender):
	j = 0
	while j < len(mazeRender[i]):
		if mazeRender[i][j] == 0 or mazeRender[i][j] == 1 or mazeRender[i][j] == 2 or mazeRender[i][j] == 3 or mazeRender[i][j] == 4: 
			#Represents walking paths, white snow block
			pygame.draw.rect(window,(255,250,250),((i)*40,(j)*40,40,40))
		if mazeRender[i][j] == 1: 
			#Represents player 1. blue
			values = Bomberman.renderValues()
			pygame.draw.rect(window,(0,0,255),(((values[0])*40)+2,((values[1])*40)+2,values[2],values[3]))
		if mazeRender[i][j] == 2: 
			#Represents player 2. Red
			pygame.draw.rect(window,(255,0,0),((i)*40,(j)*40,40,40))
		if mazeRender[i][j] == 3: 
			#Represents player 3. Green
			pygame.draw.rect(window,(0,25,0),((i)*40,(j)*40,40,40))
		if mazeRender[i][j] == 4: 
			#Represents player 4. Yellow
			pygame.draw.rect(window,(255,255,0),((i)*40,(j)*40,40,40))
		if mazeRender[i][j] == 5: 
			#Represents Bomb, Black
			pygame.draw.rect(window,(0,0,0),((i)*40,(j)*40,40,40))
		if mazeRender[i][j] == 6: 
			#represents breackable wall, brown
			pygame.draw.rect(window,(210,105,30),((i)*40,(j)*40,40,40))
		if mazeRender[i][j] == 7: 
			#Represents unbreackable wall, gray
			pygame.draw.rect(window,(128,128,128),((i)*40,(j)*40,40,40))
		if mazeRender[i][j] == 8: 
			#Colors the block grey
			pygame.draw.rect(window,(112,128,144),((i)*40,(j)*40,40,40))
		j+=1
	i+=1

while mainLoop:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			mainLoop = False

	#Main movement handler
	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT]:
		if mazeRender[Bomberman.posX-1][Bomberman.posY] == 0:
			mazeRender[Bomberman.posX][Bomberman.posY] = 0
			mazeRender[Bomberman.posX-1][Bomberman.posY] = 1
			Bomberman.posX -= 1
	if keys[pygame.K_RIGHT]:
		if mazeRender[Bomberman.posX+1][Bomberman.posY] == 0:
			mazeRender[Bomberman.posX][Bomberman.posY] = 0
			mazeRender[Bomberman.posX+1][Bomberman.posY] = 1
			Bomberman.posX += 1
	if keys[pygame.K_UP]:
		if mazeRender[Bomberman.posX][Bomberman.posY-1] == 0:
			mazeRender[Bomberman.posX][Bomberman.posY] = 0
			mazeRender[Bomberman.posX][Bomberman.posY-1] = 1
			Bomberman.posY -= 1
	if keys[pygame.K_DOWN]:
		if mazeRender[Bomberman.posX][Bomberman.posY+1] == 0:
			mazeRender[Bomberman.posX][Bomberman.posY] = 0
			mazeRender[Bomberman.posX][Bomberman.posY+1] = 1
			Bomberman.posY += 1
	if keys[pygame.K_SPACE]:
		pass

	#Main map rendering
	i = 0
	while i < len(mazeRender):
		j = 0
		while j < len(mazeRender[i]):
			if mazeRender[i][j] == 0 or mazeRender[i][j] == 1 or mazeRender[i][j] == 2 or mazeRender[i][j] == 3 or mazeRender[i][j] == 4: 
				#Represents walking paths, white snow block
				pygame.draw.rect(window,(255,250,250),((i)*40,(j)*40,40,40))
			if mazeRender[i][j] == 1: 
				#Represents player 1. blue
				values = Bomberman.renderValues()
				pygame.draw.rect(window,(0,0,255),(((values[0])*40)+2,((values[1])*40)+2,values[2],values[3]))
			if mazeRender[i][j] == 2: 
				#Represents player 2. Red
				pygame.draw.rect(window,(255,0,0),((i)*40,(j)*40,40,40))
			if mazeRender[i][j] == 3: 
				#Represents player 3. Green
				pygame.draw.rect(window,(0,25,0),((i)*40,(j)*40,40,40))
			if mazeRender[i][j] == 4: 
				#Represents player 4. Yellow
				pygame.draw.rect(window,(255,255,0),((i)*40,(j)*40,40,40))
			if mazeRender[i][j] == 5: 
				#Represents Bomb, Black
				pygame.draw.rect(window,(0,0,0),((i)*40,(j)*40,40,40))
			if mazeRender[i][j] == 6: 
				#represents breackable wall, brown
				pygame.draw.rect(window,(210,105,30),((i)*40,(j)*40,40,40))
			if mazeRender[i][j] == 7: 
				#Represents unbreackable wall, gray
				pygame.draw.rect(window,(128,128,128),((i)*40,(j)*40,40,40))
			if mazeRender[i][j] == 8: 
				#Colors the block grey
				pygame.draw.rect(window,(112,128,144),((i)*40,(j)*40,40,40))
			j+=1
		i+=1
	pygame.display.update()
	pygame.time.delay(100)

pygame.quit()