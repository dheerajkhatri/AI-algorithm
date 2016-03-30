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

def genetic_algorithm(start):
	pass