from itertools import permutations
import random
import sys
import numpy as np
import matplotlib.pyplot as plt

rows  = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
cols  = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
diags = [[0, 4, 8], [6, 4, 2]]
lines = rows + cols + diags

board_fmt = "---|---|---\n".join([" {} | {} | {}\n"] * 3)


def plot1(decoded_tot_path, path="plots/ttt/", id=0):
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

def show(p):
    snapshot = board_fmt.format(*[x or i for i, x in enumerate(p)])
    print snapshot
    ret = []
    cnt = 0
    for x in p:
        if x:
            if x == 'X':
                ret.append(-1)
            else:
                ret.append(-2)
        else:
            ret.append(cnt)
        cnt += 1
    return np.asarray(ret).reshape((3,3))

def game_state(position):
    threes = list({ three_in_a_row(position, line) for line in lines } - { None })
    if len(threes) == 1 and to_play(position) != threes[0]:
        return threes[0]
    elif len(threes) == 0:
        return 'draw' if position.count(None) == 0 else 'in_progress'
    else:
        return False

def three_in_a_row(position, line):
    marks = [ position[i] for i in line if position[i] ]
    return marks[0] if len(marks) == 3 and len(set(marks)) == 1 else None

def to_play(position):
    return 'XO'[position.count('X') - position.count('O')]

num_nodes_generated = 0
max_depth = 0
to_print_bf = False
move_ordering = False
tot_path = []

def possible_moves(position):
    mark = to_play(position)
    succ_order = range(9)
    if move_ordering:
        np.random.seed(2)
        np.random.shuffle(succ_order)
    for i in filter(lambda x: position[x] == None, succ_order):
        new = position[:i] + (mark,) + position[i+1:]
        if game_state(new): yield i, new

def alphabeta(position, a=float('-inf'), b=float('inf'), m_depth=0):
    global num_nodes_generated
    global max_depth
    max_depth = max(m_depth+1, max_depth)
    num_nodes_generated += 1
    state = game_state(position)
    if   state == 'X': return 1
    elif state == 'O': return -1
    elif state == 'draw': return 0
    elif state == 'in_progress':
        if to_play(position) == 'X':
            for m, p in possible_moves(position):
                a = max(a, alphabeta(p, a, b, m_depth+1))
                if b <= a: break
            return a
        else:
            for m, p in possible_moves(position):
                b = min(b, alphabeta(p, a, b, m_depth+1))
                if b <= a: break
            return b

def search(position):
    best_score = None
    best_moves = None

    player = to_play(position)

    def better(s):
        return s > best_score if player == 'X' else s < best_score
    
    global num_nodes_generated
    global max_depth
    global to_print_bf
    num_nodes_generated = 1
    max_depth = 0
    for m, p in possible_moves(position):
        score = alphabeta(p)
        if best_score is None or better(score):
            best_score = score
            best_moves = [ m ]
        elif score == best_score:
            best_moves.append(m)
    if to_print_bf:
        print "With first move to be chosen by computer (using alpha beta pruning) \nNodes generated:", num_nodes_generated, "\nDepth:", max_depth, "\nEffective branching factor (N^(1/d)): ", pow(num_nodes_generated, 1.0/max_depth)
    return random.choice(best_moves)

def play(human, position):
    global tot_path
    tot_path = []
    while game_state(position) == 'in_progress':
        if not to_print_bf:
            tot_path.append(show(position))
        if to_play(position) == human:
            move = int(raw_input("Move: "))
        else:
            move = search(position)
        position = position[:move] + (to_play(position),) + position[move+1:]
        if to_print_bf:
            break
    if not to_print_bf:
        show_result(position, human)

def show_result(position, human):
    global tot_path
    tot_path.append(show(position))
    state = game_state(position)
    if state == human:
        print("You win.")
    elif state == 'draw':
        print("Tie.")
    else:
        print("I win.")

def compute_eff_branching_factor():
    global to_print_bf
    to_print_bf = True
    play("O", (None,) * 9)
    to_print_bf = False

def compute_eff_branching_factor_after_move_ordering():
    print "After move ordering (random successor exploration)"
    global move_ordering
    global to_print_bf
    move_ordering = True
    to_print_bf = True
    play("O", (None,) * 9)
    to_print_bf = False
    move_ordering = False

compute_eff_branching_factor()
compute_eff_branching_factor_after_move_ordering()
print '*'*80
print 'Lets play Now!\nX will be the first player'
print '*'*80
x = raw_input('O or X? ')
play(x, (None,) * 9)
plot1(tot_path)