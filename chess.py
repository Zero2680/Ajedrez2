from random import*
class GameState():
	def __init__(self):
		#b = black, w = white
		self.tablero = [
			["bb", "be", "bm", "bQ", "bK", "bh", "bf", "bg"],
			["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
			["wg", "wf", "wh", "wQ", "wK", "wm", "we", "wb"],
		]
		self.whiteToMove = True
		self.moveLog = []
		self.finish = False
		self.action = False
		self.cooldown_wf = 0
		self.cooldown_bf = 0
		self.cooldown_wg = 0
		self.cooldown_bg = 0
		self.cooldown_wh = 0
		self.cooldown_bh = 0
		self.cooldown_wm = 0
		self.cooldown_bm = 0
		self.cooldown_we = 0
		self.w_shields = 0
		self.cooldown_be = 0
		self.b_shields = 0
		self.cooldown_wb = 4
		self.cooldown_bb = 4
		self.cooldown_wc = 4
		self.cooldown_bc = 4
		self.white_wins = False
		self.black_wins = False

	def makeMove(self, move):
		self.tablero[move.startFila][move.startColumna] = "--"
		self.tablero[move.endFila][move.endColumna] = move.pieza_movida
		self.moveLog.append(move) #almacena los movimientos
		pieza = move.pieza_movida[1]
		if self.whiteToMove: #turno blancas
			if pieza == 'p':
				if move.endFila == 0:
					self.transformPawn(move.endFila, move.endColumna)
			elif pieza == 'f':
				if self.cooldown_wf == 0:
					self.killFrancotirador(move.endFila, move.endColumna)
					if self.action == True:
						self.cooldown_wf = 1
				else:
					self.cooldown_wf = self.cooldown_wf - 1
			elif pieza == 'g':
				if self.cooldown_wg == 0:
					self.catchGancho(move.endFila, move.endColumna)
					if self.action == True:
						self.cooldown_wg = 1
				else:
					self.cooldown_wg = self.cooldown_wg - 1
			elif pieza == 'h':
				if self.cooldown_wh == 0:
					self.freezeHielo(move.endFila, move.endColumna)
					self.cooldown_wh = 1
				else:
					self.cooldown_wh = self.cooldown_wh - 1
			elif pieza == 'm':
				if self.cooldown_wm == 0:
					self.teleportMago(move.endFila, move.endColumna)
					self.cooldown_wm = 1
				else:
					self.cooldown_wm = self.cooldown_wm - 1
			elif pieza == 'e':
				if self.cooldown_we != 0:
					self.cooldown_we = self.cooldown_we - 1
				else:
					self.shieldEscudo(move.endFila, move.endColumna)
			elif pieza == 'b':
				if self.cooldown_wb == 0:
					self.explosionBomba(move.endFila, move.endColumna)
				else:
					self.cooldown_wb = self.cooldown_wb - 1
		else: #turno negras
			if pieza == 'p':
				if move.endFila == 7:
					self.transformPawn(move.endFila, move.endColumna)
			elif pieza == 'f':
				if self.cooldown_bf == 0:
					self.killFrancotirador(move.endFila, move.endColumna)
					if self.action == True:
						self.cooldown_bf = 1
				else:
					self.cooldown_bf = self.cooldown_bf - 1
			elif pieza == 'g':
				if self.cooldown_bg == 0:
					self.catchGancho(move.endFila, move.endColumna)
					if self.action == True:
						self.cooldown_bg = 1
				else:
					self.cooldown_bg = self.cooldown_bg - 1
			elif pieza == 'h':
				if self.cooldown_bh == 0:
					self.freezeHielo(move.endFila, move.endColumna)
					self.cooldown_bh = 1
				else:
					self.cooldown_bh = self.cooldown_bh - 1
			elif pieza == 'm':
				if self.cooldown_bm == 0:
					self.teleportMago(move.endFila, move.endColumna)
					self.cooldown_bm = 1
				else:
					self.cooldown_bm = self.cooldown_bm - 1
			elif pieza == 'e':
				if self.cooldown_be != 0:
					self.cooldown_be = self.cooldown_be - 1
				else:
					self.shieldEscudo(move.endFila, move.endColumna)
			elif pieza == 'b':
				if self.cooldown_bb == 0:
					self.explosionBomba(move.endFila, move.endColumna)
				else:
					self.cooldown_bb = self.cooldown_bb - 1
		self.action = False
		self.whiteToMove = not self.whiteToMove #cambia el turno
	
	def undoMove(self):
		if len(self.moveLog) != 0:
			move = self.moveLog.pop() #pop selecciona el elmento y lo elimina
			self.tablero[move.startFila][move.startColumna] = move.pieza_movida
			self.tablero[move.endFila][move.endColumna] = move.pieza_comida
			self.whiteToMove = not self.whiteToMove
	
	def getValidMoves(self): #movimientos posibles y que no dejan en jaque mate al propio rey
		return self.getAllPossibleMoves()
	
	def getAllPossibleMoves(self): #todos los posibles movimientos
		moves = []
		for f in range(len(self.tablero)):
			for c in range(len(self.tablero[f])):
				turn = self.tablero[f][c][0] #nos devuelve w (white) o b (black)
				if (turn == "w" and self.whiteToMove == True) or (turn == "b" and self.whiteToMove == False):
					pieza = self.tablero[f][c][1]
					if self.white_wins == True or self.black_wins == True:
						self.finish = True
					elif len(self.tablero[f][c]) != 2: #si la pieza está congelada
						self.unfreezeHielo(f, c)
					elif pieza == "p": #si la pieza es un peón
						self.getPawnMoves(f, c, moves)
					elif pieza == "K": #si la pieza es un rey
						self.getKingMoves(f, c, moves)
					elif pieza == "Q": #si la pieza es una reina
						self.getQueenMoves(f, c, moves)
					elif pieza == 'f': #si la pieza es un francotirador
						self.getFrancotiradorMoves(f, c, moves)
					elif pieza == 'g': #si la pieza es un gancho
						self.getGanchoMoves(f, c, moves)
					elif pieza == 'h': #si la pieza es un hielo
						self.getHieloMoves(f, c, moves)
					elif pieza == 'm': #si la pieza es un mago
						self.getMagoMoves(f, c, moves)
					elif pieza == 'e': #si la pieza es un escudo
						self.getEscudoMoves(f, c, moves)
						if self.whiteToMove: 
							if self.breakShield(f, c) == True: #si rompen un escudo blanco
								self.cooldown_we = 2
						else: 
							if self.breakShield(f, c) == True: #si rompen un escudo negro
								self.cooldown_be = 2
					elif pieza == 'b': #si la pieza es una bomba
						self.getBombaMoves(f, c, moves)
					self.kingAlive(f, c)
		return moves
	
	def getPawnMoves(self, f, c, moves):
		if self.whiteToMove: #movimiento peones blancos
			if self.tablero[f-1][c] == "--" or self.tablero[f-1][c] == "ws": #no hay pieza en el cuadrado de delante
				moves.append(Move((f,c), (f-1, c), self.tablero))
				if f == 6 and self.tablero[f-2][c] == "--" or self.tablero[f-1][c] == "ws": #no hay pieza dos cuadrados adelante
					moves.append(Move((f,c), (f-2, c), self.tablero))
			if c-1 >= 0: #capturar hacia la izquierda
				if self.tablero[f-1][c-1][0] == 'b': #hay enemigo
					 moves.append(Move((f,c), (f-1, c-1), self.tablero))
			if c+1 <= 7: #capturar hacia la derecha
				if self.tablero[f-1][c+1][0] == 'b': #hay enemigo
					moves.append(Move((f,c), (f-1, c+1), self.tablero))
		else: #movimiento peones negros
			if self.tablero[f+1][c] == "--" or self.tablero[f+1][c] == "bs": #no hay pieza en el cuadrado de delante
				moves.append(Move((f,c), (f+1, c), self.tablero))
				if f == 1 and self.tablero[f+2][c] == "--" or self.tablero[f-1][c] == "bs": #no hay pieza dos cuadrados adelante
					moves.append(Move((f,c), (f+2, c), self.tablero))
			if c-1 >= 0: #capturar hacia la izquierda
				if self.tablero[f+1][c-1][0] == 'w': #hay enemigo
					 moves.append(Move((f,c), (f+1, c-1), self.tablero))
			if c+1 <= 7: #capturar hacia la derecha
				if self.tablero[f+1][c+1][0] == 'w': #hay enemigo
					moves.append(Move((f,c), (f+1, c+1), self.tablero))
		return moves

	def transformPawn(self, f, c):
		if self.whiteToMove:
			for i in range(1000):
				transformation = int((random()*10)//1)
				if 0 < transformation <= 8:
					if transformation == 1:
						self.tablero[f][c] = 'wQ'
					elif transformation == 3:
						self.tablero[f][c] = 'wf'
					elif transformation == 4:
						self.tablero[f][c] = 'wb'
					elif transformation == 5:
						self.tablero[f][c] = 'wh'
					elif transformation == 6:
						self.tablero[f][c] = 'wg'
					elif transformation == 7:
						self.tablero[f][c] = 'wm'
					elif transformation == 8:
						self.tablero[f][c] = 'we'
		else:
			for i in range(1000):
				transformation = int((random()*10)//1)
				if 0 < transformation <= 8:
					if transformation == 1:
						self.tablero[f][c] = 'bQ'
					elif transformation == 3:
						self.tablero[f][c] = 'bf'
					elif transformation == 4:
						self.tablero[f][c] = 'bb'
					elif transformation == 5:
						self.tablero[f][c] = 'bh'
					elif transformation == 6:
						self.tablero[f][c] = 'bg'
					elif transformation == 7:
						self.tablero[f][c] = 'bm'
					elif transformation == 8:
						self.tablero[f][c] = 'be'

	def getQueenMoves(self, f, c, moves):
		direccion = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
		enemyColor = 'b' if self.whiteToMove else 'w' #color enemigo
		for d in direccion:
			for i in range(1,8):
				endFila = f + d[0] * i
				endColumna = c + d[1] * i
				if 0 <= endFila < 8 and 0 <= endColumna < 8:
					endPieza = self.tablero[endFila][endColumna]
					if endPieza == '--' or (endPieza[0] != enemyColor and endPieza[1] == 's'): #casilla en vacía
						moves.append(Move((f,c), (endFila, endColumna), self.tablero))
					elif endPieza[0] == enemyColor: #pieza enemiga
						moves.append(Move((f,c), (endFila, endColumna), self.tablero))
						break
					else: #pieza aliada
						break
				else: #se sale del tablero
					break

	def getKingMoves(self, f, c, moves):
		kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1),(0, 1), (1, -1), (1, 1), (1, 0))
		enemyColor = 'b' if self.whiteToMove else 'w' #color enemigo
		for i in range(8):
			endFila = f + kingMoves[i][0]
			endColumna = c + kingMoves[i][1]
			if 0 <= endFila < 8 and 0 <= endColumna < 8:
				endPieza = self.tablero[endFila][endColumna]
				if endPieza == '--' or (endPieza[0] != enemyColor and endPieza[1] == 's'):
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
				elif endPieza[0] == enemyColor:
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
	
	def kingAlive(self, f, c):
		wK_alive = 0
		bK_alive = 0
		if self.whiteToMove:
			for f in range(len(self.tablero)):
					for c in range(len(self.tablero[f])):
						if self.tablero[f][c] == 'wK' or self.tablero[f][c] == 'wK_cong':
							wK_alive = 1
			if wK_alive == 1:
				self.black_wins = False
			else:
				self.black_wins = True
		else:
			for f in range(len(self.tablero)):
					for c in range(len(self.tablero[f])):
						if self.tablero[f][c] == 'bK' or self.tablero[f][c] == 'bK_cong':
							bK_alive = 1
			if bK_alive == 0:
				self.white_wins = True
			else:
				self.white_wins = False
	
	def getFrancotiradorMoves(self, f, c, moves):
		francoMoves = ((1, 0),(-1, 0), (0, -1),(0, 1))
		enemyColor = 'b' if self.whiteToMove else 'w' #color enemigo
		for i in range(4):
			endFila = f + francoMoves[i][0]
			endColumna = c + francoMoves[i][1]
			if 0 <= endFila < 8 and 0 <= endColumna < 8:
				endPieza = self.tablero[endFila][endColumna]
				if endPieza == '--' or endPieza[0] != enemyColor:
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
				elif endPieza[0] == enemyColor:
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))

	def killFrancotirador(self, f, c):
		if self.whiteToMove:
			for i in range(f):
				endFila = f - i - 1
				endColumna = c
				if self.tablero[endFila][endColumna][0] == 'b': #hay enemigo
					self.tablero[endFila][endColumna] = '--'
					self.action = True
					break
				elif self.tablero[endFila][endColumna][0] == 'w': #hay aliado
					break
		else:
			for i in range(7-f):
				endFila = f + i + 1
				endColumna = c
				if self.tablero[endFila][endColumna][0] == 'w': #hay enemigo
					self.tablero[endFila][endColumna] = '--'
					self.action = True
					break
				elif self.tablero[endFila][endColumna][0] == 'b': #hay aliado
					break

	def getGanchoMoves(self, f, c, moves):
		ganchoMoves = ((1, 0),(-1, 0), (0, -1),(0, 1))
		enemyColor = 'b' if self.whiteToMove else 'w' #color enemigo
		for i in range(4):
			endFila = f + ganchoMoves[i][0]
			endColumna = c + ganchoMoves[i][1]
			if 0 <= endFila < 8 and 0 <= endColumna < 8:
				endPieza = self.tablero[endFila][endColumna]
				if endPieza == '--' or (endPieza[0] != enemyColor and endPieza[1] == 's'):
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
				elif endPieza[0] == enemyColor:
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
	
	def catchGancho(self, f, c):
		if self.whiteToMove:
			for i in range(f):
				endFila = f - i - 1
				endColumna = c
				if self.tablero[endFila][endColumna] == 'bs': #hay escudo
					break
				elif self.tablero[endFila][endColumna][0] == 'b': #hay enemigo
					self.tablero[f-1][c] = self.tablero[endFila][endColumna]
					self.tablero[endFila][endColumna] = '--'
					self.action = True
					break
				elif self.tablero[endFila][endColumna][0] == 'w': #hay aliado
						break
		else:
			for i in range(7-f):
				endFila = f + i + 1
				endColumna = c
				if self.tablero[endFila][endColumna] == 'ws': #hay escudo
					break
				elif self.tablero[endFila][endColumna][0] == 'w': #hay enemigo
					self.tablero[f+1][c] = self.tablero[endFila][endColumna]
					self.tablero[endFila][endColumna] = '--'
					self.action = True
					break
				elif self.tablero[endFila][endColumna][0] == 'b': #hay aliado
						break

	def getHieloMoves(self, f, c, moves):
		hieloMoves = ((1, 0),(-1, 0), (0, -1),(0, 1))
		enemyColor = 'b' if self.whiteToMove else 'w' #color enemigo
		for i in range(4):
			endFila = f + hieloMoves[i][0]
			endColumna = c + hieloMoves[i][1]
			if 0 <= endFila < 8 and 0 <= endColumna < 8:
				endPieza = self.tablero[endFila][endColumna]
				if endPieza == '--' or (endPieza[0] != enemyColor and endPieza[1] == 's'):
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
				elif endPieza[0] == enemyColor:
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
	
	def freezeHielo(self, f, c):
		piezasEnemigas = 0
		position = 0
		if self.whiteToMove:
			for f in range(8):
				for c in range(8):
					pieza = self.tablero[f][c]
					if pieza[0] == "b" and pieza[1] != 's':
						piezasEnemigas += 1
			for i in range(1000):
				b_cong = int((random()*100)//1)
				if 0 < b_cong <= piezasEnemigas:
					break
			for f in range(8):
				for c in range(8):
					pieza = self.tablero[f][c]
					if pieza[0] == "b" and pieza[1] != 's':
						position += 1
						if position == b_cong:
							self.tablero[f][c] = self.tablero[f][c] + '_cong'
							break
		else:
			for f in range(8):
				for c in range(8):
					pieza = self.tablero[f][c]
					if pieza[0] == "w" and pieza[1] != 's':
						piezasEnemigas += 1
			for i in range(1000):
				w_cong = int((random()*100)//1)
				if 0 < w_cong <= piezasEnemigas:
					break
			for f in range(8):
				for c in range(8):
					pieza = self.tablero[f][c]
					if pieza[0] == "w" and pieza[1] != 's':
						position += 1
						if position == w_cong:
							self.tablero[f][c] = self.tablero[f][c] + '_cong'

	def unfreezeHielo(self, f, c):
		cong = 0
		fila = f
		columna = c
		endFila = f
		endColumna = c
		if self.whiteToMove:
			for fila in range(len(self.tablero)):
				for columna in range(len(self.tablero[f])):
					if len(self.tablero[fila][columna]) != 2:
						cong = 1
						break
			if cong == 1:
				self.cooldown_wc = self.cooldown_wc - 1
				if self.cooldown_wc == 0:
					self.tablero[endFila][endColumna] = self.tablero[endFila][endColumna][0] + self.tablero[endFila][endColumna][1]
					self.cooldown_wc = 2
		else:
			for fila in range(len(self.tablero)):
				for columna in range(len(self.tablero[f])):
					if len(self.tablero[fila][columna]) != 2:
						cong = 1
						break
			if cong == 1:
				self.cooldown_bc = self.cooldown_bc - 1
				if self.cooldown_bc == 0:
					self.tablero[endFila][endColumna] = self.tablero[endFila][endColumna][0] + self.tablero[endFila][endColumna][1]
					self.cooldown_bc = 2

	def getMagoMoves(self, f, c, moves):
		magoMoves = ((1, 0),(-1, 0), (0, -1),(0, 1))
		enemyColor = 'b' if self.whiteToMove else 'w' #color enemigo
		for i in range(4):
			endFila = f + magoMoves[i][0]
			endColumna = c + magoMoves[i][1]
			if 0 <= endFila < 8 and 0 <= endColumna < 8:
				endPieza = self.tablero[endFila][endColumna]
				if endPieza == '--' or (endPieza[0] != enemyColor and endPieza[1] == 's'):
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
				elif endPieza[0] == enemyColor:
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
			
	def teleportMago(self, f, c):
		piezasEnemigas = 0
		position1 = 0
		position2 = 0
		if self.whiteToMove:
			for i in range(1000):
				for f in range(8):
					for c in range(8):
						pieza = self.tablero[f][c]
						if pieza[0] == "b" and pieza[1] != 's':
							piezasEnemigas += 1
				for i in range(1000):
					pieza1 = int((random()*100)//1)
					pieza2 = int((random()*100)//1)
					if 0 < pieza1 <= piezasEnemigas and 0 < pieza2 <= piezasEnemigas and pieza1 != pieza2:
						break
				for f in range(8):
					for c in range(8):
						pieza = self.tablero[f][c]
						if pieza[0] == "b" and pieza[1] != 's':
							position1 += 1
							if position1 == pieza1:
								fila1 = f
								columna1 = c
								break
				for f in range(8):
					for c in range(8):
						pieza = self.tablero[f][c]
						if pieza[0] == "b" and pieza[1] != 's':
							position2 += 1
							if position2 == pieza2:
								fila2 = f
								columna2 = c
								break
				pieza1 = self.tablero[fila1][columna1]
				pieza2 = self.tablero[fila2][columna2]
				if pieza1 != pieza2:
					self.tablero[fila1][columna1] = pieza2
					self.tablero[fila2][columna2] = pieza1
					break
		else:
			for i in range(1000):
				for f in range(8):
					for c in range(8):
						pieza = self.tablero[f][c]
						if pieza[0] == "w" and pieza[1] != 's':
							piezasEnemigas += 1
				for i in range(1000):
					pieza1 = int((random()*100)//1)
					pieza2 = int((random()*100)//1)
					if 0 < pieza1 <= piezasEnemigas and 0 < pieza2 <= piezasEnemigas and pieza1 != pieza2:
						break
				for f in range(8):
					for c in range(8):
						pieza = self.tablero[f][c]
						if pieza[0] == "w" and pieza[1] != 's':
							position1 += 1
							if position1 == pieza1:
								fila1 = f
								columna1 = c
								break
				for f in range(8):
					for c in range(8):
						pieza = self.tablero[f][c]
						if pieza[0] == "w" and pieza[1] != 's':
							position2 += 1
							if position2 == pieza2:
								fila2 = f
								columna2 = c
								break
				pieza1 = self.tablero[fila1][columna1]
				pieza2 = self.tablero[fila2][columna2]
				if pieza1 != pieza2:
					self.tablero[fila1][columna1] = pieza2
					self.tablero[fila2][columna2] = pieza1
					break
	
	def getEscudoMoves(self, f, c, moves):
		escudoMoves = ((1, 0),(-1, 0), (0, -1),(0, 1))
		enemyColor = 'b' if self.whiteToMove else 'w' #color enemigo
		for i in range(4):
			endFila = f + escudoMoves[i][0]
			endColumna = c + escudoMoves[i][1]
			if 0 <= endFila < 8 and 0 <= endColumna < 8:
				endPieza = self.tablero[endFila][endColumna]
				if endPieza == '--' or (endPieza[0] != enemyColor and endPieza[1] == 's'):
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
				elif endPieza[0] == enemyColor:
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
	
	def shieldEscudo(self, f, c):
		if self.whiteToMove:
			filaSH = f-1
			columnaSH = c+1
			for f in range(len(self.tablero)):
				for c in range(len(self.tablero[f])):
					if self.tablero[f][c] == 'ws':
						self.tablero[f][c] = '--'
						self.w_shields = 0
			for i in range(3):
				if i == 2:
					columnaSH -= 1
				else:
					columnaSH = columnaSH-i
				if self.tablero[filaSH][columnaSH] == "--":
					self.tablero[filaSH][columnaSH] = 'ws'
					self.w_shields += 1
		else:
			filaSH = f+1
			columnaSH = c+1
			for f in range(len(self.tablero)):
				for c in range(len(self.tablero[f])):
					if self.tablero[f][c] == 'bs':
						self.tablero[f][c] = '--'
						self.b_shields = 0
			for i in range(3):
				if i == 2:
					columnaSH -= 1
				else:
					columnaSH = columnaSH-i
				if self.tablero[filaSH][columnaSH] == "--":
					self.tablero[filaSH][columnaSH] = 'bs'
					self.b_shields += 1

	def breakShield(self, f, c):
		w_pieces = 0
		b_pieces = 0
		shields = 0
		if self.whiteToMove:
			filaSH = f-1
			columnaSH = c+1
			for f in range(len(self.tablero)):
					for c in range(len(self.tablero[f])):
						if self.tablero[f][c] == 'ws':
							shields += 1
			if shields != self.w_shields:
				for f in range(len(self.tablero)):
						for c in range(len(self.tablero[f])):
							if self.tablero[f][c] == 'ws':
								self.tablero[f][c] = '--'
								self.w_shields = 0
				return True
			elif shields != 0 and shields != 3:
				for i in range(3):
					if i == 2:
						columnaSH -= 1
					else:
						columnaSH = columnaSH-i
					if self.tablero[filaSH][columnaSH][0] == "b":
						b_pieces += 1
				if b_pieces == 1:
					for f in range(len(self.tablero)):
						for c in range(len(self.tablero[f])):
							if self.tablero[f][c] == 'ws':
								self.tablero[f][c] = '--'
								self.w_shields = 0
					return True
				else:
					return False
		else:
			filaSH = f+1
			columnaSH = c+1
			for f in range(len(self.tablero)):
					for c in range(len(self.tablero[f])):
						if self.tablero[f][c] == 'bs':
							shields += 1
			if shields != self.b_shields:
				for f in range(len(self.tablero)):
						for c in range(len(self.tablero[f])):
							if self.tablero[f][c] == 'bs':
								self.tablero[f][c] = '--'
								self.b_shields = 0
				return True
			elif shields != 0 and shields != 3:
				for i in range(3):
					if i == 2:
						columnaSH -= 1
					else:
						columnaSH = columnaSH-i
					if self.tablero[filaSH][columnaSH][0] == "w":
						w_pieces += 1
				if w_pieces == 1:
					for f in range(len(self.tablero)):
						for c in range(len(self.tablero[f])):
							if self.tablero[f][c] == 'bs':
								self.tablero[f][c] = '--'
								self.b_shields = 0
					return True
				else:
					return False
	
	def getBombaMoves(self, f, c, moves):
		bombaMoves = ((2, 0),(-2, 0), (0, -2),(0, 2))
		enemyColor = 'b' if self.whiteToMove else 'w' #color enemigo
		for i in range(4):
			endFila = f + bombaMoves[i][0]
			endColumna = c + bombaMoves[i][1]
			if 0 <= endFila < 8 and 0 <= endColumna < 8:
				endPieza = self.tablero[endFila][endColumna]
				if endPieza == '--' or (endPieza[0] != enemyColor and endPieza[1] == 's'):
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
				elif endPieza[0] == enemyColor:
					moves.append(Move((f,c), (endFila, endColumna), self.tablero))
	
	def explosionBomba(self, f, c):
		explosion = ((-1, -1), (-1, 0), (-1, 1), (0, -1),(0, 1), (1, -1), (1, 1), (1, 0))
		for i in range(8):
			endFila = f + explosion[i][0]
			endColumna = c + explosion[i][1]
			if 0 <= endFila < 8 and 0 <= endColumna < 8:
				self.tablero[endFila][endColumna] = '--'
		self.tablero[f][c] = '--'

class Move():
	#DICCIONARIOS PARA QUE PYGAME ENTIENDA LAS CASILLAS
	ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
	rowsToRanks = {v: k for k, v in ranksToRows.items()}
	filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
	colsToFiles = {v: k for k, v in filesToCols.items()}
	def __init__(self, startSq, endSq, tablero):
		self.startFila = startSq[0]
		self.startColumna = startSq[1]
		self.endFila = endSq[0]
		self.endColumna = endSq[1]
		self.pieza_movida = tablero[self.startFila][self.startColumna]
		self.pieza_comida = tablero[self.endFila][self.endColumna]
		self.moveID = self.startFila * 1000 + self.startColumna * 100 + self.endFila * 10 + self.endColumna #nos da una combinación de números de los movimientos
	
	def __eq__(self, other): #comprobar que dos movimientos son iguales
		if isinstance(other, Move):
			return self.moveID == other.moveID
		return False

	def getChessNotation(self):
		return self.getRankFile(self.startFila, self.startColumna) + self.getRankFile(self.endFila, self.endColumna)

	def getRankFile(self, f, c):
		return self.colsToFiles[c] + self.rowsToRanks[f]