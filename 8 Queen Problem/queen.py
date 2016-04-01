import sys
import random
import math
import numpy as np
from sets import Set
QUEENS = 8

def decode(current):
	if current == None:
		return None
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

def get_fitness(current):
	return max(0,(QUEENS*(QUEENS-1)/2)-num_attacking(current))