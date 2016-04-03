import sys
import math
import random
import numpy as np
from sets import Set
from queen import decode,generate_instance,generate_instance_file,get_neighbours,num_attacking
QUEENS = 8

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
	instances = 20
	init_state = []
	resutls_rr = []
	resutls_sa = []
	solved_rr = 0
	solved_sa = 0

	for i in range(0,instances):		
		print str(i) + ':'
		start = generate_instance()
		init_state.append(start)
		
		ret,restarts = random_restart(10)
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