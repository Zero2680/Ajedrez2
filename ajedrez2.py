from pygame import*
from chess import*
from random import*
screen = display.set_mode((1280, 720), FULLSCREEN) 
display.set_caption('Ajedrez 2')
encendido = True
finish = False
width = height = 720
dimensiones = 8 #8x8
sq_size = height // dimensiones
IMAGES = {}
gs = GameState()
validMoves = gs.getValidMoves() #movimientos válidos
moveMade = False #variable que permite o no hacer el movimiento
sqSelected = () #ultimo click del jugador
playerClicks= [] #lista con los dos clicks del jugador


#DIBUJAR TABLERO // f = fila, c = columna
def dibujarTablero(screen):
	colores = [Color(255,204,105), Color(126,83,0)]
	for f in range(dimensiones):
		for c in range(dimensiones):
			color = colores[((f+c) % 2)]
			draw.rect(screen, color, Rect(c*sq_size, f*sq_size, sq_size, sq_size))


#CARGAR IMAGENES
def loadImages():
	piezas = ["bf", "bg", "bh", "bm", "bb", "be", "bs", "bQ", "bK", "bp", "wf", "wg", "wh", "wm", "wb", "we", "ws", "wQ", "wK", "wp", "bf_cong", "bg_cong", "bh_cong", "bm_cong", "bb_cong", "be_cong", "bQ_cong", "bK_cong", "bp_cong", "wf_cong", "wg_cong", "wh_cong", "wm_cong", "wb_cong", "we_cong", "wQ_cong", "wK_cong", "wp_cong", "white_wins", "black_wins"]
	for pieza in piezas:
		IMAGES[pieza] = transform.scale(image.load("ajedrez2_images/" + pieza + ".png"), (90, 90))


#DIBUJAR IMAGENES
def dibujarPiezas(screen, tablero):
	for f in range(dimensiones):
		for c in range(dimensiones):
			pieza = tablero[f][c]
			if pieza != "--":
				screen.blit(IMAGES[pieza], Rect(c*sq_size, f*sq_size, sq_size, sq_size))

loadImages()

while encendido:
	if gs.finish == False:
		dibujarTablero(screen)
		dibujarPiezas(screen, gs.tablero)
		for evento in event.get():
			if evento.type==QUIT:
				encendido=False

			#PULSAR RATÓN (MOVER PIEZAS)
			elif evento.type==MOUSEBUTTONDOWN:
				location = mouse.get_pos()
				columna = location[0]//sq_size
				fila = location[1]//sq_size
				if sqSelected == (fila,columna): #click dos veces en la misma casilla
					sqSelected = ()
					playerClicks = []
				else:
					sqSelected = (fila, columna)
					playerClicks.append(sqSelected)
				if len(playerClicks) == 2:
					if gs.tablero[playerClicks[0][0]][playerClicks[0][1]] == "--": #si toca primero en una casilla en blanco (para que no desaparezca el personaje)
						sqSelected = ()
						playerClicks = []
					else:
						move = Move(playerClicks[0], playerClicks[1], gs.tablero)
						print(move.getChessNotation())
						if move in validMoves:
							gs.makeMove(move)
							moveMade = True
							sqSelected = ()
							playerClicks = []
						else:
							playerClicks = [sqSelected]
			
			#PULSAR TECLA
			elif evento.type == KEYDOWN:
				if evento.key == K_z: #pulsar z para deshacer un movimiento
					gs.undoMove()
					moveMade = True

				if evento.key == K_ESCAPE:
					quit()
					exit()

		if moveMade: #devuelve a la variable a False
			validMoves = gs.getValidMoves()
			moveMade = False
		dibujarTablero(screen)
		dibujarPiezas(screen, gs.tablero)
	elif gs.finish == True:
		if gs.white_wins == True:
			white_wins = transform.scale(image.load("ajedrez2_images/white_wins.png"), (500, 500))
			screen.blit(white_wins, (110,110))
		elif gs.black_wins == True:
			black_wins = transform.scale(image.load("ajedrez2_images/black_wins.png"), (500, 500))
			screen.blit(black_wins, (110,110))
		for evento in event.get():
			if evento.type==QUIT:
				encendido=False
			elif evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					quit()
					exit()
	display.flip()