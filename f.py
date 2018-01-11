"""Example of how to use this bayesian optimization package."""

import sys
sys.path.append("./")
from bayes_opt import BayesianOptimization
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

def target(x):
	return np.exp(-(x - 2)**2) + np.exp(-(x - 6)**2/10) + 1/ (x**2 + 1)

def posterior(bo, x, xmin=-2, xmax=10):
    xmin, xmax = -2, 10
    bo.gp.fit(bo.X, bo.Y)
    mu, sigma = bo.gp.predict(x, return_std=True)
    return mu, sigma

def plot_gp(bo, x, y):
    
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('Gaussian Process and Utility Function After {} Steps'.format(len(bo.X)), fontdict={'size':30})
    
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) 
    axis = plt.subplot(gs[0])
    acq = plt.subplot(gs[1])
    
    mu, sigma = posterior(bo, x)
    axis.plot(x, y, linewidth=3, label='Target')
    axis.plot(bo.X.flatten(), bo.Y, 'D', markersize=8, label=u'Observations', color='r')
    axis.plot(x, mu, '--', color='k', label='Prediction')

    axis.fill(np.concatenate([x, x[::-1]]), 
              np.concatenate([mu - 1.9600 * sigma, (mu + 1.9600 * sigma)[::-1]]),
        alpha=.6, fc='c', ec='None', label='95% confidence interval')
    
    axis.set_xlim((-2, 10))
    axis.set_ylim((None, None))
    axis.set_ylabel('f(x)', fontdict={'size':20})
    axis.set_xlabel('x', fontdict={'size':20})
    
    utility = bo.util.utility(x, bo.gp, 0)
    acq.plot(x, utility, label='Utility Function', color='purple')
    acq.plot(x[np.argmax(utility)], np.max(utility), '*', markersize=15, 
             label=u'Next Best Guess', markerfacecolor='gold', markeredgecolor='k', markeredgewidth=1)
    acq.set_xlim((-2, 10))
    acq.set_ylim((0, np.max(utility) + 0.5))
    acq.set_ylabel('Utility', fontdict={'size':20})
    acq.set_xlabel('x', fontdict={'size':20})
    
    axis.legend(loc=2, bbox_to_anchor=(1.01, 1), borderaxespad=0.)
    acq.legend(loc=2, bbox_to_anchor=(1.01, 1), borderaxespad=0.)



x = np.linspace(-2, 10, 10000).reshape(-1, 1)
y = target(x)

plt.plot(x, y)

# Lets find the maximum of a simple quadratic function of two variables
# We create the bayes_opt object and pass the function to be maximized
# together with the parameters names and their bounds.
#bo = BayesianOptimization(lambda x, y: -x ** 2 - (y - 1) ** 2 + 1,
#                          {'x': (-4, 4), 'y': (-3, 3)})
bo = BayesianOptimization(lambda x: target(x),
                          {'x': (-4, 4)})

# One of the things we can do with this object is pass points
# which we want the algorithm to probe. A dictionary with the
# parameters names and a list of values to include in the search
# must be given.
bo.explore({'x': [-1, 3]})

# Additionally, if we have any prior knowledge of the behaviour of
# the target function (even if not totally accurate) we can also
# tell that to the optimizer.
# Here we pass a dictionary with 'target' and parameter names as keys and a
# list of corresponding values
bo.initialize(
    {
        'target': [-1, -1],
        'x': [1, 1]
    }
)

# Once we are satisfied with the initialization conditions
# we let the algorithm do its magic by calling the maximize()
# method.
bo.maximize(init_points=5, n_iter=15, kappa=2)

plot_gp(bo, x, y)

# The output values can be accessed with self.res
print(bo.res['max'])

# If we are not satisfied with the current results we can pickup from
# where we left, maybe pass some more exploration points to the algorithm
# change any parameters we may choose, and the let it run again.
bo.explore({'x': [0.6]})

# Making changes to the gaussian process can impact the algorithm
# dramatically.
gp_params = {'kernel': None,
             'alpha': 1e-5}

# Run it again with different acquisition function
bo.maximize(n_iter=5, acq='ei', **gp_params)

# Finally, we take a look at the final results.
print(bo.res['max'])
print(bo.res['all'])


from random import randint
from BaseAI import BaseAI
import time
import math

actionDic = {
0: "UP",
1: "DOWN",
2: "LEFT",
3: "RIGHT"
}

time_limit = 0.1

free_weight = 0
smooth_weight = 0
mono_weight = 0
max_weight = 0
corner_weight = 0
island_weight = 0
newmax_weight = 0
complex_weight = 0 # seems good heuristic
goal_weight = 0
gameover_weight = 0 # very good heuristic
density_weight = 0


#with open('weights.txt') as f:
#    content = f.read().splitlines()

#i = 0
#for line in content:
#	parts = line.split(":")
#	n = 0
#	for part in parts:
#		if n%2 != 0:
#			if i == 0:
#				free_weight = float(part)
#			elif i == 1:
#				smooth_weight = float(part)
#			elif i == 2:
#				mono_weight = float(part)
#			elif i == 3:
#				max_weight = float(part)
#			elif i == 4:
#				corner_weight = float(part)
#			else:
#				island_weight = float(part)
#			i += 1
#		n += 1

class PlayerAI(BaseAI):

	def __init__(self, fr, sm, mo, ma, nm, go, de, co):
		self.free_weight = float(fr)
		self.smooth_weight = float(sm)
		self.mono_weight = float(mo)
		self.max_weight = float(ma)
		self.newmax_weight = float(nm)
		self.complex_weight = float(co) # seems good heuristic
		self.gameover_weight = float(go) # very good heuristic
		self.density_weight = float(de)

	def freeTiles(self, grid):
		cells = grid.getAvailableCells()
		if len(cells) > 0:
			return len(cells)
		else:
			return 0

	def complexity(self, grid):
		complexity = 0
		m = grid.map
		size = grid.size
		for row in range(0, size):
			for col in range(0, size):
				if m[row][col] != 0:
					complexity += math.log(m[row][col])/math.log(2)

		return complexity

	def goalCounter(self, grid):
		goal = 2048
		counted = 0
		m = grid.map
		size = grid.size
		for row in range(0, size):
			for col in range(0, size):
				if m[row][col] == goal:
					counted += 1
		return counted*10

	def gameover(self, grid):
		if len(grid.getAvailableMoves()) == 0:
			return -100000
		return 0

	def density(self, grid):
		density = 0
		maxTile = grid.getMaxTile()
		m = grid.map
		size = grid.size
		for row in range(0, size):
			for col in range(0, size):
				if m[row][col] != 0:
					density += (math.log(m[row][col])/math.log(2))*m[row][col]
		return density

	def smooth(self, grid):
		m = grid.map
		size = grid.size
		smoothness = 0
		for row in range(0, size):
			for col in range(0, size):
				merge_cell = 0
				if m[row][col] != 0:
					cell_val = math.log(m[row][col])/math.log(2)
					for i in range(1, 3):
						# Down
						if i == 1:
							x = row + 1
							while x < size and merge_cell == 0:
								merge_cell = m[x][col]
								x += 1

							if merge_cell != 0:
								merge_cell = math.log(merge_cell)/math.log(2)
								smoothness -= abs(merge_cell - cell_val)
						# Right
						elif i == 2:
							y = col + 1
							merge_cell = 0
							while y < size and merge_cell == 0:
								merge_cell = m[row][y]
								y += 1
							if merge_cell != 0:
								merge_cell = math.log(merge_cell)/math.log(2)
								smoothness -= abs(merge_cell - cell_val)
			
		return smoothness

	def corner(self, grid):
		# Check if we have the highest tile in a corner, this is to encourage keeping it there.
		m = grid.map
		size = grid.size
		high = grid.getMaxTile()
		if high == m[0][0] or high == m[0][size-1] or high == m[size-1][0] or high == m[size-1][size-1]:
			return math.log(100)/math.log(2)
		else:
			return 0

	def mono(self, grid):
		m = grid.map
		size = grid.size
		mono = [0, 0, 0, 0]

		# Check for verticals.
		for row in range(0, size):
			current_col = 0
			next_col = current_col + 1
			while next_col < size:
				while next_col < size and m[row][next_col] == 0:
					next_col += 1
				if next_col >= size:
					next_col -= 1
				
				current_val = 0
				if m[row][current_col] != 0:
					current_val = math.log(m[row][current_col])/math.log(2)

				next_val = 0
				if m[row][next_col] != 0:
					next_val = math.log(m[row][next_col])/math.log(2)

				if current_val > next_val:
					mono[0] += next_val - current_val
					#mono[0] += current_val - next_val
				elif current_val < next_val:
					mono[1] += current_val - next_val
					#mono[1] += next_val - current_val

				current_col = next_col
				next_col += 1

		# Check for horizontals.
		for col in range(0, size):
			current_row = 0
			next_row = current_row + 1
			while next_row < size:
				while next_row < size and m[next_row][col] == 0:
					next_row += 1
				if next_row >= size:
					next_row -= 1
				
				current_val = 0
				if m[current_row][col] != 0:
					current_val = math.log(m[current_row][col])/math.log(2)

				next_val = 0
				if m[next_row][col] != 0:
					next_val = math.log(m[next_row][col])/math.log(2)

				if current_val > next_val:
					mono[2] += next_val - current_val
					#mono[2] += current_val - next_val
				elif current_val < next_val:
					mono[3] += current_val - next_val
					#mono[3] += next_val - current_val

				current_row = next_row
				next_row += 1

		return max(mono[0], mono[1]) + max(mono[2], mono[3])


	def maxValue(self, grid):
		return grid.getMaxTile()

	def collapseMax(self, grid):
		m = grid.map
		size = grid.size
		current_max = grid.getMaxTile()
		new_max = 0

		for row in range(0, size):
			for col in range(0, size):
				for i in range(0, 4):
					# UP
					if i == 0:
						x = row-1
						y = col
						if x >= 0 and y >= 0:
							if m[row][col] == m[x][y]:
								result = (m[row][col]+m[x][y])
								if result > current_max:
									new_max = result
					# Down
					elif i == 1:
						x = row+1
						y = col
						if x < size and y < size:
							if m[row][col] == m[x][y]:
								result = (m[row][col]+m[x][y])
								if result > current_max:
									new_max = result
					# Left
					elif i == 2:
						x = row
						y = col-1
						if x >= 0 and y >= 0:
							if m[row][col] == m[x][y]:
								result = (m[row][col]+m[x][y])
								if result > current_max:
									new_max = result
					# Right
					elif i == 3:
						x = row
						y = col+1
						if x < size and y < size:
							if m[row][col] == m[x][y]:
								result = (m[row][col]+m[x][y])
								if result > current_max:
									new_max = result
		
		return new_max

	def island(self, grid):
		m = grid.map
		size = grid.size
		stranded = 0

		for row in range(0, size):
			for col in range(0, size):
				island = False
				if m[row][col] != 0:
					island = True
					for vertical in range(0, 2):
						for horizontal in range(0, 2):
							r = row - horizontal
							c = col - vertical
							if c >= 0 and r >= 0:
								if m[r][c] == 0 or m[r][c] == m[row][col]:
									island = False

				if island:
					stranded += 1

		return stranded*-1



	def utility(self, grid, chosen = False):
		# Define weights for heuristics.
		utility = 0
		ft = self.freeTiles(grid)
		sm = self.smooth(grid)
		mo = self.mono(grid)
		ma = self.maxValue(grid)
		nm = self.collapseMax(grid)
		co = self.complexity(grid)
		de = self.density(grid)
		go = self.gameover(grid)

		utility += (ft*self.free_weight)
		utility += (sm*self.smooth_weight)
		utility += (mo*self.mono_weight)
		utility += (ma*self.max_weight)
		utility += (nm*self.newmax_weight)
		utility += (co*self.complex_weight)
		utility += (de*self.density_weight)
		utility += (go*self.gameover_weight)

		#if chosen:
			#print 'Heuristics:'
			#print 'Free: ', ft
			#print 'Smooth: ', sm
			#print 'Mono: ', mo
			#print 'Max: ', ma
			#print 'New Max: ', nm
			#print 'Complex: ', co
			#print 'Dense: ', de
			#print 'Game Over: ', go
			#print 'Utility: ', utility
		#max_base = math.log(self.maxValue(grid))/math.log(2)
		#print grid.map
		#utility += (self.freeTiles(grid)*free_weight)
		#print 'Free Tiles: ', (self.freeTiles(grid)*free_weight)
		#utility += (self.smooth(grid)*smooth_weight)
		#print 'Smooth: ', (self.smooth(grid)*smooth_weight)
		#utility += (self.mono(grid)*mono_weight)
		#print 'Mono: ', (self.mono(grid)*mono_weight)
		#utility += (self.corner(grid)*corner_weight)
		#print 'Corner: ', (self.corner(grid)*corner_weight)
		#utility += (self.maxValue(grid)*max_weight)
		#utility += (self.complexity(grid)*complex_weight)
		#utility += (self.density(grid)*density_weight)
		#utility += (self.goalCounter(grid)*goal_weight)
		#utility += (self.gameover(grid)*gameover_weight)
		#utility += (self.collapseMax(grid)*newmax_weight)

		#utility += (self.island(grid)*(island_weight+(max_base/10)))
		#print 'Max Val: ', (self.maxValue(grid)*max_weight)

		#print utility

		return utility

	def minimize(self, grid, alpha, beta, init_time, depth):
		depth -= 1
		if time.clock() - init_time > time_limit:
			return [None, 0, True]
		#if grid.getMaxTile() == 2048 or depth == 0:
		if depth == 0:
			return [None, self.utility(grid), False]

		state = [None, 9999999, True]

		for cell in grid.getAvailableCells():

			# Insert cell and create grid for it.
			g = grid.clone()
			g.setCellValue(cell, 2)
			m = self.maximize(g, alpha, beta, init_time, depth)

			#print 'Min depth: ', depth
			#print 'Min Utility Option: ', m[1]

			g2 = grid.clone()
			g2.setCellValue(cell, 4)
			m2 = self.maximize(g2, alpha, beta, init_time, depth)

			#print 'Min depth: ', depth
			#print 'Min Utility Option: ', m2[1]

			# Check which utility is lower.
			if m[1] < state[1] or m2[1] < state[1]:
				if m[1] < m2[1]:
					state = m
				else:
					state = m2

				#state[1] = state[1]+self.utility(grid)

			#print 'Selected Utility: ', state[1]
			#print ''
			# Check if we can cut some branches.
			if state[1] <= alpha:
				state[1] += self.utility(grid)
				return state

			if state[1] < beta:
				beta = state[1]

		state[1] += self.utility(grid)

		return state

	def maximize(self, grid, alpha, beta, init_time, depth):
		depth -= 1
		if time.clock() - init_time > time_limit:
			return [None, 0, True]
		#if grid.getMaxTile() == 2048 or depth == 0:
		if depth == 0:
			return [None, self.utility(grid), False]

		state = [None, -9999999, True]

		for move in grid.getAvailableMoves():

			# Make move and create grid for it.
			g = grid.clone()
			g.move(move)
			m = self.minimize(g, alpha, beta, init_time, depth)

			#print 'Max depth: ', depth
			#print 'Max Utility Option: ', m[1] 
			#print 'Move: ', actionDic[move]
			#print ''
			# Check which utility is higher.

			if m[1] > state[1]:
				state = [move, m[1], m[2]]

			# Check if we can cut some branches.
			if state[1] >= beta:
				state[1] += self.utility(grid)
				return state

			if state[1] > alpha:
				alpha = state[1]

		state[1] += self.utility(grid)
		#print 'Max Utility selected: ', state[1]
		#print 'Move ', state[0]
		return state

	def getMove(self, grid):

		# Get current time.
		init_time = time.clock()
		depth = 2
		last_depth = depth
		loop = True
		selected_move = (0, 0, False)
		depth_limit = 50

		#print 'CURRENT BOARD:'
		#print grid.map

		while loop:
		#for x in range(0, 10):
			last_depth = depth
			#print 'Possible moves: ', grid.getAvailableMoves()
			move = self.maximize(grid, -9999999, 9999999, init_time, depth)
			loop = time.clock() <= (init_time + time_limit)
			depth = last_depth + 1
			#print last_depth
			#print move
			if not move[2]:
				selected_move = move
			#else:
			#	print 'Timeout'
			if last_depth >= depth_limit:
				loop = False

		#print last_depth
		#print actionDic[selected_move[0]]
		return selected_move[0]
		#return randint(0, 3) 