import sys
import random
import math
import numpy as np
from sets import Set
QUEENS = 8

def decode(current):
	node = np.zeros((8,8),dtype=int)
	for pos in current:
		node[pos[0]-1,pos[1]-1] = 1
	return node

def generate_instance():
	#each queen's position is (x,y)
	node = np.zeros((QUEENS,2),dtype=int)
	pos = Set([])
	for i in range(QUEENS):				
		while True:
			row = random.randint(1,QUEENS)
			col = random.randint(1,QUEENS)
			if(row,col) not in pos:
				#modify this if you want to generate compltely randome chessboard
				#otherwise this will generate one queen in each column
				#node[i][0] = row
				node[i][0] = i+1
				node[i][1] = col
				pos.add((row,col))
				break			
	return node

def generate_instance_file():
	node = np.zeros((QUEENS,2),dtype=int)
	i = 0
	for line in open('input.txt','r'):
		line = line.strip()
		x,y = line.split(' ')
		xint = int(x)
		yint = int(y)
		if (xint < 0 or yint < 0  or xint > QUEENS or yint > QUEENS):
			print xint,yint
			print 'error in input file'
			sys.exit(0)
		node[i] = (xint,yint)
		i += 1
	return node

#this function assumes constraint that there is exact one queen in each column
def get_neighbours(current):	
	neighbours = []
	for i in range(QUEENS):
		(curx,cury) = current[i]
		for j in range(QUEENS):
			if j+1 == cury:
				continue
			newnode = current.copy()
			newnode[i][1] = j+1
			neighbours.append(newnode)	

	return neighbours	

def num_attacking(current):
	count = 0	
	for i in range(0,QUEENS):
		curx,cury = current[i]
		for j in range(i+1,QUEENS):
			nextx,nexty = current[j]
			if curx==nextx or cury==nexty or abs(curx-nextx)==abs(cury-nexty):
				count += 1
	return count

def hill_climbing(start,debug=False):
	current = start
	while True:
		attacking_cur = num_attacking(current)
		if(attacking_cur==0):
			return current

		neighbours = get_neighbours(current)
		min_attacking = QUEENS*(QUEENS-1)
		nextnode = None

		for neighbour in neighbours:

			if debug == True:
				print neighbour
				print num_attacking(neighbour)

			attacking_neigh = num_attacking(neighbour)

			if(attacking_neigh < min_attacking):
				nextnode = neighbour
				min_attacking = attacking_neigh

		if min_attacking >= attacking_cur:			
			return None	
		
		current = nextnode

def random_restart(no_restart=1000):
	for i in range(0,no_restart):
		start = generate_instance()
		ret = hill_climbing(start)
		if ret!=None:
			return ret,i
	return None,i

def get_accept_prob(newAttacking,attacking,T):
	if newAttacking < attacking:
		return 1
	else :		
		return math.exp((1.0*(attacking - newAttacking))/T)	

def simulated_annealing(start,debug=False):
	current = start
	attacking = num_attacking(current)
	prev_best = attacking
	T = 1.0	
	T_min = 0.00001		
	alpha = 0.9

	while T > T_min:				

		if debug == True:
			print 'T: ' + str(T)
			raw_input('Press Enter to continue...\n')

		for i in range(100):
			neighbours = get_neighbours(current)
			newSolution = random.choice(neighbours)
			newAttacking = num_attacking(newSolution)			
			acceptProb = get_accept_prob(newAttacking,attacking,T)
			
			if debug == True:
				
				print newSolution			
				print 'newAttacking: ' + str(newAttacking)
				print 'acceptProb: ' + str(acceptProb)

			if acceptProb > np.random.uniform(0., 1.):
				current = newSolution
				attacking = newAttacking	

		if attacking == 0:
			return current,0

		T = T*alpha
		prev_best = attacking

	return current,attacking

def ex3():
	instances = 10
	init_state = []
	resutls_rr = []
	resutls_sa = []
	solved_rr = 0
	solved_sa = 0

	for i in range(0,instances):		
		print str(i) + ':'
		start = generate_instance()
		init_state.append(start)
		
		ret,restarts = random_restart(100)
		resutls_rr.append(ret)
		if ret!=None:					
			solved_rr += 1			
			print decode(ret)
			print 'restarts: ' + str(restarts)

		ret,attacking = simulated_annealing(start,False)
		#print ret
		#print attacking
		if attacking == 0:
			solved_sa += 1			
			print decode(ret)
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