import pygame
from character import Player
from character import NPC
from mapCreation import GameMap
from bomb import Bomb
from bomb import Explosion
from math import floor
from menu import menuInicial
from continueFile import menuPerdida
from terminar import Victoria
pygame.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
imgBomb = pygame.image.load("BombaPU.jpg")
imgFire = pygame.image.load("rangoPU.jpg")
imgLife = pygame.image.load("vidaPU.jpg")
mainLoop = True
while mainLoop:

	menu = menuInicial()
	if menu == 0:
		mainLoop = False
		break
	nivel = True
	winW,winH = 1000,700
	mazeW,mazeH,playerCant = 21,21,4
	gameTime = 90000
	endDrop,side,times = 200,0,1
	timeLeft = myfont.render("Time left: "+str(gameTime/1000), False, (255, 255, 255))
	timeLeft = myfont.render("Time left: "+str(gameTime/1000), False, (255, 255, 255))
	dificulty = myfont.render("Dificulty: "+str(menu), False, (255, 255, 255))
	playerPos = []
	blocksW,blocksH = floor((winW-300)/mazeH) , floor(winH/mazeH)
	Bombs = []
	Explosions = []
	movementDelay = 3
	initialization = 0
	window = pygame.display.set_mode((winW,winH))
	window.blit(dificulty,(750,85))
	pygame.display.set_caption("Bomberman Ultra")

	NPCs, NumNPC,enemyDeleted, NPCmov = [], playerCant-1,0, [[] for x in range(playerCant-1)]

	mainMaze = GameMap(mazeW,mazeH,playerCant)
	mazeRender = mainMaze.getMaze()

	while nivel:
		if initialization == 0:
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
						playerPos = Bomberman.getPos()

						values = Bomberman.renderValues()
						pygame.draw.rect(window,(0,0,255),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
					if mazeRender[i][j][0] == 2: 
						#Represents player 2. Red
						NumNPC -=1
						newNPC = NPC(i,j,blocksW-10,blocksH-10,1,playerPos,menu,0)

						NPCs.append(newNPC)
						values = NPCs[0].renderValues()
						pygame.draw.rect(window,(255,0,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
					if mazeRender[i][j][0] == 3: 
						#Represents player 3. Green
						NumNPC -=1
						NPCs.append(NPC(i,j,blocksW-10,blocksH-10,2,playerPos,menu,1))
						values = NPCs[1].renderValues()
						pygame.draw.rect(window,(0,200,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
					if mazeRender[i][j][0] == 4: 
						#Represents player 4. Yellow
						NumNPC -=1
						NPCs.append(NPC(i,j,blocksW-10,blocksH-10,3,playerPos,menu,2))
						values = NPCs[2].renderValues()
						pygame.draw.rect(window,(255,255,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
					if mazeRender[i][j][0] == 5: 
						#represents breackable wall, brown
						pygame.draw.rect(window,(210,105,30),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
					if mazeRender[i][j][0] == 6: 
						#Represents unbreackable wall, gray
						pygame.draw.rect(window,(128,128,128),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
					if mazeRender[i][j] == [0,3]: 
						#Represents life Power up
						window.blit(imgLife, pygame.rect.Rect((i)*blocksW,(j)*blocksH,blocksW,blocksH))
					if mazeRender[i][j] == [0,4]: 
						#Represents bomb increment
						window.blit(imgBomb, pygame.rect.Rect((i)*blocksW,(j)*blocksH,blocksW,blocksH))
					if mazeRender[i][j] == [0,5]: 
						#Represents bomb range increment
						window.blit(imgFire, pygame.rect.Rect((i)*blocksW,(j)*blocksH,blocksW,blocksH))
					j+=1
				i+=1
			NumNPC = playerCant-1
			initialization = 1


		#Main movement handler
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			if mazeRender[Bomberman.posX-1][Bomberman.posY][0] != 6 and mazeRender[Bomberman.posX-1][Bomberman.posY][0] != 5 and mazeRender[Bomberman.posX-1][Bomberman.posY][1] != 1:
				mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
				mazeRender[Bomberman.posX-1][Bomberman.posY][0] = 1
				Bomberman.posX -= 1
				Bomberman.direct = 3
				index = 0
				if mazeRender[Bomberman.posX-1][Bomberman.posY][1] == 3:
					Bomberman.lifes+=1
					mazeRender[Bomberman.posX-1][Bomberman.posY][1] = 0
				if mazeRender[Bomberman.posX-1][Bomberman.posY][1] == 4:
					Bomberman.bombCount+=1
					mazeRender[Bomberman.posX-1][Bomberman.posY][1] = 0
				if mazeRender[Bomberman.posX-1][Bomberman.posY][1] == 5:
					Bomberman.bombRange+=1
					mazeRender[Bomberman.posX-1][Bomberman.posY][1] = 0
				for npc in NPCs:
					#Pathfinding
					if npc.level == 1 and npc.estado == 1:
						if npc.iaType == 1: 
							NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
							
						elif npc.iaType == 2:
							npc.playerPos[0]-=1
							NPCmov[index] = npc.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH],Bomberman.getPos())
							
						elif npc.iaType == 3:
							NPCmov[index] = npc.areaProtecting(Bomberman.getPos(),mazeRender)
							
					elif npc.level == 2 and npc.estado == 1:
						NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
						detect = npc.bombDetect(Bombs,mazeRender)
						if detect[0]:
							NPCmov[index] = npc.bombAvoid(mazeRender,detect[1],detect[2],detect[3])
					index +=1
		if keys[pygame.K_RIGHT]:
			if mazeRender[Bomberman.posX+1][Bomberman.posY][0] != 6 and mazeRender[Bomberman.posX+1][Bomberman.posY][0] != 5 and mazeRender[Bomberman.posX+1][Bomberman.posY][1] != 1:
				mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
				mazeRender[Bomberman.posX+1][Bomberman.posY][0] = 1
				Bomberman.posX += 1
				Bomberman.direct = 1
				if mazeRender[Bomberman.posX+1][Bomberman.posY][1] == 3:
					Bomberman.lifes+=1
					mazeRender[Bomberman.posX+1][Bomberman.posY][1] = 0
				if mazeRender[Bomberman.posX+1][Bomberman.posY][1] == 4:
					Bomberman.bombCount+=1
					mazeRender[Bomberman.posX+1][Bomberman.posY][1] = 0
				if mazeRender[Bomberman.posX+1][Bomberman.posY][1] == 5:
					Bomberman.bombRange+=1
					mazeRender[Bomberman.posX+1][Bomberman.posY][1] = 0
				index = 0
				for npc in NPCs:
					#Pathfinding
					if npc.level == 1 and npc.estado == 1:
						if npc.iaType == 1: 
							NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
							
						elif npc.iaType == 2:
							npc.playerPos[0]+=1
							NPCmov[index] = npc.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH],Bomberman.getPos())
							
						elif npc.iaType == 3:
							NPCmov[index] = npc.areaProtecting(Bomberman.getPos(),mazeRender)
							
					elif npc.level == 2 and npc.estado == 1:
						NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
						detect = npc.bombDetect(Bombs,mazeRender)
						if detect[0]:
							NPCmov[index] = npc.bombAvoid(mazeRender,detect[1],detect[2],detect[3])
					index +=1
		if keys[pygame.K_UP]:
			if mazeRender[Bomberman.posX][Bomberman.posY-1][0] != 5 and mazeRender[Bomberman.posX][Bomberman.posY-1][0] !=6 and  mazeRender[Bomberman.posX][Bomberman.posY-1][1] != 1:
				mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
				mazeRender[Bomberman.posX][Bomberman.posY-1][0] = 1
				Bomberman.posY -= 1
				Bomberman.direct = 0
				if mazeRender[Bomberman.posX][Bomberman.posY-1][1] == 3:
					Bomberman.lifes+=1
					mazeRender[Bomberman.posX][Bomberman.posY-1][1] = 0
				if mazeRender[Bomberman.posX][Bomberman.posY-1][1] == 4:
					Bomberman.bombCount+=1
					mazeRender[Bomberman.posX][Bomberman.posY-1][1] = 0
				if mazeRender[Bomberman.posX][Bomberman.posY-1][1] == 5:
					Bomberman.bombRange+=1
					mazeRender[Bomberman.posX][Bomberman.posY-1][1] = 0
				index = 0
				for npc in NPCs:
					#Pathfinding
					if npc.level == 1 and npc.estado == 1:
						if npc.iaType == 1: 
							NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
							
						elif npc.iaType == 2:
							npc.playerPos[1]-=1
							NPCmov[index] = npc.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH],Bomberman.getPos())
							
						elif npc.iaType == 3:
							NPCmov[index] = npc.areaProtecting(Bomberman.getPos(),mazeRender)
							
					elif npc.level == 2 and npc.estado == 1:
						NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
						detect = npc.bombDetect(Bombs,mazeRender)
						if detect[0]:
							NPCmov[index] = npc.bombAvoid(mazeRender,detect[1],detect[2],detect[3])
					index +=1
		if keys[pygame.K_DOWN]:
			if mazeRender[Bomberman.posX][Bomberman.posY+1][0] != 5 and mazeRender[Bomberman.posX][Bomberman.posY+1][0] != 6 and mazeRender[Bomberman.posX][Bomberman.posY+1][1] != -1:
				mazeRender[Bomberman.posX][Bomberman.posY][0] = 0
				mazeRender[Bomberman.posX][Bomberman.posY+1][0] = 1
				Bomberman.posY += 1
				Bomberman.direct = 2
				if mazeRender[Bomberman.posX][Bomberman.posY+1][1] == 3:
					Bomberman.lifes+=1
					mazeRender[Bomberman.posX][Bomberman.posY+1][1] = 0
				if mazeRender[Bomberman.posX][Bomberman.posY+1][1] == 4:
					Bomberman.bombCount+=1
					mazeRender[Bomberman.posX][Bomberman.posY+1][1] = 0
				if mazeRender[Bomberman.posX][Bomberman.posY+1][1] == 5:
					Bomberman.bombRange+=1
					mazeRender[Bomberman.posX][Bomberman.posY+1][1] = 0
				index = 0
				for npc in NPCs:
					#Pathfinding
					if npc.level == 1 and npc.estado == 1:
						if npc.iaType == 1: 
							NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
							
						elif npc.iaType == 2:
							npc.playerPos[1]+=1
							NPCmov[index] = npc.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH],Bomberman.getPos())
							
						elif npc.iaType == 3:
							NPCmov[index] = npc.areaProtecting(Bomberman.getPos(),mazeRender)
							
					elif npc.level == 2 and npc.estado == 1:
						NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
						detect = npc.bombDetect(Bombs,mazeRender)
						if detect[0]:
							NPCmov[index] = npc.bombAvoid(mazeRender,detect[1],detect[2],detect[3])
					index +=1

		if keys[pygame.K_SPACE]:
			if mazeRender[Bomberman.posX][Bomberman.posY][1] == 0:
				if Bomberman.bombCount > 0:
					mazeRender[Bomberman.posX][Bomberman.posY][1] = 1
					Bombs.append(Bomb(Bomberman.posX,Bomberman.posY,Bomberman.bombRange,-1))
					Bomberman.bombCount -= 1
					index = 0
					for npc in NPCs:
						#Pathfinding
						if npc.level == 1 and npc.estado == 1:
							if npc.iaType == 1: 
								NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
								
							elif npc.iaType == 2:
								NPCmov[index] = npc.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH],Bomberman.getPos())
								
							elif npc.iaType == 3:
								NPCmov[index] = npc.areaProtecting(Bomberman.getPos(),mazeRender)
								
						elif npc.level == 2 and npc.estado == 1:
							NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
							
							detect = npc.bombDetect(Bombs,mazeRender)
							if detect[0]:
								NPCmov[index] = npc.bombAvoid(mazeRender,detect[1],detect[2],detect[3])
						index +=1
					
		#Main movement handler end
		#NPC movement
		index = 0
		for npc in NPCs:
			#Pathfinding
			if npc.level == 1 and npc.estado == 1:
				if npc.iaType == 1: 
					NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
					
				elif npc.iaType == 2:
					NPCmov[index] = npc.pathclosing(Bomberman.direct,mazeRender,[mazeW,mazeH],Bomberman.getPos())
					
				elif npc.iaType == 3:
					NPCmov[index] = npc.areaProtecting(Bomberman.getPos(),mazeRender)
			
			elif npc.level == 2 and npc.estado == 1:
				NPCmov[index] = npc.pathfinding(Bomberman.getPos(),mazeRender)
				detect = npc.bombDetect(Bombs,mazeRender)
				
				if detect[0]:
					NPCmov[index] = npc.bombAvoid(mazeRender,detect[1],detect[2],detect[3])
			index +=1
		if movementDelay == 0:
			i = 0
			while i < NumNPC:
				if NPCmov[i] != []:
					direction = NPCmov[i][0]
					if NPCs[i].level == 1 and NPCs[i].estado == 1:
						if direction == 0:
							if (mazeRender[NPCs[i].posX][NPCs[i].posY-1][0] == 0 or mazeRender[NPCs[i].posX][NPCs[i].posY-1][0] == 1) and mazeRender[NPCs[i].posX][NPCs[i].posY-1][1] != 1:
								mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
								mazeRender[NPCs[i].posX][NPCs[i].posY-1][0] = i+2
								NPCs[i].posY -=1
								NPCs[i].direct = 0
						if direction == 2:
							if (mazeRender[NPCs[i].posX-1][NPCs[i].posY][0] == 0 or mazeRender[NPCs[i].posX-1][NPCs[i].posY][0] == 1) and mazeRender[NPCs[i].posX-1][NPCs[i].posY][1] != 1:
								mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
								mazeRender[NPCs[i].posX-1][NPCs[i].posY][0] = i+2
								NPCs[i].posX -=1
								NPCs[i].direct = 3
						if direction == 1:
							if (mazeRender[NPCs[i].posX][NPCs[i].posY+1][0] == 0 or mazeRender[NPCs[i].posX][NPCs[i].posY+1][0] == 1) and mazeRender[NPCs[i].posX][NPCs[i].posY+1][1] != 1:
								mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
								mazeRender[NPCs[i].posX][NPCs[i].posY+1][0] = i+2
								NPCs[i].posY +=1
								NPCs[i].direct = 2
						if direction == 3:
							if (mazeRender[NPCs[i].posX+1][NPCs[i].posY][0] == 0 or mazeRender[NPCs[i].posX+1][NPCs[i].posY][0] == 1) and mazeRender[NPCs[i].posX+1][NPCs[i].posY][1] != 1:
								mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
								mazeRender[NPCs[i].posX+1][NPCs[i].posY][0] = i+2
								NPCs[i].posX +=1
								NPCs[i].direct = 1

					if NPCs[i].level == 2 and NPCs[i].estado == 1:
						if direction == 0:
							if mazeRender[NPCs[i].posX][NPCs[i].posY-1][0] == 0 and mazeRender[NPCs[i].posX][NPCs[i].posY-1][1] != 1:
								mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
								mazeRender[NPCs[i].posX][NPCs[i].posY-1][0] = i+2
								NPCs[i].posY -=1
								NPCs[i].direct = 0
							elif mazeRender[NPCs[i].posX][NPCs[i].posY-1][0] == 5 or mazeRender[NPCs[i].posX][NPCs[i].posY-1][0] == 1:
								if NPCs[i].bombCount > 0:
									mazeRender[NPCs[i].posX][NPCs[i].posY][1] = 1
									Bombs.append(Bomb(NPCs[i].posX,NPCs[i].posY,NPCs[i].bombRange,NPCs[i].id))
									NPCs[i].bombCount-=1
									index = 0
									for npc in NPCs:
										#Pathfinding
										NPCmov[index] = npc.pathfinding(NPCs[i].getPos(),mazeRender)
										detect = npc.bombDetect(Bombs,mazeRender)
										if detect[0]:
											NPCmov[index] = npc.bombAvoid(mazeRender,detect[1],detect[2],detect[3])
										index +=1
						if direction == 2:
							if mazeRender[NPCs[i].posX-1][NPCs[i].posY][0] == 0  and mazeRender[NPCs[i].posX-1][NPCs[i].posY][1] != 1:
								mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
								mazeRender[NPCs[i].posX-1][NPCs[i].posY][0] = i+2
								NPCs[i].posX -=1
								NPCs[i].direct = 3
							elif mazeRender[NPCs[i].posX-1][NPCs[i].posY][0] == 5 or mazeRender[NPCs[i].posX-1][NPCs[i].posY][0] == 1:
								if NPCs[i].bombCount > 0:
									mazeRender[NPCs[i].posX][NPCs[i].posY][1] = 1
									Bombs.append(Bomb(NPCs[i].posX,NPCs[i].posY,NPCs[i].bombRange,NPCs[i].id))
									NPCs[i].bombCount-=1
									index = 0
									for npc in NPCs:
										#Pathfinding
										NPCmov[index] = npc.pathfinding(NPCs[i].getPos(),mazeRender)
										detect = npc.bombDetect(Bombs,mazeRender)
										if detect[0]:
											NPCmov[index] = npc.bombAvoid(mazeRender,detect[1],detect[2],detect[3])
										index +=1
						if direction == 1:
							if mazeRender[NPCs[i].posX][NPCs[i].posY+1][0] == 0  and mazeRender[NPCs[i].posX][NPCs[i].posY+1][1] != 1:
								mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
								mazeRender[NPCs[i].posX][NPCs[i].posY+1][0] = i+2
								NPCs[i].posY +=1
								NPCs[i].direct = 2
							elif mazeRender[NPCs[i].posX][NPCs[i].posY+1][0] == 5 or mazeRender[NPCs[i].posX][NPCs[i].posY+1][0] == 1:
								if NPCs[i].bombCount > 0:
									mazeRender[NPCs[i].posX][NPCs[i].posY][1] = 1
									Bombs.append(Bomb(NPCs[i].posX,NPCs[i].posY,NPCs[i].bombRange,NPCs[i].id))
									NPCs[i].bombCount-=1
									index = 0
									for npc in NPCs:
										#Pathfinding
										NPCmov[index] = npc.pathfinding(NPCs[i].getPos(),mazeRender)
										detect = npc.bombDetect(Bombs,mazeRender)
										if detect[0]:
											NPCmov[index] = npc.bombAvoid(mazeRender,detect[1],detect[2],detect[3])
										index +=1
						if direction == 3:
							if mazeRender[NPCs[i].posX+1][NPCs[i].posY][0] == 0  and mazeRender[NPCs[i].posX+1][NPCs[i].posY][1] != 1:
								mazeRender[NPCs[i].posX][NPCs[i].posY][0] = 0
								mazeRender[NPCs[i].posX+1][NPCs[i].posY][0] = i+2
								NPCs[i].posX +=1
								NPCs[i].direct = 1
							elif mazeRender[NPCs[i].posX+1][NPCs[i].posY][0] == 5 or mazeRender[NPCs[i].posX+1][NPCs[i].posY][0] == 1:
								if NPCs[i].bombCount > 0:
									mazeRender[NPCs[i].posX][NPCs[i].posY][1] = 1
									Bombs.append(Bomb(NPCs[i].posX,NPCs[i].posY,NPCs[i].bombRange,NPCs[i].id))
									NPCs[i].bombCount-=1
									index = 0
									for npc in NPCs:
										#Pathfinding
										NPCmov[index] = npc.pathfinding(NPCs[i].getPos(),mazeRender)
										detect = npc.bombDetect(Bombs,mazeRender)
										if detect[0]:
											NPCmov[index] = npc.bombAvoid(mazeRender,detect[1],detect[2],detect[3])
										index +=1
					NPCmov[i].pop(0)
				i+=1
			movementDelay = 3
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
					pygame.draw.rect(window,(10,105,30),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
				if mazeRender[i][j][0] == 4: 
					#Represents player 4. Yellow
					values = NPCs[2].renderValues()
					pygame.draw.rect(window,(255,255,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
				if mazeRender[i][j][0] == 5: 
					#represents breackable wall, brown
					pygame.draw.rect(window,(180,180,180),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
				if mazeRender[i][j][0] == 6: 
					#Represents unbreackable wall, gray
					pygame.draw.rect(window,(128,128,128),((i)*blocksW,(j)*blocksH,blocksW,blocksH))
				if mazeRender[i][j] == [0,3]: 
					#Represents life Power up
					window.blit(imgLife, pygame.rect.Rect((i)*blocksW,(j)*blocksH,blocksW,blocksH))
				if mazeRender[i][j] == [0,4]: 
					#Represents bomb increment
					window.blit(imgBomb, pygame.rect.Rect((i)*blocksW,(j)*blocksH,blocksW,blocksH))
				if mazeRender[i][j] == [0,5]: 
					#Represents bomb range increment
					window.blit(imgFire, pygame.rect.Rect((i)*blocksW,(j)*blocksH,blocksW,blocksH))
				j+=1
			i+=1
		#re render player and NPCs
		for i in range(playerCant):
			if i == 0:
				values = Bomberman.renderValues()
				pygame.draw.rect(window,(0,0,255),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
			if i == 1:
				if NPCs[0].estado == 1:
					values = NPCs[0].renderValues()
					pygame.draw.rect(window,(255,0,0),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
			if i == 2:
				if NPCs[1].estado == 1:
					values = NPCs[1].renderValues()
					pygame.draw.rect(window,(10,105,30),(((values[0])*blocksW)+4,((values[1])*blocksH)+4,values[2],values[3]))
			if i == 3:
				if NPCs[2].estado == 1:
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
				posible = [True,True,True,True]
				for j in range(rangeBomb):
					if Bombs[i].posX+j+1 < mazeW and posible[0]:
						if mazeRender[Bombs[i].posX+j+1][Bombs[i].posY][0] != 6:
							if mazeRender[Bombs[i].posX+j+1][Bombs[i].posY][0] == 5:
								mazeRender[Bombs[i].posX+j+1][Bombs[i].posY][0] = 0
								posible[0] = False
							if mazeRender[Bombs[i].posX+j+1][Bombs[i].posY][1] == 0:
								mazeRender[Bombs[i].posX+j+1][Bombs[i].posY][1] = 2
								Explosions.append(Explosion(Bombs[i].posX+j+1,Bombs[i].posY))
						else:
							posible[0] = False
					if Bombs[i].posY-(j+1) >= 0 and posible[1]:
						if mazeRender[Bombs[i].posX][Bombs[i].posY-(j+1)][0] != 6:
							if mazeRender[Bombs[i].posX][Bombs[i].posY-(j+1)][0] == 5:
								mazeRender[Bombs[i].posX][Bombs[i].posY-(j+1)][0] = 0
								posible[1] = False
							if mazeRender[Bombs[i].posX][Bombs[i].posY-(j+1)][1] == 0:
								mazeRender[Bombs[i].posX][Bombs[i].posY-(j+1)][1] = 2
								Explosions.append(Explosion(Bombs[i].posX,Bombs[i].posY-(j+1)))
						else:
							posible[1] = False
					if Bombs[i].posX-(j+1) >= 0 and posible[2]:
						if mazeRender[Bombs[i].posX-(j+1)][Bombs[i].posY][0] != 6:
							if mazeRender[Bombs[i].posX-(j+1)][Bombs[i].posY][0] == 5:
								mazeRender[Bombs[i].posX-(j+1)][Bombs[i].posY][0] = 0
								posible[2] = False
							if mazeRender[Bombs[i].posX-(j+1)][Bombs[i].posY][1] == 0:
								mazeRender[Bombs[i].posX-(j+1)][Bombs[i].posY][1] = 2
								Explosions.append(Explosion(Bombs[i].posX-(j+1),Bombs[i].posY))
						else:
							posible[2] = False

					if Bombs[i].posY+j+1 < mazeH and posible[3]:
						if mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][0] != 6:
							if mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][0] == 5:
								mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][0] = 0
								posible[3] = False
							if mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][1] == 0:
								mazeRender[Bombs[i].posX][Bombs[i].posY+j+1][1] = 2
								Explosions.append(Explosion(Bombs[i].posX,Bombs[i].posY+j+1))
						else:
							posible[3] = False
				if Bombs[i].id == -1:
					Bomberman.bombCount += 1
				index = 0
				for npc in NPCs:
					if npc.id == Bombs[i].id:
						npc.bombCount+=1
				del Bombs[i]
				
			i-=1


		i = len(Explosions)-1
		while i >= 0:
			Explosions[i].decreaseTime()
			if Explosions[i].ended():
				mazeRender[Explosions[i].posX][Explosions[i].posY][1] = 0
				del Explosions[i]
			else:
				for npc in NPCs:
					if ((npc.posX,npc.posY) == (Explosions[i].posX,Explosions[i].posY)) and npc.estado == 1:
						enemyDeleted+=1
						mazeRender[npc.posX][npc.posY][0] = 0
						npc.muerte()
				if ((Bomberman.posX,Bomberman.posY) == (Explosions[i].posX,Explosions[i].posY)):
					Bomberman.lifes-=1
					if Bomberman.lifes == 0:
						decision = menuPerdida()
						if decision == 1:
							nivel = False
						else:
							mainLoop = False
							nivel = False
						pygame.display.quit()
					else:
						Bomberman.realocate(mazeRender)
						mazeRender[playerPos[0]][playerPos[1]][0] = 0
						playerPos = Bomberman.getPos()
			i-=1
		#ENd handling bomb explosions

		movementDelay-=1
		gameTime-=100
		if gameTime <= 0:
			gameTime = 0
			if endDrop == 0:
				returnValues = mainMaze.endingMaze(side,mazeRender,times)
				side = returnValues[2]
				if mazeRender[returnValues[0]][returnValues[1]][0] == 1:
					Bomberman.lifes = 0
					decision = menuPerdida()
					if decision == 1:
						nivel = False
					else:
						mainLoop = False
						nivel = False
					pygame.display.quit()
				elif mazeRender[returnValues[0]][returnValues[1]][0] == 2 or mazeRender[returnValues[0]][returnValues[1]][0] == 3 or mazeRender[returnValues[0]][returnValues[1]][0] == 4:
					enemyDeleted+=1
					for i in NPCs:
						if i.posX == returnValues[0] and i.posY == returnValues[1]  and npc.estado == 1:
							i.muerte()
				mazeRender[returnValues[0]][returnValues[1]][0] = 6
				times = returnValues[3]
			else:
				endDrop-= 100
		if endDrop < 0:
			endDrop = 200
		#Check life status
		for npc in NPCs:
			if npc.level == 1 and npc.estado == 1:
				if ((npc.posX,npc.posY) == (playerPos[0],playerPos[1])):
					Bomberman.lifes-=1
					if Bomberman.lifes == 0:
						decision = menuPerdida()
						if decision == 1:
							nivel = False
						else:
							mainLoop = False
							nivel = False
						pygame.display.quit()
					else:
						Bomberman.realocate(mazeRender)
						mazeRender[playerPos[0]][playerPos[1]] = [0,0]
						playerPos = Bomberman.getPos()
		#end check life status
		#Check victoria
		if NumNPC - enemyDeleted == 0:
			Victoria()
			nivel = False
		#End check victoria
		if nivel == True:
			playerPos = Bomberman.getPos()
			pygame.draw.rect(window,(0,0,0),(700,0,300,700)) #Refreshing status bar
			timeLeft = myfont.render("Time left: "+str(gameTime/1000), False, (255, 255, 255))
			window.blit(timeLeft,(750,5))
			lifesLeft = myfont.render("Lifes left: "+str(Bomberman.lifes), False, (255, 255, 255))
			window.blit(lifesLeft,(750,45))
			window.blit(dificulty,(750,125))
			enemyLeft = myfont.render("Enemy left: "+str(NumNPC - enemyDeleted), False, (255, 255, 255))
			window.blit(enemyLeft,(750,85))
			bombAmount = myfont.render("Aviable Bombs: "+str(Bomberman.bombCount), False, (255, 255, 255))
			window.blit(bombAmount,(750,165))
			bombRangeCover = myfont.render("Bomb Range: "+str(Bomberman.bombRange), False, (255, 255, 255))
			window.blit(bombRangeCover,(750,205))
			pygame.display.update()
			pygame.time.delay(200)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					nivel = False
					del mainMaze
					del Bomberman
					for i in NPCs:
						del i
					pygame.display.quit()
		else:
			del mainMaze
			del Bomberman
			for i in NPCs:
				del i

pygame.quit()