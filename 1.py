import sys
import random
import math
import numpy as np
from sets import Set
from Queue import PriorityQueue

np.random.seed(5)

class ASTAR():

	def get_pos_map(self,node):
		posMap = {}
		for i in range(0,node.shape[0]):
			for j in range(0,node.shape[1]):
				posMap[node[i][j]] = (i,j)
		return posMap

	#get heuristic cost to reach to the goal node from current node for 15puzzle problem
	def heuristic_cost_estimate(self,current,goal):
		currentPosMap = self.get_pos_map(current)
		goalPosMap = self.get_pos_map(goal)
		totalManhattanDis = 0		

		for i in range(1,16):
			totalManhattanDis += abs((currentPosMap[i])[0] - (goalPosMap[i])[0])
			totalManhattanDis += abs((currentPosMap[i])[1] - (goalPosMap[i])[1])

		return totalManhattanDis

	def dist_between(self,node1,node2):
		return 1

	def reconstruct_path(self,current):				
		total_path = [current]		
		while self.encode(current) in self.cameFrom:		
			current = self.cameFrom[self.encode(current)]
			total_path.append(current)
		return total_path

	def get_neighbours(self,current):			
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
				#make a deep copy here don't set reference like newNeighbour = currnet
				newNeighbour = np.empty_like(current)
				newNeighbour[:] = current
				newNeighbour[zeroxpos][zeroypos] = newNeighbour[curxpos][curypos]
				newNeighbour[curxpos][curypos] = 0
				neighbours.append(newNeighbour)

		return neighbours

	def get_gScore(self,xcurrent):
		if xcurrent not in self.gScore:
			return sys.maxsize
		return self.gScore[xcurrent]

	def get_fScore(self,xcurrent):
		if xcurrent not in self.fScore:
			return sys.maxsize
		return self.fScore[xcurrent]

	def generate_initial_state(self,current,moves=50):
		
		for i in range(0,moves):
			neighbours = self.get_neighbours(current)
			#now randomly choose from 
			next_node  = random.choice(neighbours)						
			current = next_node			
		
		return current

	def encode(self,current):
		ret = ''
		for i in range(0,current.shape[0]):
			for j in range(0,current.shape[1]):
				ret += str(current[i][j])				
				if (i != current.shape[0]-1 or j != current.shape[1]-1):
					ret += ','				
		return ret

	def decode(self,xcurrent):
		currentList = xcurrent.split(',')
		size = int(math.sqrt(len(currentList)))
		current = np.empty([size,size],dtype=int)
		count = 0
		for i in range(0,size):
			for j in range(0,size):
				current[i][j] = int(currentList[count])
				count += 1
		return current

	def apply_astar(self,start,goal,debug=False):	
		# The set of nodes already evaluated.
		closedList = Set([])

		#The set of currently discovered nodes still to be evaluated.
		openList = PriorityQueue()	
		
		'''
		For each node, which node it can most efficiently be reached from.
	    If a node can be reached from many nodes, cameFrom will eventually contain the
	    most efficient previous step.'''
		self.cameFrom  = {}

		'''
		For each node, the cost of getting from the start node to that node.
		map with default value of Infinity'''
		self.gScore = {}
		self.fScore = {}

		xstart = self.encode(start)
		xgoal = self.encode(goal)
		self.gScore[xstart] = 0
		self.fScore[xstart] = self.heuristic_cost_estimate(start,goal)	

		count = 1
		openList.put((self.fScore[xstart],count,xstart))

		while openList.qsize() > 0:
			
			fcurrent,other,xcurrent = openList.get()
			current = self.decode(xcurrent)												

			if debug == True:
				print 'PQ size: ' + str(openList.qsize())				
				print current
				print 'fscore is : ' + str(fcurrent)
				raw_input('Press Enter to Continue..\n')					
	

			if xcurrent == xgoal:					
				return self.reconstruct_path(goal),openList.qsize()+len(closedList)
			
			closedList.add(xcurrent)
			neighbours = self.get_neighbours(current)
		
			for neighbour in neighbours:

				xneighbour = self.encode(neighbour)
				if xneighbour in closedList:
					if debug == True:		
						print neighbour
						print 'Neighbour present in ClosedList\n'
					continue				

				tentative_gScore = self.get_gScore(xcurrent) + self.dist_between(current,neighbour)
				#Neighbour not in openset - Discover a new node
				

				neighbourInOpnedList = False
				for value,cnt,xitem in openList.queue:
					if xitem == xneighbour:
						neighbourInOpnedList = True
						break

				if neighbourInOpnedList == False:					
					tempScore = tentative_gScore + self.heuristic_cost_estimate(neighbour,goal)					
					count += 1
					openList.put((tempScore,count,xneighbour))
					#print neighbour
					#print 'added with score ' + str(tempScore) + ' ' + str(tentative_gScore) + '+' + str(self.heuristic_cost_estimate(neighbour,goal))

				#If this is not a better path
				elif tentative_gScore >= self.get_gScore(xneighbour):
					if debug == True:
						print 'better gscore present, continue\n'
					continue

				
				self.cameFrom[xneighbour] = current
				self.gScore[xneighbour] = tentative_gScore
				self.fScore[xneighbour] = self.get_gScore(xneighbour) + self.heuristic_cost_estimate(neighbour,goal)

		print 'No Solution Exists'	
		return ''


class IDASTAR():

	def ida_start(self,current):
		pass

	def search():
		pass


def ex1():
	trails = 1
	nums = [i for i in range (16)]	
	npmat = np.reshape(nums,(4,4))
	goal = npmat
	astar = ASTAR()
	
	for i in range(0,trails):
		start = astar.generate_initial_state(goal.copy(),60)		
		print start
		resultPath,totalNodes = astar.apply_astar(start,goal,False)
		print 'Nodes generated:' + str(totalNodes)
		for i in range(len(resultPath)-1,-1,-1):
			print resultPath[i]

def ex1_2():
	pass

if __name__ == '__main__':	
	ex1()