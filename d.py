from Grid       import Grid
from PlayerAI   import PlayerAI
from ComputerAI import ComputerAI
from random     import randint
import time

defaultInitialTiles = 2
defaultProbability = 0.9
maxTile = 0
actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}


(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

class GameManager:
    def __init__(self, size = 4):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles  = defaultInitialTiles
        self.computerAI = None
        self.playerAI   = None
        self.displayer  = None
        self.over       = False
        self.maxTile = 0

    def setComputerAI(self, computerAI):
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI

    def start(self):
        for i in xrange(self.initTiles):
            self.insertRandonTile()

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
                #print "Selected Move: ", actionDic[move]

                # Validate Move
                if move != None and move >= 0 and move < 4:
                    if self.grid.canMove([move]):
                        self.grid.move(move)

                        # Update maxTile
                        self.maxTile = self.grid.getMaxTile()
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
                    #print "Invalid Computer AI Move"
                    self.over = True

            turn = 1 - turn
        print self.maxTile

    def isGameOver(self):
        #if not self.grid.canMove():
        #    print self.maxTile
        return not self.grid.canMove()

    def getMaxTile(self):
        return self.maxTile

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

    def modifyWeights(self):
        # Get weights
        free_weight = 0
        smooth_weight = 0
        mono_weight = 0
        max_weight = 0
        corner_weight = 0
        island_weight = 0

        with open('weights.txt') as f:
            content = f.read().splitlines()
            i = 0
            for line in content:
                parts = line.split(":")
                n = 0
                for part in parts:
                    if n%2 != 0:
                        if i == 0:
                            free_weight = float(part)
                        elif i == 1:
                            smooth_weight = float(part)
                        elif i == 2:
                            mono_weight = float(part)
                        elif i == 3:
                            max_weight = float(part)
                        elif i == 4:
                            corner_weight = float(part)
                        else:
                            island_weight = float(part)
                        i += 1
                    n += 1

        # Get iteration
        with open('iteration.txt') as f:
            content = f.read().splitlines()

        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        possibilities = 0

        i = 0
        for line in content:
            if i == 0:
                a = float(line)
            elif i == 1:
                b = float(line)
            elif i == 2:
                c = float(line)
            elif i == 3:
                d = float(line)
            elif i == 4:
                e = float(line)
            else:
                possibilities = float(line)
            i += 1

        possibilities += 1
        change_rate = 0.2
        complete = False
        a += change_rate
        if a > 1:
            a = 0
            b += change_rate
        if b > 1:
            b = 0
            c += change_rate
        if c > 1:
            c = 0
            d += change_rate
        if d > 1:
            d = 0
            e += change_rate
        if e > 1:
            complete = True

        with open('iteration.txt', 'r+') as f:
            text = f.read()
            f.seek(0)
            f.write(str(a))
            f.write('\n')
            f.write(str(b))
            f.write('\n')
            f.write(str(c))
            f.write('\n')
            f.write(str(d))
            f.write('\n')
            f.write(str(e))
            f.write('\n')
            f.write(str(possibilities))
            f.truncate()


        with open('weights.txt', 'r+') as f:
            text = f.read()
            f.seek(0)
            f.write('free_weight:'+str((2+a)))
            f.write('\n')
            f.write('mono_weight:'+str((0+b)))
            f.write('\n')
            f.write('max_weight:'+str((0+c)))
            f.write('\n')
            f.write('corner_weight:'+str((0+d)))
            f.write('\n')
            f.write('island_weight:'+str((0+e)))
            f.truncate()

        with open('results.txt', 'r+') as f:
            text = f.read()
            f.write('\n')
            f.write('New Combination:')
            f.write('\n')
            f.write('free_weight:'+str((2+a)))
            f.write('\n')
            f.write('mono_weight:'+str((0+b)))
            f.write('\n')
            f.write('max_weight:'+str((0+c)))
            f.write('\n')
            f.write('corner_weight:'+str((0+d)))
            f.write('\n')
            f.write('island_weight:'+str((0+e)))
            f.write('\n')
            f.write('\n')
        return complete


def main():
    loop = 0
    results = []
    complete = False
    while not complete:

        gameManager = GameManager()
        playerAI    = PlayerAI()
        computerAI  = ComputerAI()

        gameManager.setPlayerAI(playerAI)
        gameManager.setComputerAI(computerAI)

        gameManager.start()
        results.append(gameManager.getMaxTile())

        loop += 1
        if loop/10 == 1:
            average = 0
            for result in results:
                #print result
                average += float(result)
            average = average/10
            with open('results.txt', 'r+') as f:
                text = f.read()
                f.write('Average Max Tile: '+str(average))
            loop = 0
            results = []
            complete = gameManager.modifyWeights()

if __name__ == '__main__':
    main()