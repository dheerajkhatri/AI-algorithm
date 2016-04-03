import random
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations

def plot1(decoded_tot_path, path="plots/ttt/", id=0):
    to_plot = []
    to_plot2 = []
    annotatations = []
    for i in range(len(decoded_tot_path)):
        temp = decoded_tot_path[i]+2
        temp = temp * 100 + 50
        temp2 = np.zeros((3,4)).astype(np.int32)
        temp2[:,:-1] = temp
        to_plot.append(temp2.copy())
        temp2 = temp2*0-3
        temp2[:,:-1] = decoded_tot_path[i]
        temp2 = temp2.astype('str')
        temp2[temp2=="-1"] = "X"
        temp2[temp2=="-2"] = "O"
        temp2[temp2=="-3"] = " "
        temp2[temp2=="0"] = " "
        to_plot2.append(temp2)
        
    to_plot = np.concatenate(to_plot, axis=1)
    to_plot2 = np.concatenate(to_plot2, axis=1)
    
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

    plt.savefig(path+"/init_plt_"+str(id)+".png")

rows  = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
cols  = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
diags = [[0, 4, 8], [6, 4, 2]]
lines = rows + cols + diags

my_board = "---|---|---\n".join([" {} | {} | {}\n"] * 3)


def display(X):
    snapshot = my_board.format(*[y or a for a, y in enumerate(X)])
    print snapshot
    ret = []
    cnt = 0
    for x in X:
        if x:
            if x == 'X':
                ret.append(-1)
            else:
                ret.append(-2)
        else:
            ret.append(0)
        cnt += 1
    return np.asarray(ret).reshape((3,3))

def get_state_of_game(instance):
    threes = list({ triplet(instance, line) for line in lines } - { None })
    if len(threes) == 1 and whose_turn(instance) != threes[0]:
        return threes[0]
    elif len(threes) == 0:
        return 'draw' if instance.count(None) == 0 else 'is_on'
    else:
        return False

def triplet(instance, line):
    marks = [instance[i] for i in line if instance[i]]
    return marks[0] if len(marks) == 3 and len(set(marks)) == 1 else None

def whose_turn(instance):
    xc = instance.count('X')
    oc = instance.count('O')
    return 'XO'[xc-oc]

num_nodes_generated = 0
max_depth = 0
to_print_bf = False
action_ordering = False
tot_path = []

def get_possible_actions(instance):
    mark = whose_turn(instance)
    succ_order = range(9)
    if action_ordering:
        np.random.seed(2)
        np.random.shuffle(succ_order)
    for i in filter(lambda x: instance[x] == None, succ_order):
        new = instance[:i] + (mark,) + instance[i+1:]
        if get_state_of_game(new): yield i, new

def alphabeta_pruning(instance, a=float('-inf'), b=float('inf'), m_depth=0):
    global num_nodes_generated
    global max_depth
    max_depth = max(m_depth+1, max_depth)
    num_nodes_generated += 1
    my_state = get_state_of_game(instance)
    if   my_state == 'X': return 1
    elif my_state == 'O': return -1
    elif my_state == 'draw': return 0
    elif my_state == 'is_on':
        if whose_turn(instance) == 'X':
            for m, p in get_possible_actions(instance):
                a = max(a, alphabeta_pruning(p, a, b, m_depth+1))
                if b <= a: break
            return a
        else:
            for m, p in get_possible_actions(instance):
                b = min(b, alphabeta_pruning(p, a, b, m_depth+1))
                if b <= a: break
            return b

def get_best_action(instance):
    best_score = None
    best_actions = None
    player = whose_turn(instance)
    def better(s):
        return s > best_score if player == 'X' else s < best_score
    
    global num_nodes_generated
    global max_depth
    global to_print_bf
    num_nodes_generated = 1
    max_depth = 0
    for m, p in get_possible_actions(instance):
        score = alphabeta_pruning(p)
        if best_score is None or better(score):
            best_score = score
            best_actions = [ m ]
        elif score == best_score:
            best_actions.append(m)
    if to_print_bf:
        print "With first action to be chosen by computer (using alpha beta pruning) \nNodes generated:", num_nodes_generated, "\nDepth:", max_depth, "\nEffective branching factor (N^(1/d)): ", pow(num_nodes_generated, 1.0/max_depth)
    return random.choice(best_actions)

def play(human, instance):
    global tot_path
    tot_path = []
    while get_state_of_game(instance) == 'is_on':
        if not to_print_bf:
            tot_path.append(display(instance))
        if whose_turn(instance) == human:
            action = int(raw_input("Your action: "))
        else:
            action = get_best_action(instance)
        instance = instance[:action] + (whose_turn(instance),)+instance[action+1:]
        if to_print_bf:
            break
    if not to_print_bf:
        display_output(instance, human)

def display_output(instance, human):
    global tot_path
    tot_path.append(display(instance))
    my_state = get_state_of_game(instance)
    if my_state == human:
        print("You win.")
    elif my_state == 'draw':
        print("Tie.")
    else:
        print("I win.")

def compute_eff_branching_factor():
    global to_print_bf
    to_print_bf = True
    play("O", (None,) * 9)
    to_print_bf = False

def compute_eff_branching_factor_after_action_ordering():
    print "After action ordering (random successor exploration)"
    global action_ordering
    global to_print_bf
    action_ordering = True
    to_print_bf = True
    play("O", (None,) * 9)
    to_print_bf = False
    action_ordering = False

compute_eff_branching_factor()
compute_eff_branching_factor_after_action_ordering()
print '*'*80
print 'Lets play Now!\nX will be the first player'
print '*'*80
x = raw_input('O or X? ')
play(x, (None,) * 9)
plot1(tot_path)