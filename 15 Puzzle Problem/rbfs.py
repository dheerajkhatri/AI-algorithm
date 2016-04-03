import sys
import random
import math
import numpy as np
from sets import Set

def get_pos_map(node):
	posMap = {}
	for i in range(0,node.shape[0]):
		for j in range(0,node.shape[1]):
			posMap[node[i][j]] = (i,j)
	return posMap

#get heuristic cost to reach to the goal node from current node for 15puzzle problem
def heuristic_cost_estimate(current,goal):
	currentPosMap = get_pos_map(current)
	goalPosMap = get_pos_map(goal)
	totalManhattanDis = 0		

	for i in range(1,16):
		totalManhattanDis += abs((currentPosMap[i])[0] - (goalPosMap[i])[0])
		totalManhattanDis += abs((currentPosMap[i])[1] - (goalPosMap[i])[1])

	return totalManhattanDis

def get_neighbours(current):			
	neighbours = []

	zeroxpos,zeroypos = 0,0
	for i in range(0,current.shape[0]):
		for j in range(0,current.shape[1]):
			if current[i][j] == 0:
				zeroxpos = i
				zeroypos = j		

	#there can be atmax 4 neighbours
	xpos = [-1,0,1,0]
	ypos = [0,1,0,-1]

	for i in range(0,4):
		curxpos = zeroxpos + xpos[i]
		curypos = zeroypos + ypos[i]
		if(curxpos >=0 and curypos >=0 and curxpos < current.shape[0] and curypos < current.shape[1]):
			#make a deep copy here don't set reference like newNeighbour = current
			newNeighbour = np.empty_like(current)
			newNeighbour[:] = current
			newNeighbour[zeroxpos][zeroypos] = newNeighbour[curxpos][curypos]
			newNeighbour[curxpos][curypos] = 0
			neighbours.append(newNeighbour)

	return neighbours

def generate_initial_state(current,moves=50):
	
	for i in range(0,moves):
		neighbours = get_neighbours(current)
		#now randomly choose from 
		next_node  = random.choice(neighbours)						
		current = next_node			
	
	return current

def encode(current):
	ret = ''
	for i in range(0,current.shape[0]):
		for j in range(0,current.shape[1]):
			ret += str(current[i][j])				
			if (i != current.shape[0]-1 or j != current.shape[1]-1):
				ret += ','				
	return ret

def decode(xcurrent):
	currentList = xcurrent.split(',')
	size = int(math.sqrt(len(currentList)))
	current = np.empty([size,size],dtype=int)
	count = 0
	for i in range(0,size):
		for j in range(0,size):
			current[i][j] = int(currentList[count])
			count += 1
	return current

all_xnodes = Set([])

class Node:
	def __init__(self,xstate=None,xparent=[],cost=[sys.maxsize,sys.maxsize]):
		self.xstate = xstate
		self.xparent = xparent
		self.cost = cost

def rbfs(curNode,goal,curOffLimit):	
	xgoal = encode(goal)
	global all_xnodes
	if curNode.xstate == xgoal:
		return curNode
	succ = []	
	neighbours = get_neighbours(decode(curNode.xstate))
	

	for n in neighbours:		
		xn = encode(n)
		all_xnodes.add(xn)
		newChild = Node(xstate=xn)
		newChild.xparent = curNode.xparent + [newChild.xstate]
		h_val = heuristic_cost_estimate(n,goal)
		g_val = curNode.cost[0] + 1
		f_val = max(curNode.cost[0] + curNode.cost[1] , g_val + h_val)
		final_h_val = f_val - g_val
		newChild.cost = [g_val,final_h_val]
		succ.append(newChild)

	if len(succ) == 0:
		return Node()
	
	while True:		
		succ.sort(key=lambda x: x.cost[0]+x.cost[1])		
		bestSucc = succ[0]
		bestf = bestSucc.cost[0]+bestSucc.cost[1]		

		if bestf > curOffLimit:
			return Node(cost=bestSucc.cost)
		
		alternative = Node()		

		if len(succ)>1:
			alternative = succ[1]		
		alternativef = alternative.cost[0]+alternative.cost[1]
		
		result = rbfs(bestSucc, goal, min(curOffLimit,alternativef))
		succ[0].cost[1] = result.cost[0]+result.cost[1]-succ[0].cost[0]
		if result.xstate is not None:
			return result

def rbfs_main(start, goal, debug=False):
    global all_xnodes
    xstart = encode(start)
    xgoal = encode(goal)
    all_xnodes = Set([xstart])
    node = Node(xstart, [xstart], [0,heuristic_cost_estimate(start,goal)])
    resNode=rbfs(node, goal, sys.maxsize)
    return resNode.xparent, len(all_xnodes)

def ex2():	
	trails = 20
	nums = [i for i in range (16)]
	npmat = np.reshape(nums,(4,4))
	goal = npmat
	for i in range(trails):
		start = generate_initial_state(goal.copy(),50)
		#print start
		tot_path,nodes_generated=rbfs_main(start,goal)		
		for val in tot_path:
			#print decode(val)		
			pass
		print nodes_generated,len(tot_path)

ex2()