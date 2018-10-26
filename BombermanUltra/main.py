import pygame
from character import Player
from mapCreation import GameMap
from bomb import Bomb
from bomb import Explosion
pygame.init()

winW,winH = 600,600
blockW,blockH,playerCant = 15,15,1
Bombs = []
Explosions = []
window = pygame.display.set_mode((winW,winH))
pygame.display.set_caption("Bomberman Ultra")

Bomberman = Player()
mainLoop = True

mainMaze = GameMap(blockW,blockH,playerCant)

mazeRender = mainMaze.getMaze()
i, len1 = 0,len(mazeRender)
while i < len1:
	j, len2 = 0,len(mazeRender[i])
	while j < len2:
		if mazeRender[i][j][0] == 0 or mazeRender[i][j][0] == 1 or mazeRender[i][j][0] == 2 or mazeRender[i][j][0] == 3 or mazeRender[i][j][0] == 4: 
			#Represents walking paths, white snow block
			pygame.draw.rect(window,(255,250,250),((i)*40,(j)*40,40,40))
		if mazeRender[i][j][1] == 1: 
			#Represents Bomb, Black
			pygame.draw.rect(window, (0,0,0),((i)*40,(j)*40,40,40))
		if mazeRender[i][j][1] == 2: 
			#Represents explosion, orange 
			pygame.draw.rect(window,(255,165,0),((i)*40,(j)*40,40,40))
		if mazeRender[i][j][0] == 1: 
			#Represents player 1. blue
			values = Bomberman.renderValues()
			pygame.draw.rect(window,(0,0,255),(((values[0])*40)+4,((values[1])*40)+4,values[2],values[3]))
		if mazeRender[i][j][0] == 2: 
			#Represents player 2. Red
			pygame.draw.rect(window,(255,0,0),((i)*40,(j)*40,40,40))
		if mazeRender[i][j][0] == 3: 
			#Represents player 3. Green
			pygame.draw.rect(window,(0,25,0),((i)*40,(j)*40,40,40))
		if mazeRender[i][j][0] == 4: 
			#Represents player 4. Yellow
			pygame.draw.rect(window,(255,255,0),((i)*40,(j)*40,40,40))
		if mazeRender[i][j][0] == 5: 
			#represents breackable wall, brown
			pygame.draw.rect(window,(210,105,30),((i)*40,(j)*40,40,40))
		if mazeRender[i][j][0] == 6: 
			#Represents unbreackable wall, gray
			pygame.draw.rect(window,(128,128,128),((i)*40,(j)*40,40,40))
		j+=1
	i+=1

while mainLoop:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			mainLoop = False

	#Main movement handler
	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT]:
		if mazeRender[Bomberman.posX-1][Bomberman.posY][0] == 0:
			mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
			mazeRender[Bomberman.posX-1][Bomberman.posY][0] = 1
			Bomberman.posX -= 1
	if keys[pygame.K_RIGHT]:
		if mazeRender[Bomberman.posX+1][Bomberman.posY][0] == 0:
			mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
			mazeRender[Bomberman.posX+1][Bomberman.posY][0] = 1
			Bomberman.posX += 1
	if keys[pygame.K_UP]:
		if mazeRender[Bomberman.posX][Bomberman.posY-1][0] == 0:
			mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
			mazeRender[Bomberman.posX][Bomberman.posY-1][0] = 1
			Bomberman.posY -= 1
	if keys[pygame.K_DOWN]:
		if mazeRender[Bomberman.posX][Bomberman.posY+1][0] == 0:
			mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
			mazeRender[Bomberman.posX][Bomberman.posY+1][0] = 1
			Bomberman.posY += 1
	if keys[pygame.K_SPACE]:
		if mazeRender[Bomberman.posX][Bomberman.posY][1] == 0:
			mazeRender[Bomberman.posX][Bomberman.posY][1] = 1
			Bombs.append(Bomb(Bomberman.posX,Bomberman.posY))
	#Main movement handler end

	#Main map rendering
	i,len1 = 0,len(mazeRender)
	while i < len1:
		j , len2= 0,len(mazeRender[i])
		while j < len2:
			if mazeRender[i][j][0] == 0 or mazeRender[i][j][0] == 1 or mazeRender[i][j][0] == 2 or mazeRender[i][j][0] == 3 or mazeRender[i][j][0] == 4: 
				#Represents walking paths, white snow block
				pygame.draw.rect(window,(255,250,250),((i)*40,(j)*40,40,40))
			if mazeRender[i][j][1] == 1: 
				#Represents Bomb, Black
				pygame.draw.rect(window, (0,0,0),((i)*40,(j)*40,40,40))
			if mazeRender[i][j][1] == 2: 
				#Represents explosion, orange 
				pygame.draw.rect(window,(255,165,0),((i)*40,(j)*40,40,40))
			if mazeRender[i][j][0] == 1: 
				#Represents player 1. blue
				values = Bomberman.renderValues()
				pygame.draw.rect(window,(0,0,255),(((values[0])*40)+4,((values[1])*40)+4,values[2],values[3]))
			if mazeRender[i][j][0] == 2: 
				#Represents player 2. Red
				pygame.draw.rect(window,(255,0,0),((i)*40,(j)*40,40,40))
			if mazeRender[i][j][0] == 3: 
				#Represents player 3. Green
				pygame.draw.rect(window,(0,25,0),((i)*40,(j)*40,40,40))
			if mazeRender[i][j][0] == 4: 
				#Represents player 4. Yellow
				pygame.draw.rect(window,(255,255,0),((i)*40,(j)*40,40,40))
			if mazeRender[i][j][0] == 5: 
				#represents breackable wall, brown
				pygame.draw.rect(window,(210,105,30),((i)*40,(j)*40,40,40))
			if mazeRender[i][j][0] == 6: 
				#Represents unbreackable wall, gray
				pygame.draw.rect(window,(128,128,128),((i)*40,(j)*40,40,40))
			j+=1
		i+=1
	#Main map rendering end

	#Handling bomb explosion
	i = len(Bombs)-1
	while i >= 0:
		Bombs[i].decreaseTime()
		if Bombs[i].exploded():
			mazeRender[Bombs[i].posX][Bombs[i].posY][1] = 2
			Explosions.append(Explosion(Bombs[i].posX,Bombs[i].posY))
			rangeBomb = Bombs[i].range
			for j in range(rangeBomb):
				if Bombs[i].posX+j+1 <= blockW:
					if mazeRender[Bombs[i].posX+j+1][Bombs[i].posY][0] != 6:
						if mazeRender[Bombs[i].posX+j+1][Bombs[i].posY][0] == 5:
							mazeRender[Bombs[i].posX+j+1][Bombs[i].posY][0] = 0
						if mazeRender[Bombs[i].posX+j+1][Bombs[i].posY][1] == 0:
							mazeRender[Bombs[i].posX+j+1][Bombs[i].posY][1] = 2
							Explosions.append(Explosion(Bombs[i].posX+j+1,Bombs[i].posY))

				if Bombs[i].posY-(j+1) >= 0:
					if mazeRender[Bombs[i].posX][Bombs[i].posY-(j+1)][0] != 6:
						if mazeRender[Bombs[i].posX][Bombs[i].posY-(j+1)][0] == 5:
							mazeRender[Bombs[i].posX][Bombs[i].posY-(j+1)][0] = 0
						if mazeRender[Bombs[i].posX][Bombs[i].posY-(j+1)][1] == 0:
							mazeRender[Bombs[i].posX][Bombs[i].posY-(j+1)][1] = 2
							Explosions.append(Explosion(Bombs[i].posX,Bombs[i].posY-(j+1)))

				if Bombs[i].posX-(j+1) >= 0:
					if mazeRender[Bombs[i].posX-(j+1)][Bombs[i].posY][0] != 6:
						if mazeRender[Bombs[i].posX-(j+1)][Bombs[i].posY][0] == 5:
							mazeRender[Bombs[i].posX-(j+1)][Bombs[i].posY][0] = 0
						if mazeRender[Bombs[i].posX-(j+1)][Bombs[i].posY][1] == 0:
							mazeRender[Bombs[i].posX-(j+1)][Bombs[i].posY][1] = 2
							Explosions.append(Explosion(Bombs[i].posX-(j+1),Bombs[i].posY))

				if Bombs[i].posY+j+1 <= blockH:
					if mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][0] != 6:
						if mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][0] == 5:
							mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][0] = 0
						if mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][1] == 0:
							mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][1] = 2
							Explosions.append(Explosion(Bombs[i].posX,Bombs[i].posY+j+1))
			del Bombs[i]
		i-=1
	i = len(Explosions)-1
	while i >= 0:
		Explosions[i].decreaseTime()
		if Explosions[i].ended():
			mazeRender[Explosions[i].posX][Explosions[i].posY][1] = 0
			del Explosions[i]
		i-=1
	#ENd handling bomb explosions
	pygame.display.update()
	pygame.time.delay(100)

pygame.quit()