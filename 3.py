import sys
import random
import math
import numpy as np
from sets import Set
from Queue import PriorityQueue
QUEENS = 8

def generate_instance():
	#in each column one queen is present
	node = np.zeros((QUEENS,QUEENS),dtype=int)
	for col in range(0,QUEENS):
		row = random.randint(0,QUEENS-1)
		node[row][col] = 1
	return node

def get_neighbours(current):
	neighbours = []
	for col in range(0,QUEENS):
		row = -1
		for i in range(0,QUEENS):
			if current[i][col] == 1:
				row = i
				break
		newNeighbour1 = np.empty_like(current)
		newNeighbour2 = np.empty_like(current)
		newNeighbour1[:] = current
		newNeighbour2[:] = current
		if row-1 >=0:
			newNeighbour1[row-1][col] = 1
			newNeighbour1[row][col]  = 0
			neighbours.append(newNeighbour1)			
		if row+1 < QUEENS:
			newNeighbour2[row+1][col] = 1
			newNeighbour2[row][col] = 0
			neighbours.append(newNeighbour2)

	return neighbours

def num_attacking(node):
	count = 0
	for col in range(0,QUEENS):
		row = -1
		for i in range(0,QUEENS):
			if node[i][col] == 1:
				row = i
				break
		for j in range(0,QUEENS):
			if j==col:
				continue
			else:
				if node[row][j] == 1:
					count += 1
	return count

def get_fitness(node):
	count = 0
	for col in range(0,QUEENS):
		row = -1
		for i in range(0,QUEENS):
			if node[i][col] == 1:
				row = i
				break
		for j in range(0,QUEENS):
			if j==col:
				continue
			else:
				if node[row][j] == 0:
					count += 1
	return count

def hill_climbing(start,debug=False):
	current = start
	while True:
		neighbours = get_neighbours(current)
		min_attacking = QUEENS*(QUEENS-1)
		nextnode = None

		for neighbour in neighbours:

			if debug == True:
				print neighbour
				print num_attacking(neighbour)

			if(num_attacking(neighbour) < min_attacking):
				nextnode = neighbour
				min_attacking = num_attacking(neighbour)

		if min_attacking >= num_attacking(current):
			if num_attacking(current)!=0:
				return None
			else:
				return current
		current = nextnode

def get_accept_prob(newAttacking,attacking,T):
	if newAttacking < attacking:
		return 1
	else:
		return math.exp((1.0*(attacking - newAttacking))/T)	

def get_t_schedule(T):
	return (1.0/T)

def simulated_annealing(start,debug=False):
	current = start
	attacking = num_attacking(current)
	t = 10
	T = t
	T_min = 0.0001		

	while T > T_min:		

		T = get_t_schedule(t)
		t += 1

		neighbours = get_neighbours(current)
		newSolution = random.choice(neighbours)
		newAttacking = num_attacking(newSolution)			
		acceptProb = get_accept_prob(newAttacking,attacking,T)		

		if attacking == 0:
			return newSolution,0

		if debug == True:
			print 'T: ' + str(T)
			print newSolution			
			print 'newAttacking: ' + str(newAttacking)
			print 'acceptProb: ' + str(acceptProb)
			raw_input('Press Enter to continue...\n')

		if acceptProb >= np.random.uniform(0., 1.):
			current = newSolution			
			attacking = newAttacking		
	
	return current,attacking

def ex3():
	instances = 1000
	init_state = []
	resutls_rr = []
	resutls_sa = []
	solved_rr = 0
	solved_sa = 0

	for i in range(0,instances):				
		start = generate_instance()
		init_state.append(start)
		ret = hill_climbing(start)
		if ret!=None:
			solved_rr += 1
			resutls_rr.append(ret)
		else:
			resutls_rr.append(None)


		ret,attacking = simulated_annealing(start)
		if attacking == 0:
			solved_sa += 1
			resutls_sa.append(ret)
		else:
			resutls_sa.append(None)
	# for i in range(0,instances):
	# 	print init_state[i]
	# 	print resutls[i]
	print 'total instances:' + str(instances) + '\n'
	print 'Random Restart'	
	print 'solved instances:' + '\t' + str(solved_rr) + '\t' + str(float(solved_rr)/instances)	
	print '\nSimulated Annealing'
	print 'solved instances:' + '\t' + str(solved_sa) + '\t' + str(float(solved_sa)/instances)	

if __name__ == '__main__':	
	ex3()