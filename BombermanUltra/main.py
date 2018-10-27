import pygame
from character import Player
from character import NPC
from mapCreation import GameMap
from bomb import Bomb
from bomb import Explosion
pygame.init()

winW,winH = 600,600
mazeW,mazeH,playerCant = 15,15,4
playerPos = []
blocksW,blocksH = winW//mazeH , winH//mazeH
Bombs = []
Explosions = []
window = pygame.display.set_mode((winW,winH))
pygame.display.set_caption("Bomberman Ultra")

mainLoop = True
NPCs, NumNPC, NPCmov = [], playerCant-1, [[] for x in range(playerCant-1)]

mainMaze = GameMap(mazeW,mazeH,playerCant)
mazeRender = mainMaze.getMaze()

i, len1 = 0,len(mazeRender)
while i < len1:
	j, len2 = 0,len(mazeRender[i])
	while j < len2:
		if mazeRender[i][j][0] == 0 or mazeRender[i][j][0] == 1 or mazeRender[i][j][0] == 2 or mazeRender[i][j][0] == 3 or mazeRender[i][j][0] == 4: 
			#Represents walking paths, white snow block
			pygame.draw.rect(window,(255,250,250),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
		if mazeRender[i][j][1] == 1: 
			#Represents Bomb, Black
			pygame.draw.rect(window, (0,0,0),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
		if mazeRender[i][j][1] == 2: 
			#Represents explosion, orange 
			pygame.draw.rect(window,(255,165,0),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
		if mazeRender[i][j][0] == 1: 
			#Represents player 1. blue
			Bomberman = Player(i,j,blocksW-10,blocksH-10)
			playerPos = [i,j]
			values = Bomberman.renderValues()
			pygame.draw.rect(window,(0,0,255),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
		if mazeRender[i][j][0] == 2: 
			#Represents player 2. Red
			NumNPC -=1
			NPCs.append(NPC(i,j,blocksW-10,blocksH-10,1,playerPos))
			values = NPCs[0].renderValues()
			pygame.draw.rect(window,(255,0,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
		if mazeRender[i][j][0] == 3: 
			#Represents player 3. Green
			NumNPC -=1
			NPCs.append(NPC(i,j,blocksW-10,blocksH-10,2,playerPos))
			values = NPCs[1].renderValues()
			pygame.draw.rect(window,(0,25,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
		if mazeRender[i][j][0] == 4: 
			#Represents player 4. Yellow
			NumNPC -=1
			NPCs.append(NPC(i,j,blocksW-10,blocksH-10,3,playerPos))
			values = NPCs[2].renderValues()
			pygame.draw.rect(window,(255,255,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
		if mazeRender[i][j][0] == 5: 
			#represents breackable wall, brown
			pygame.draw.rect(window,(210,105,30),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
		if mazeRender[i][j][0] == 6: 
			#Represents unbreackable wall, gray
			pygame.draw.rect(window,(128,128,128),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
		j+=1
	i+=1
NumNPC = playerCant-1

while mainLoop:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			mainLoop = False

	#Main movement handler
	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT]:
		if mazeRender[Bomberman.posX-1][Bomberman.posY][0] == 0 and mazeRender[Bomberman.posX-1][Bomberman.posY][1] != 1:
			mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
			mazeRender[Bomberman.posX-1][Bomberman.posY][0] = 1
			Bomberman.posX -= 1
			Bomberman.direct = 3
			index = 0
			for NPC in NPCs:
				#Pathfinding
				if NPC.iaType == 1: 
					NPCmov[index] = NPC.pathfinding(Bomberman.getPos(),mazeRender)
					index +=1
				elif NPC.iaType == 2:
					NPC.playerPos[0]-=1
					NPCmov[index] = NPC.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH])
					index +=1
				elif NPC.iaType == 3:
					NPCmov[index] = NPC.areaProtecting(Bomberman.getPos(),mazeRender)
					index +=1
	if keys[pygame.K_RIGHT]:
		if mazeRender[Bomberman.posX+1][Bomberman.posY][0] == 0 and mazeRender[Bomberman.posX+1][Bomberman.posY][1] != 1:
			mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
			mazeRender[Bomberman.posX+1][Bomberman.posY][0] = 1
			Bomberman.posX += 1
			Bomberman.direct = 1
			index = 0
			for NPC in NPCs:
				#Pathfinding
				if NPC.iaType == 1: 
					NPCmov[index] =  NPC.pathfinding(Bomberman.getPos(),mazeRender)
					index +=1
				elif NPC.iaType == 2:
					NPC.playerPos[0]+=1
					NPCmov[index] = NPC.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH])
					index +=1
				elif NPC.iaType == 3:
					NPCmov[index] = NPC.areaProtecting(Bomberman.getPos(),mazeRender)
					index +=1
	if keys[pygame.K_UP]:
		if mazeRender[Bomberman.posX][Bomberman.posY-1][0] == 0 and mazeRender[Bomberman.posX][Bomberman.posY-1][1] != 1:
			mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
			mazeRender[Bomberman.posX][Bomberman.posY-1][0] = 1
			Bomberman.posY -= 1
			Bomberman.direct = 0
			index = 0
			for NPC in NPCs:
				#Pathfinding
				if NPC.iaType == 1: 
					NPCmov[index] =  NPC.pathfinding(Bomberman.getPos(),mazeRender)
					index +=1
				elif NPC.iaType == 2:
					NPC.playerPos[1]-=1
					NPCmov[index] = NPC.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH])
					index +=1
				elif NPC.iaType == 3:
					NPCmov[index] = NPC.areaProtecting(Bomberman.getPos(),mazeRender)
					index +=1
	if keys[pygame.K_DOWN]:
		if mazeRender[Bomberman.posX][Bomberman.posY+1][0] == 0  and mazeRender[Bomberman.posX][Bomberman.posY+1][1] != -1:
			mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
			mazeRender[Bomberman.posX][Bomberman.posY+1][0] = 1
			Bomberman.posY += 1
			Bomberman.direct = 2
			index = 0
			for NPC in NPCs:
				#Pathfinding
				if NPC.iaType == 1: 
					NPCmov[index] = NPC.pathfinding(Bomberman.getPos(),mazeRender)
					index +=1
				elif NPC.iaType == 2:
					NPC.playerPos[1]+=1
					NPCmov[index] = NPC.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH])
					index +=1
				elif NPC.iaType == 3:
					NPCmov[index] = NPC.areaProtecting(Bomberman.getPos(),mazeRender)
					index +=1
	if keys[pygame.K_SPACE]:
		if mazeRender[Bomberman.posX][Bomberman.posY][1] == 0:
			if Bomberman.bombCount > 0:
				mazeRender[Bomberman.posX][Bomberman.posY][1] = 1
				Bombs.append(Bomb(Bomberman.posX,Bomberman.posY))
				Bomberman.bombCount -= 1
				"""
				for NPC in NPCs:
					#Pathfinding
					if NPC.iaType == 1: 
						NPCmov[index] = NPC.pathfinding(Bomberman.getPos(),mazeRender)
						index +=1
					elif NPC.iaType == 2:
						NPCmov[index] = NPC.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH])
						index +=1
					elif NPC.iaType == 3:
						NPCmov[index] = NPC.areaProtecting(Bomberman.getPos(),mazeRender)
						index +=1
				"""
	#Main movement handler end

	#NPC movement
	index = 0
	for NPC in NPCs:
		#Pathfinding
		if NPC.iaType == 1:
			NPCmov[index] = NPC.pathfinding(Bomberman.getPos(),mazeRender)
			index +=1
		elif NPC.iaType == 2:
			NPCmov[index] = NPC.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH])
			index +=1
		elif NPC.iaType == 3:
			NPCmov[index] = NPC.areaProtecting(Bomberman.getPos(),mazeRender)
			index +=1
	i = 0
	while i < NumNPC:
		if NPCmov[i] != []:
			direction = NPCmov[i][0]
			if direction == 0:
				if mazeRender[NPCs[i].posX][NPCs[i].posY-1][0] == 0:
					mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
					mazeRender[NPCs[i].posX][NPCs[i].posY-1][0] = i+2
					NPCs[i].posY -=1
					NPCs[i].direct = 0
			if direction == 2:
				if mazeRender[NPCs[i].posX-1][NPCs[i].posY][0] == 0:
					mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
					mazeRender[NPCs[i].posX-1][NPCs[i].posY][0] = i+2
					NPCs[i].posX -=1
					NPCs[i].direct = 3
			if direction == 1:
				if mazeRender[NPCs[i].posX][NPCs[i].posY+1][0] == 0:
					mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
					mazeRender[NPCs[i].posX][NPCs[i].posY+1][0] = i+2
					NPCs[i].posY +=1
					NPCs[i].direct = 2
			if direction == 3:
				if mazeRender[NPCs[i].posX+1][NPCs[i].posY][0] == 0:
					mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
					mazeRender[NPCs[i].posX+1][NPCs[i].posY][0] = i+2
					NPCs[i].posX +=1
					NPCs[i].direct = 1
			NPCmov[i].pop(0)
		i+=1
	#NPC movement end

	#Main map rendering
	i, len1 = 0,len(mazeRender)
	while i < len1:
		j, len2 = 0,len(mazeRender[i])
		while j < len2:
			if mazeRender[i][j][0] == 0 or mazeRender[i][j][0] == 1 or mazeRender[i][j][0] == 2 or mazeRender[i][j][0] == 3 or mazeRender[i][j][0] == 4: 
				#Represents walking paths, white snow block
				pygame.draw.rect(window,(255,250,250),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
			if mazeRender[i][j][1] == 1: 
				#Represents Bomb, Black
				pygame.draw.rect(window, (0,0,0),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
			if mazeRender[i][j][1] == 2: 
				#Represents explosion, orange 
				pygame.draw.rect(window,(255,165,0),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
			if mazeRender[i][j][0] == 1: 
				#Represents player 1. blue
				values = Bomberman.renderValues()
				pygame.draw.rect(window,(0,0,255),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
			if mazeRender[i][j][0] == 2: 
				#Represents player 2. Red
				values = NPCs[0].renderValues()
				pygame.draw.rect(window,(255,0,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
			if mazeRender[i][j][0] == 3: 
				#Represents player 3. Green
				values = NPCs[1].renderValues()
				pygame.draw.rect(window,(0,25,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
			if mazeRender[i][j][0] == 4: 
				#Represents player 4. Yellow
				values = NPCs[2].renderValues()
				pygame.draw.rect(window,(255,255,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
			if mazeRender[i][j][0] == 5: 
				#represents breackable wall, brown
				pygame.draw.rect(window,(210,105,30),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
			if mazeRender[i][j][0] == 6: 
				#Represents unbreackable wall, gray
				pygame.draw.rect(window,(128,128,128),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
			j+=1
		i+=1
	#re render player and NPCs
	for i in range(playerCant):
		if i == 0:
			values = Bomberman.renderValues()
			pygame.draw.rect(window,(0,0,255),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
		if i == 1:
			values = NPCs[0].renderValues()
			pygame.draw.rect(window,(255,0,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
		if i == 2:
			values = NPCs[1].renderValues()
			pygame.draw.rect(window,(0,25,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
		if i == 3:
			values = NPCs[2].renderValues()
			pygame.draw.rect(window,(255,255,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
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
				if Bombs[i].posX+j+1 <= mazeW:
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

				if Bombs[i].posY+j+1 <= mazeH:
					if mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][0] != 6:
						if mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][0] == 5:
							mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][0] = 0
						if mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][1] == 0:
							mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][1] = 2
							Explosions.append(Explosion(Bombs[i].posX,Bombs[i].posY+j+1))
			del Bombs[i]
			Bomberman.bombCount += 1
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
	pygame.time.delay(200)

pygame.quit()