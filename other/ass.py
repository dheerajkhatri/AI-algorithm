import numpy as np
from collections import OrderedDict
from sets import Set
import cv2
import matplotlib.pyplot as plt

def hamming_dist(a, b):
    a = np.asarray(a)
    b = np.asarray(b)
    c = np.abs(a-b)
    return np.sum(c)

incons = False

def heuristic_cost_estimate(s1, goal_map):
    global incons
    '''
    s1: 2d numpy array with integer values from 0 to 15
    goalmap: A map, [integer] -> (x,y)
    '''
    h = 0
    for i in range(s1.shape[0]):
        for j in range(s1.shape[1]):
            if s1[i,j] == 0:
                continue
            val = s1[i,j]
            h += hamming_dist((i,j), goal_map[val])
    if not incons:
        return h
    else:
        temp = np.array([[-1, 0, -1, -1], [-1, -1, 0, 0], [0, -1, -1, 0], [0, -1, -1, 0]])
        vv = np.sum(temp==s1)
        return (vv==0)*h + (vv!=0)*0

def make_val_map(goal):
    goal_map = {}
    for i in range(goal.shape[0]):
        for j in range(goal.shape[1]):
            goal_map[goal[i,j]] = (i,j)
    return goal_map

def get_all_neighbors(s1):
    all_s = []
    pos0 = None
    for i in range(s1.shape[0]):
        for j in range(s1.shape[1]):
            if s1[i,j] == 0:
                pos0 = (i,j)
                break
        if pos0 is not None:
            break
    i0,j0 = pos0
    if i0 > 0:
        s2 = s1.copy()
        s2[i0,j0]=s2[i0-1,j0]
        s2[i0-1,j0] = 0
        all_s.append(s2.copy())
    if i0 < 3:
        s2 = s1.copy()
        s2[i0,j0]=s2[i0+1,j0]
        s2[i0+1,j0] = 0
        all_s.append(s2.copy())
    if j0 > 0:
        s2 = s1.copy()
        s2[i0,j0]=s2[i0,j0-1]
        s2[i0,j0-1] = 0
        all_s.append(s2.copy())
    if j0 < 3:
        s2 = s1.copy()
        s2[i0,j0]=s2[i0,j0+1]
        s2[i0,j0+1] = 0
        all_s.append(s2.copy())
    return all_s

def decode_state_str(s1):
    x = s1.split(',')
    x = np.asarray(x).astype(np.int32).reshape((4,4))
    return x

def encode_state_str(s1):
    s = ""
    for i in range(s1.shape[0]):
        for j in range(s1.shape[1]):
            s += str(s1[i,j])
            if i != s1.shape[0]-1 or j != s1.shape[1]-1:
                s += ","
    return s

def reconstruct_path(came_from, current):   
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path

def A_star(init_state, goal,  debug=False):
    goal_map = make_val_map(decode_state_str(goal))
    closed_set = Set([])
    open_set = Set([init_state])
    came_from = {}
    g_score = {}
    f_score = {}
    g_score[init_state] = 0
    f_score[init_state] = g_score[init_state] + heuristic_cost_estimate(decode_state_str(init_state), goal_map)
    
    if debug:
        print "START"
    
    while len(open_set) != 0:
        current = None
        min_f_score = 100000
        for state in open_set:
            my_f_score = f_score[state]
            if my_f_score < min_f_score:
                current = state
                min_f_score = my_f_score
        
        if debug:
            print "cur: "
            print decode_state_str(current)
            print "HD:"
            print heuristic_cost_estimate(decode_state_str(current),goal_map)
        
        if current == goal:
            return reconstruct_path(came_from, goal), len(open_set)+len(closed_set)
        
        open_set.remove(current)
        closed_set.add(current)
        
        nbrs = get_all_neighbors(decode_state_str(current))
        
        for nbr in nbrs:
            nbr_str = encode_state_str(nbr)
            if debug:
                print "nbr: "
                print nbr
                print "HD: "
                print heuristic_cost_estimate(nbr, goal_map)
            if nbr_str in closed_set:
                continue
            tentative_g_score = g_score[current] + 1
            if nbr_str not in open_set:
                open_set.add(nbr_str)
            elif nbr_str in g_score and tentative_g_score >= g_score[nbr_str]:
                continue
            came_from[nbr_str] = current
            g_score[nbr_str] = tentative_g_score
            f_score[nbr_str] = g_score[nbr_str] + heuristic_cost_estimate(nbr, goal_map)
        
        if debug:
            raw_input("Press Enter to continue...")
    return None

def find_zero(s1):
    for i in range(s1.shape[0]):
        for j in range(s1.shape[1]):
            if s1[i,j]==0:
                return (i,j)

def make_a_move(s1, mv, i=None, j=None):
    if i==None or j==None:
        i,j = find_zero(s1)
    if mv == 0:
        if i > 0:
            s2 = s1.copy()
            s2[i,j] = s2[i-1,j]
            s2[i-1,j] = 0
            return s2,i-1,j
    if mv == 1:
        if i < 3:
            s2 = s1.copy()
            s2[i,j] = s2[i+1,j]
            s2[i+1,j] = 0
            return s2,i+1,j
    if mv == 2:
        if j > 0:
            s2 = s1.copy()
            s2[i,j] = s2[i,j-1]
            s2[i,j-1] = 0
            return s2,i,j-1
    if mv == 3:
        if j < 3:
            s2 = s1.copy()
            s2[i,j] = s2[i,j+1]
            s2[i,j+1] = 0
            return s2,i,j+1
    return s1,i,j

def make_legal_state(goal, n_moves):
    x,y = (0,0)
    for i in range(n_moves):
        goal,x,y = make_a_move(goal, np.random.randint(0,4), x, y)
    return goal

def plot1(decoded_tot_path, path, id):
    to_plot = []
    to_plot2 = []
    annotatations = []
    for i in range(len(decoded_tot_path)):
        temp = decoded_tot_path[i]*200.0/15.0+50.0
        temp2 = np.zeros((4,5)).astype(np.int32)
        temp2[:,:-1] = temp
        to_plot.append(temp2.copy())
        temp2 = temp2*0-1
        temp2[:,:-1] = decoded_tot_path[i]
        temp2 = temp2.astype('str')
        temp2[temp2=="-1"] = ""
        to_plot2.append(temp2)
        
    to_plot = np.concatenate(to_plot, axis=1)
    to_plot2 = np.concatenate(to_plot2, axis=1)
    cv2.imwrite(path+"/"+str(id)+".png", to_plot)
    
    fig = plt.figure(figsize=(2, 2))
    plt.clf()
    ax = fig.add_subplot(111)
    plt.axis('off')
    res = ax.imshow(np.array(to_plot[:4,:4]), cmap=plt.cm.jet, 
                    interpolation='nearest')
    plt.tight_layout()

    width, height = 4, 4

    for x in xrange(width):
        for y in xrange(height):
            ax.annotate(str(to_plot2[x][y]), xy=(y, x), 
                        horizontalalignment='center',
                        verticalalignment='center')

    plt.savefig(path+"/init_plt_"+str(id)+".png")
    
    fig = plt.figure(figsize=(18, 2))
    plt.clf()
    ax = fig.add_subplot(111)
    plt.axis('off')
    res = ax.imshow(np.array(to_plot), cmap=plt.cm.jet, 
                    interpolation='nearest')
    plt.tight_layout()

    width, height = to_plot2.shape

    for x in xrange(width):
        for y in xrange(height):
            ax.annotate(str(to_plot2[x][y]), xy=(y, x), 
                        horizontalalignment='center',
                        verticalalignment='center')

    plt.savefig(path+"/plt_"+str(id)+".png")

def ex1_1(init_states):
    ret = []
    goal = np.asarray([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
    tot_trials = 20
    for i in range(tot_trials):
        if init_states is None:
            x = make_legal_state(goal.copy(), 50)
        else:
            x = init_states[i]
        x_str = encode_state_str(x)
        tot_path,num_gen_nodes = A_star(x_str, encode_state_str(goal))
        ret.append((x, tot_path, num_gen_nodes))
        if tot_path is not None:
            decoded_tot_path = []
            for j in range(len(tot_path)-1, -1, -1):
                temp = decode_state_str(tot_path[j])
                decoded_tot_path.append(temp)
            plot1(decoded_tot_path, "plots/a_star/", i)
        #raw_input('Done.Press Enter to continue...')
    return ret

def IDA_star(init_state, goal, bound, debug=False):
    goal_map = make_val_map(decode_state_str(goal))
    closed_set = Set([])
    open_set = Set([init_state])
    came_from = {}
    g_score = {}
    f_score = {}
    g_score[init_state] = 0
    f_score[init_state] = g_score[init_state] + heuristic_cost_estimate(decode_state_str(init_state), goal_map)
    
    if debug:
        print "START"
    
    while len(open_set) != 0:
        current = None
        min_f_score = 100000
        for state in open_set:
            my_f_score = f_score[state]
            if my_f_score < min_f_score:
                current = state
                min_f_score = my_f_score
        
        if debug:
            print "cur: "
            print decode_state_str(current)
            print "HD:"
            print heuristic_cost_estimate(decode_state_str(current),goal_map)
        
        if current == goal:
            return 1,reconstruct_path(came_from, goal), len(open_set)+len(closed_set)
        
        open_set.remove(current)
        closed_set.add(current)
        
        nbrs = get_all_neighbors(decode_state_str(current))
        next_min_f = 1000000
        for nbr in nbrs:
            nbr_str = encode_state_str(nbr)
            if debug:
                print "nbr: "
                print nbr
                print "HD: "
                print heuristic_cost_estimate(nbr, goal_map)
            if nbr_str in closed_set:
                continue
            tentative_g_score = g_score[current] + 1
            tentative_f_score = tentative_g_score + heuristic_cost_estimate(nbr, goal_map)
            if tentative_f_score > bound:
                if next_min_f > tentative_f_score:
                    next_min_f = tentative_f_score
                continue
            if nbr_str not in open_set:
                open_set.add(nbr_str)
            elif nbr_str in g_score and tentative_g_score >= g_score[nbr_str]:
                continue
            came_from[nbr_str] = current
            g_score[nbr_str] = tentative_g_score
            f_score[nbr_str] = tentative_f_score
        
        if debug:
            raw_input("Press Enter to continue...")
    return 0,next_min_f,len(open_set)+len(closed_set)

def IDA_star_main(init_state, goal, debug=False):
    bound = heuristic_cost_estimate(decode_state_str(init_state), make_val_map(decode_state_str(goal)))
    tot_nodes_gen = 0
    while True:
        b,x,y = IDA_star(init_state, goal, bound, debug)
        if b == 0 and x == 1000000:
            return None
        tot_nodes_gen += y
        if b == 0:
            bound = x
            if debug:
                print "BOUND UPDATED"
        else:
            return x,tot_nodes_gen
    return None

def ex1_2(init_states):
    ret = []
    goal = np.asarray([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
    tot_trials = 20
    for i in range(tot_trials):
        x = init_states[i]
        x_str = encode_state_str(x)
        tot_path,num_gen_nodes = IDA_star_main(x_str, encode_state_str(goal))
        ret.append((x, tot_path, num_gen_nodes))
        if tot_path is not None:
            decoded_tot_path = []
            for j in range(len(tot_path)-1, -1, -1):
                temp = decode_state_str(tot_path[j])
                decoded_tot_path.append(temp)
            plot1(decoded_tot_path, "plots/ida_star/", i)
        #raw_input('Done.Press Enter to continue...')
    return ret

def ex1():
    ret_a_star = ex1_1()
    init_states = []
    for item in ret_a_star:
        init_states.append(item[0])
    ret_ida_star = ex1_2(init_states)

    for i in range(len(ret_a_star)):
        print len(ret_a_star[i][1]), len(ret_ida_star[i][1])

##
## RBFS
##

class Node:
    def __init__(self, state_=None, parent_=[], cost_=[1000000, 1000000]):
        self.state = state_
        self.parent = parent_
        self.cost = cost_

gen_nodes = Set([])

def rbfs(node, goal, goal_map, flimit, debug=False):    
    print node.state
    print goal
    raw_input('....')
    global gen_nodes
    if node.state == goal:
        return node
    if debug:
        print '*'*50
        print decode_state_str(node.state)
        print 'COST:', node.cost
        print 'FLIMIT', flimit
        raw_input('Press Enter to continue...')
    successors = []
    nbrs = get_all_neighbors(decode_state_str(node.state))
    for nbr in nbrs:
        nbr_str = encode_state_str(nbr)
        gen_nodes.add(nbr_str)
        if debug:
            print "nbr: "
            print nbr
            print "HD: "
            print heuristic_cost_estimate(nbr, goal_map)
        child = Node(state_=nbr_str)
        child.parent = node.parent + [child.state]
        c_h = heuristic_cost_estimate(nbr, goal_map)
        c_g = node.cost[0]+1
        c_f = max(node.cost[0]+node.cost[1],c_h+c_g)
        c_h = c_f-c_g
        child.cost = [c_g, c_h]
        successors.append(child)
    if len(successors) == 0:
        return Node()
    
    while True:
        successors.sort(key=lambda x: x.cost[0]+x.cost[1])
        best = successors[0]
        bestf = best.cost[0]+best.cost[1]
        if bestf > flimit:
            return Node(cost_=best.cost)
        alternative = Node()
        if len(successors)>1:
            alternative = successors[1]
        alternativef = alternative.cost[0]+alternative.cost[1]
        result = rbfs(best, goal, goal_map, min(flimit,alternativef), debug)
        successors[0].cost[1] = result.cost[0]+result.cost[1]-successors[0].cost[0]
        if result.state is not None:
            return result

def rbfs_main(init_state, goal, debug=False):
    global gen_nodes
    gen_nodes = Set([init_state])
    goal_map = make_val_map(decode_state_str(goal))
    node = Node(init_state, [init_state], [0, heuristic_cost_estimate(decode_state_str(init_state), goal_map)])
    mynode=rbfs(node, goal, goal_map, 10000000, debug=debug)
    return mynode.parent, len(gen_nodes)

def ex2_2(init_states):
    ret = []
    goal = np.asarray([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
    tot_trials = 1
    for i in range(tot_trials):
        if init_states is not None:
            x = init_states[i]
        else:
            x = make_legal_state(goal.copy(), 50)
        x_str = encode_state_str(x)
        print x_str        
        tot_path,num_gen_nodes = rbfs_main(x_str, encode_state_str(goal), False)
        #print tot_path
        print num_gen_nodes
        #ret.append((x, tot_path, num_gen_nodes))
        if tot_path is not None:
            decoded_tot_path = []
            for j in range(0, len(tot_path)):
                temp = decode_state_str(tot_path[j])
                decoded_tot_path.append(temp)
            #plot1(decoded_tot_path, "plots/rbfs/", i)
        #raw_input('Done.Press Enter to continue...')
        for r in decoded_tot_path:
            #print r
            pass
    return ret

ex2_2(None)

# # ex2_2(None)
# def ex1_and_2(init_states_):
#     ret_a_star = ex1_1(init_states_)
#     init_states = []
#     for item in ret_a_star:
#         init_states.append(item[0])
#     ret_ida_star = ex1_2(init_states)
#     ret_rbfs = ex2_2(init_states)
#     print 'optimal path lengths'
#     for i in range(len(ret_a_star)):
#         print len(ret_a_star[i][1]), len(ret_ida_star[i][1]), len(ret_rbfs[i][1])
#     print 'number of gen nodes'
#     for i in range(len(ret_a_star)):
#         print (ret_a_star[i][2]), (ret_ida_star[i][2]), (ret_rbfs[i][2])
#     return init_states



# ##################################################
# ##################################################
# def encode_state_str_2(s1):
#     s = ""
#     for i in range(s1.shape[0]):
#             s += str(s1[i,1])
#             if i != s1.shape[0]-1:
#                 s += ","
#     return s

# def decode_state_str_2(s1):
#     x = s1.split(',')
#     y = np.zeros((8,2)).astype(np.int32)
#     for i in range(8):
#         y[i,0] = i+1
#         y[i,1] = int(x[i])
#     x = y.copy()
#     return x

# def get_all_neighbors_2(s1):
#     all_s = []
#     for i in range(8):
#         for j in range(1,9):
#             if s1[i,1] == j:
#                 continue
#             s2 = s1.copy()
#             s2[i,1] = j
#             all_s.append(s2)
#     return all_s

# def is_attacking(x1, y1, x2, y2):
#     if x1 == x2 or y1 == y2 or np.abs(x1-x2) == np.abs(y1-y2):
#         return 1
#     return 0

# def heuristic_cost_estimate_2(s1):
#     cost = 0
#     for i in range(8):
#         for j in range(i+1, 8):
#             if is_attacking(s1[i,0], s1[i,1], s1[j,0], s1[j,1]):
#                 cost += 1
#     return cost

# def fitness_estimate_2(s1):
#     fit = 0
#     for i in range(8):
#         for j in range(i+1, 8):
#             if not is_attacking(s1[i,0], s1[i,1], s1[j,0], s1[j,1]):
#                 fit += 1
#     return fit
        

# def hill_climbing(init_state):
#     s1 = decode_state_str_2(init_state)
#     my_path = []
#     while True:
#         my_path.append(s1)
#         all_s = get_all_neighbors_2(s1)
#         min_cost = heuristic_cost_estimate_2(s1)
#         if min_cost == 0:
#             return encode_state_str_2(s1), my_path
#         min_cost_i = -1
#         cnt = 0
#         for s in all_s:
#             my_cost = heuristic_cost_estimate_2(s)
#             if my_cost < min_cost:
#                 min_cost = my_cost
#                 min_cost_i = cnt
#             cnt += 1
#         if min_cost_i != -1:
#             s1 = all_s[min_cost_i]
#         else:
#             return None, my_path

# def get_queen_board(s):
#     x = np.zeros((8,8)).astype(np.int32)
#     for i in range(8):
#         x[s[i,0]-1, s[i,1]-1] = 1
#     return x

# def plot2(decoded_tot_path, path, id):
#     to_plot = []
#     to_plot2 = []
#     annotatations = []
#     for i in range(len(decoded_tot_path)):
#         temp1 = np.transpose(get_queen_board(decoded_tot_path[i]))
#         temp = temp1*255
#         temp2 = np.zeros((8,9)).astype(np.int32)+125
#         temp2[:,:-1] = temp
#         to_plot.append(temp2.copy())
#         temp2 = temp2*0-1
#         temp2[:,:-1] = temp1
#         temp2 = temp2.astype('str')
#         temp2[temp2=="-1"] = ""
#         temp2[temp2=="0"] = "-"
#         temp2[temp2=="1"] = "Q"
#         to_plot2.append(temp2)
        
#     to_plot = np.concatenate(to_plot, axis=1)
#     to_plot2 = np.concatenate(to_plot2, axis=1)
#     cv2.imwrite(path+"/"+str(id)+".png", to_plot)
    
#     fig = plt.figure(figsize=(18, 2))
#     plt.clf()
#     ax = fig.add_subplot(111)
#     plt.axis('off')
#     res = ax.imshow(np.array(to_plot), cmap=plt.cm.jet, 
#                     interpolation='nearest')
#     plt.tight_layout()

#     width, height = to_plot2.shape

#     for x in xrange(width):
#         for y in xrange(height):
#             ax.annotate(str(to_plot2[x][y]), xy=(y, x), 
#                         horizontalalignment='center',
#                         verticalalignment='center')

#     plt.savefig(path+"/plt_"+str(id)+".png")

# def random_restart_hill_climbing(tot_gen = 10000, n_restart=100):
#     n_solved = 0
#     init_states = []
#     for i in range(tot_gen):
#         init_state = np.zeros((8,2)).astype(np.int32)
#         for j in range(8):
#             init_state[j,0] = j+1
#             init_state[j,1] = np.random.randint(1,9)
#         init_states.append(init_state)
#         init_state_str = encode_state_str_2(init_state)
        
#         x, tot_path = hill_climbing(init_state_str)
#         if x is not None:
#             n_solved += 1
#             #print get_queen_board(decode_state_str_2(x))
#             plot2(tot_path, "plots/random_restart_hill/", i)
#     return n_solved, tot_gen, init_states

# def temp_schedule(t):
#     #return 1./np.log(1.+t)
#     return 1./t

# def simulated_annealing(init_state, epsilon = 1e-4, debug=False):
#     t = 1
#     current = decode_state_str_2(init_state)
#     my_path = []
#     while True:
#         if len(my_path) == 0 or encode_state_str_2(my_path[-1]) != encode_state_str_2(current):
#             my_path.append(current)
#         T = temp_schedule(t)
#         t += 1.
#         if debug:
#             print T
#         current_cost = heuristic_cost_estimate_2(current)
#         if current_cost == 0:
#             return encode_state_str_2(current), my_path
#         if T <= epsilon:
#             return None, my_path
#         all_s = get_all_neighbors_2(current)
#         next = all_s[np.random.randint(0, len(all_s))]
#         next_cost = heuristic_cost_estimate_2(next)
#         if next_cost < current_cost:
#             current = next
#         else:
#             u = np.random.uniform(0., 1.)
#             if u <= np.exp((current_cost-next_cost)/T):
#                 current = next
#     return None, my_path

# def simulated_annealing_main(tot_gen = 10000, init_states=None, debug = False):
#     n_solved = 0
#     for i in range(tot_gen):
#         if init_states is None:
#             init_state = np.zeros((8,2)).astype(np.int32)
#             for j in range(8):
#                 init_state[j,0] = j+1
#                 init_state[j,1] = np.random.randint(1,9)
#         else:
#             init_state = init_states[i]
#         init_state_str = encode_state_str_2(init_state)
#         x, tot_path = simulated_annealing(init_state_str, debug=debug)
#         if x is not None:
#             n_solved += 1
#             #print get_queen_board(decode_state_str_2(x))
#             plot2(tot_path, "plots/sim_ann/", i)
#     return n_solved, tot_gen

# def ex3():
#     tgen = 1000
#     a1,b1,init_states = random_restart_hill_climbing(tot_gen = tgen)
#     a,b = simulated_annealing_main(tot_gen = tgen, init_states=init_states)
#     print "Random Restart Hill::Total:", b1, "Solved:", a1, "Ratio:", (1.0*a1)/b1
#     print "Simulated Annealing::Total:", b, "Solved:", a, "Ratio:", (1.0*a)/b

# # ex3()

# def encode_state_str_3(s1):
#     x = s1
#     y = ""
#     for i in range(8):
#         y += x[i]
#         if i!=7:
#             y += ","
#     return y

# def decode_state_str_3(s1):
#     x = s1.split(',')
#     y = ""
#     for i in range(8):
#         y += x[i]
#     return y

# def reproduce(x, y, debug):
#     u = np.random.randint(0, len(x))
#     if debug:
#         print u, x[:(u+1)], y[(u+1):]
#     c = x[:(u+1)]+y[(u+1):]
#     return encode_state_str_3(c)

# def genetic_algorithm(init_pop, mut_prob = 0.2, total_time=100, debug = False):
#     cur_pop = []
#     for s in init_pop:
#         cur_pop.append(s)
#     t = 0
#     my_path = []
#     while t < total_time:
#         my_path.append(cur_pop)
#         new_pop = []
#         cur_pop_fit_val = np.zeros(len(cur_pop))
#         cur_pop_decoded2 = []
#         cur_pop_decoded3 = []
#         for i in range(len(cur_pop)):
#             cur_pop_decoded2.append(decode_state_str_2(cur_pop[i]))
#             cur_pop_decoded3.append(decode_state_str_3(cur_pop[i]))
#             cur_pop_fit_val[i] = fitness_estimate_2(cur_pop_decoded2[i])
#             cost = heuristic_cost_estimate_2(cur_pop_decoded2[i])
#             if debug:
#                 print cur_pop[i], '->', cur_pop_fit_val[i], '->', cost
#             if cost == 0:
#                 return cur_pop[i], my_path
#         if debug:
#             raw_input('Press Enter to continue...')
#         i = 0
#         fit_cum_sum = np.cumsum(cur_pop_fit_val)*1.0
#         fit_cum_sum = fit_cum_sum / fit_cum_sum[-1]
#         while i < len(cur_pop):
#             u1 = np.random.uniform(0., 1.)
#             u2 = np.random.uniform(0., 1.)
#             x = np.argmax(fit_cum_sum >= u1)
#             y = np.argmax(fit_cum_sum >= u2)
#             if x == y:
#                 continue
#             child = reproduce(cur_pop_decoded3[x], cur_pop_decoded3[y], debug)
            
#             if debug:
#                 print cur_pop[x], '+', cur_pop[y], '->', child
#                 raw_input('Press Enter to continue...')
            
#             u = np.random.uniform(0.,1.)
#             if u <= mut_prob:
#                 child_ = decode_state_str_2(child)
#                 pos = np.random.randint(0,8)
#                 transfer_to = np.random.randint(1,9)
#                 child_[pos,1] = transfer_to
#                 child = encode_state_str_2(child_)
#             new_pop.append(child)
#             i += 1
#         cur_pop = new_pop
#         t += 1
#     return None, my_path

# def plot3(tot_path, path, pop_size, f_sol, id):
#     to_plot = []
#     to_plot2 = []
#     annotatations = []
#     for i in range(len(tot_path)):
#         to_plot_ = []
#         for aa in tot_path[i]:
#             temp1 = np.transpose(get_queen_board(decode_state_str_2(aa)))
#             temp = temp1*255
#             temp2 = np.zeros((9,8)).astype(np.int32)+125
#             temp2[:-1,:] = temp
#             to_plot_.append(temp2.copy())
#         to_plot_ = np.concatenate(to_plot_)
#         temp1 = to_plot_
#         temp2 = np.zeros((temp1.shape[0],temp1.shape[1]+1)).astype(np.int32)+125
#         temp2[:,:-1] = temp1
#         to_plot.append(temp2.copy())
#         temp2[temp2==125] = -1
#         temp2[temp2==255] = 0
#         temp2 = temp2.astype('str')
#         temp2[temp2=="-1"] = ""
#         temp2[temp2=="0"] = "-"
#         temp2[temp2=="1"] = "Q"      
#         to_plot2.append(temp2.copy())
    
#     to_plot.append(f_sol.copy())
#     f_sol[f_sol==125] = -1
#     f_sol[f_sol==255] = 0
#     f_sol = f_sol.astype('str')
#     f_sol[f_sol=="-1"] = ""
#     f_sol[f_sol=="0"] = "-"
#     f_sol[f_sol=="1"] = "Q"
#     to_plot2.append(f_sol)
#     to_plot = np.concatenate(to_plot, axis=1)
#     to_plot2 = np.concatenate(to_plot2, axis=1)
        
#     cv2.imwrite(path+"/"+str(id)+".png", to_plot)
    
#     fig = plt.figure(figsize=(18, 18))
#     plt.clf()
#     ax = fig.add_subplot(111)
#     plt.axis('off')
#     res = ax.imshow(np.array(to_plot), cmap=plt.cm.jet, 
#                     interpolation='nearest')
#     plt.tight_layout()

#     width, height = to_plot2.shape

#     for x in xrange(width):
#         for y in xrange(height):
#             ax.annotate(str(to_plot2[x][y]), xy=(y, x), 
#                         horizontalalignment='center',
#                         verticalalignment='center')

#     plt.savefig(path+"/plt_"+str(id)+".png")

# def genetic_algorithm_main(tot_gen = 10000, init_pop_size=16, mut_prob = 0.1, total_time=100000, debug = False):
#     n_solved = 0
#     for i in range(tot_gen):
#         init_pop = []
#         for j in range(init_pop_size):
#             init_state = np.zeros((8,2)).astype(np.int32)
#             for j in range(8):
#                 init_state[j,0] = j+1
#                 init_state[j,1] = np.random.randint(1,9)
#             init_state_str = encode_state_str_2(init_state)
#             init_pop.append(init_state_str)
#         x, tot_path = genetic_algorithm(init_pop, mut_prob, total_time, debug=debug)
#         if x is not None:
#             n_solved += 1
#             #print get_queen_board(decode_state_str_2(x))
#             temp = np.zeros((init_pop_size*(9),9))+125
#             temp[:8,:8] = get_queen_board(decode_state_str_2(x))*255
#             #plot3(tot_path, "plots/genetic/", init_pop_size, temp, i)
#             plot3([init_pop, tot_path[-1]], "plots/genetic/", init_pop_size, temp, i)
#     return n_solved, tot_gen

# def ex4():
#     a,b = genetic_algorithm_main(tot_gen = 100, debug=False)
#     print a,b,(1.0*a)/b
# '''
# np.random.seed(2)
# print "With consistent heuristic"
# my_init_states = ex1_and_2(None)
# print "With incons heuristic"
# incons = True
# ex1_and_2(my_init_states)
# '''
# np.random.seed(2)
# ex3()
# np.random.seed(2)
# ex4()