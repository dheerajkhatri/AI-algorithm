import sys
import random
import math
import numpy as np
from sets import Set
from Queue import PriorityQueue

np.random.seed(5)

class IDASTAR():

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

	def apply_idastar(self,start,goal,bound,debug=False):
		closedList = Set([])
		openList = PriorityQueue()
		self.cameFrom  = {}
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
			if xcurrent == xgoal:
				return True,self.reconstruct_path(goal),openList.qsize()+len(closedList)
			
			closedList.add(xcurrent)
			neighbours = self.get_neighbours(current)
			next_bound = sys.maxsize
			for n in neighbours:
				xn = self.encode(n)
				if xn in closedList:
					continue
				tentative_gScore = self.get_gScore(xn) + 1
				tentative_fScore = tentative_gScore + self.heuristic_cost_estimate(n,goal)

				if tentative_fScore > bound:
					if next_bound > tentative_fScore:
						next_bound = tentative_fScore
					continue

				neighbourInOpnedList = False
				for value,cnt,xitem in openList.queue:
					if xitem == xn:
						neighbourInOpnedList = True
						break
				if neighbourInOpnedList == False:
					openList.put((tempScore,count,xneighbour))

				#If this is not a better path
				elif tentative_gScore >= self.get_gScore(xn):				
					continue
				
				self.cameFrom[xn] = current
				self.gScore[xn] = tentative_gScore
				self.fScore[xn] = tentative_fScore
		return False,next_bound,len(closedList)+openList.qsize()


	def idastar_main(self,start,goal,debug=False):
		bound = self.heuristic_cost_estimate(start,goal)
		#print bound
		total_nodes_generated = 0

		while True:
			f,result,total_size = self.apply_idastar(start,goal,bound)
			if f == False and result == sys.maxsize:
				return None
			total_nodes_generated += total_size
			if f == False:
				bound = result
			else:
				return result,total_nodes_generated
		return None

def ex1_2():
	trails = 1
	nums = [i for i in range (16)]	
	npmat = np.reshape(nums,(4,4))
	goal = npmat
	idastar = IDASTAR()
	
	for i in range(0,trails):
		start = idastar.generate_initial_state(goal.copy(),60)		
		print start
		resultPath,totalNodes = idastar.idastar_main(start,goal)
		#print resultPath
		print 'Nodes generated:' + str(totalNodes)
		for i in range(len(resultPath)-1,-1,-1):
			print resultPath[i]

if __name__ == '__main__':	
	ex1_2()