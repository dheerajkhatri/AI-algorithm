import sys
import random
import math
import numpy as np
from sets import Set
from queen import decode,generate_instance,generate_instance_file,get_neighbours,num_attacking,get_fitness
QUEENS = 8

def roulette_selection(fitness):
	init_pop_size = len(fitness)
	total_fitness = 0
	for i in range(init_pop_size):
		total_fitness += fitness[i]

	selectPoint = np.random.uniform(0., 1.) * total_fitness

	for i in range(init_pop_size):
		selectPoint -= fitness[i]
		if selectPoint <=0 :
			return i

	return init_pop_size-1

def mutation_possible(node,mutProb):
	curMutProb = np.random.uniform(0., 1.)

	if curMutProb > mutProb:
		mutationPos = random.randint(0,QUEENS-1)
		mutationVal = random.randint(1,QUEENS)
		node[mutationPos][1] = mutationVal

	return node

def cross_over_and_mutation(node1,node2,mutProb):
	crossOverPoint = random.randint(1,QUEENS)
	
	for i in range(crossOverPoint,QUEENS):
		temp = node1[i][1]
		node1[i][1] = node2[i][1]
		node2[i][1] = temp

	
	node1 = mutation_possible(node1,mutProb)
	node2 = mutation_possible(node2,mutProb)
	return node1,node2,crossOverPoint

def genetic_algorithm(init_pop,mutProb=0.1,time=1000,debug=False):
	
	cur_pop = init_pop	
	t = 0
	MAX_FITNESS = (QUEENS*(QUEENS-1))/2

	while t < time:
		fitness = []			
		cur_pop_size = len(cur_pop)
		for i in range(cur_pop_size):
			fit = get_fitness(cur_pop[i])
			if fit == MAX_FITNESS:
				return cur_pop[i],t
			fitness.append(fit)

		if debug == True:		
			print 'fitness:' + str(fitness)			
	
		selectionIndex = []

		for i in range(cur_pop_size):
			index = roulette_selection(fitness)
			selectionIndex.append(index)		

		if debug == True:
			print 'selectionIndex:' + str(selectionIndex)

		res = []		
		for i in range(cur_pop_size/2):
			node1,node2 = init_pop[selectionIndex[2*i]],init_pop[selectionIndex[2*i+1]] 
			ret1,ret2,point = cross_over_and_mutation(node1,node2,mutProb)
			
			res.append(ret1)
			res.append(ret2)				

		t += 1
		cur_pop = res		
	return None,t
	

def ex4():
	trials = 20
	solved = 0
	mutProb = 0.1
	init_pop_size = 16
	max_time_allowed = 10000

	print 'Trails:' + str(trials)
	print 'Mutation Prob:' + str(mutProb)
	print 'Initial Population:' + str(init_pop_size)
	print 'Max time allowed:' + str(10000)

	for i in range(trials):	
		init_pop = []
		for j in range(init_pop_size):
			init_pop.append(generate_instance())	
		res,t = genetic_algorithm(init_pop,mutProb,max_time_allowed,False)
		print decode(res)
		if res!=None:
			solved += 1
		print 'time taken:' + str(t)
	print 'total solved instaces:' + str(solved)

if __name__ == '__main__':	
	ex4()