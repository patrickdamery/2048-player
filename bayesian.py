from Grid   import Grid
from ComputerAI import ComputerAI
from PlayerAI   import PlayerAI
from Displayer  import Displayer
from random import randint
import time
import os
import sys
sys.path.append("./")
from bayes_opt import BayesianOptimization

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
0: "UP",
1: "DOWN",
2: "LEFT",
3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time Limit Before Losing
timeLimit = 0.1
allowance = 0.05

class GameManager:
	def __init__(self, size = 4):
		#self.grid = Grid(size)
		self.possibleNewTiles = [2, 4]
		self.probability = defaultProbability
		self.initTiles  = defaultInitialTiles
		self.computerAI = None
		self.playerAI   = None
		self.over   = False
		self.grid = Grid(size)

	def setComputerAI(self, computerAI):
		self.computerAI = computerAI

	def setPlayerAI(self, playerAI):
		self.playerAI = playerAI

	def updateAlarm(self, currTime):
		if currTime - self.prevTime > timeLimit + allowance:
			print 'Out of time'
			self.over = True
		else:
			while time.clock() - self.prevTime < timeLimit + allowance:
				pass

		self.prevTime = time.clock()

	def start(self):
		#for i in xrange(self.initTiles):
		#	self.insertRandonTile()

		sel_board = randint(0, 4)

		if sel_board == 0:
			self.board1(self.grid)
		elif sel_board == 1:
			self.board2(self.grid)
		elif sel_board == 2:
			self.board3(self.grid)
		elif sel_board == 3:
			self.board4(self.grid)
		else:
			self.board5(self.grid)

		# Player AI Goes First
		turn = PLAYER_TURN
		maxTile = 0

		self.prevTime = time.clock()

		while not self.isGameOver() and not self.over:
			# Copy to Ensure AI Cannot Change the Real Grid to Cheat
			gridCopy = self.grid.clone()

			move = None

			if turn == PLAYER_TURN:
				#print "Player's Turn:",
				move = self.playerAI.getMove(gridCopy)
				#print actionDic[move]

				# Validate Move
				if move != None and move >= 0 and move < 4:
					if self.grid.canMove([move]):
						self.grid.move(move)
						#self.playerAI.utility(self.grid, True)

						# Update maxTile
						maxTile = self.grid.getMaxTile()
					else:
						#print "Invalid PlayerAI Move"
						self.over = True
				else:
					#print "Invalid PlayerAI Move - 1"
					self.over = True
			else:
				#print "Computer's turn:"
				move = self.computerAI.getMove(gridCopy)

				# Validate Move
				if move and self.grid.canInsert(move):
					self.grid.setCellValue(move, self.getNewTileValue())
				else:
					print "Invalid Computer AI Move"
					self.over = True

			# Exceeding the Time Allotted for Any Turn Terminates the Game
			self.updateAlarm(time.clock())

			turn = 1 - turn

	def isGameOver(self):
		return not self.grid.canMove()

	def getNewTileValue(self):
		if randint(0,99) < 100 * self.probability:
			return self.possibleNewTiles[0]
		else:
			return self.possibleNewTiles[1];

	def insertRandonTile(self):
		tileValue = self.getNewTileValue()
		cells = self.grid.getAvailableCells()
		cell = cells[randint(0, len(cells) - 1)]
		self.grid.setCellValue(cell, tileValue)

	# Have predefined board conditions to explore games from an advanced state.
	def board1(self, grid):
		grid.map = [[2, 0, 2, 0], [4, 32, 16, 4], [2, 4, 128, 16], [128, 1024, 4, 2]]

	def board2(self, grid):
		grid.map = [[8, 8, 4, 2], [1024, 16, 64, 4], [4, 128, 16, 2], [256, 4, 0, 0]]

	def board3(self, grid):
		grid.map = [[0, 0, 4, 32], [0, 0, 0, 512], [2, 4, 8, 64], [0, 8, 32, 16]]

	def board4(self, grid):
		grid.map = [[2, 2, 4, 0], [1024, 32, 16, 0], [64, 512, 8, 8], [8, 2, 4, 2]]

	def board5(self, grid):
		grid.map = [[32, 16, 8, 0], [1024, 8, 16, 0], [8, 0, 0, 0], [4, 2, 2, 0]]

def play_game(fr, sm, mo, ma, nm, de, co):

	avgMax = 0
	loop = 0
	results = []
	while loop < 26:
		gameManager = GameManager()
		playerAI  	= PlayerAI(fr, sm, mo, ma, nm, 1, de, co)
		computerAI  = ComputerAI()

		gameManager.setPlayerAI(playerAI)
		gameManager.setComputerAI(computerAI)

		gameManager.start()
		avgMax += gameManager.grid.getMaxTile()
		results.append(gameManager.grid.getMaxTile())
		loop += 1
	#print results

	return avgMax/loop

def main():
	bo = BayesianOptimization(lambda fr, sm, mo, ma, nm, de, co: play_game(fr, sm, mo, ma, nm, de, co),
						  {'fr': (2, 6), 'sm': (-1, 1), 'mo': (0, 2),  'ma': (0, 2), 'nm': (-1, 1), 'de': (-1, 1), 'co': (-1, 1)})

	bo.explore({'fr': [5.0771664428677061], 'sm': [-0.13059762676063172], 'mo': [1.3682148714919597],
		'ma': [0.52214706278657907], 'nm': [-0.86627512983565302], 'de': [0.42238952601950097], 'co': [-0.39416823224808289]})

	bo.maximize(init_points=5, n_iter=50, kappa=0.5)

	# The output values can be accessed with self.res
	print 'RESULTS'
	print(bo.res['max'])

if __name__ == '__main__':
	main()
