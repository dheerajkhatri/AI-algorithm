from itertools import permutations
import random
import numpy as np

class TIC():
    rows  = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    cols  = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
    diags = [[0, 4, 8], [6, 4, 2]]
    lines = rows + cols + diags
    my_board_frame = "---|---|---\n".join([" {} | {} | {}\n"] * 3)    
    total_node_count = 0
    max_depth = 0
    to_print_bf = False
    action_ordering = False
    complete_path = []

    def display_board(self,X):
        current_board = self.my_board_frame.format(*[y or a for a, y in enumerate(X)])
        print current_board
        ret = []
        count = 0
        for x in X:
            if x:
                if x == 'X':
                    ret.append(-1)
                else:
                    ret.append(-2)
            else:
                ret.append(0)
            count += 1
        return np.asarray(ret).reshape((3,3))

    def get_current_state(self,current_inst):
        threes = list({ self.apply_triplet(current_inst, line) for line in self.lines } - { None })
        if len(threes) == 1 and self.get_turn_player(current_inst) != threes[0]:
            return threes[0]
        elif len(threes) == 0:
            return 'tie' if current_inst.count(None) == 0 else 'continue'
        else:
            return False

    def apply_triplet(self,current_inst, line):
        marks = [current_inst[i] for i in line if current_inst[i]]
        return marks[0] if len(marks) == 3 and len(set(marks)) == 1 else None

    def get_turn_player(self,current_inst):
        xc = current_inst.count('X')
        oc = current_inst.count('O')
        return 'XO'[xc-oc]    

    def actions_possible(self,current_inst):
        mark = self.get_turn_player(current_inst)
        succ_order = range(9)
        if self.action_ordering:
            np.random.seed(5)
            np.random.shuffle(succ_order)
        for i in filter(lambda x: current_inst[x] == None, succ_order):
            new = current_inst[:i] + (mark,) + current_inst[i+1:]
            if self.get_current_state(new): yield i, new

    def apply_alphabeta(self,current_inst, a=float('-inf'), b=float('inf'), m_depth=0):        
        self.max_depth = max(m_depth+1, self.max_depth)
        self.total_node_count += 1
        my_state = self.get_current_state(current_inst)
        if   my_state == 'X': return 1
        elif my_state == 'O': return -1
        elif my_state == 'tie': return 0
        elif my_state == 'continue':
            if self.get_turn_player(current_inst) == 'X':
                for m, p in self.actions_possible(current_inst):
                    a = max(a, self.apply_alphabeta(p, a, b, m_depth+1))
                    if b <= a: break
                return a
            else:
                for m, p in self.actions_possible(current_inst):
                    b = min(b, self.apply_alphabeta(p, a, b, m_depth+1))
                    if b <= a: break
                return b

    def get_best_action(self,current_inst):
        bestScore = None
        best_actions = None
        player = self.get_turn_player(current_inst)
        def better(s):
            return s > bestScore if player == 'X' else s < bestScore
                
        self.total_node_count = 1
        self.max_depth = 0
        for m, p in self.actions_possible(current_inst):
            score = self.apply_alphabeta(p)
            if bestScore is None or better(score):
                bestScore = score
                best_actions = [ m ]
            elif score == bestScore:
                best_actions.append(m)
        if self.to_print_bf:
            print "First action by computer (using alpha-beta pruning) \nTotal Nodes generated:", self.total_node_count, "\nDepth:", self.max_depth, "\nEffective branching factor (N^(1/d)): ", pow(self.total_node_count, 1.0/self.max_depth)
        return random.choice(best_actions)

    def play(self,opponent, current_inst):
        global complete_path
        complete_path = []
        while self.get_current_state(current_inst) == 'continue':
            if not self.to_print_bf:
                complete_path.append(self.display_board(current_inst))
            if self.get_turn_player(current_inst) == opponent:
                action = int(raw_input("Your action: "))
            else:
                action = self.get_best_action(current_inst)
            current_inst = current_inst[:action] + (self.get_turn_player(current_inst),)+current_inst[action+1:]
            if self.to_print_bf:
                break
        if not self.to_print_bf:
            self.display_output(current_inst, opponent)

    def display_output(self,current_inst, opponent):        
        self.complete_path.append(self.display_board(current_inst))
        my_state = self.get_current_state(current_inst)
        if my_state == opponent:
            print("You win.")
        elif my_state == 'tie':
            print("Tie.")
        else:
            print("I win.")

    def get_eff_factor(self):        
        self.to_print_bf = True
        self.play("O", (None,) * 9)
        self.to_print_bf = False

    def get_eff_after_action_ordering(self):
        print "After action ordering (random successor exploration)"        
        self.action_ordering = True
        self.to_print_bf = True
        self.play("O", (None,) * 9)
        self.to_print_bf = False
        self.action_ordering = False


if __name__ == '__main__':
    game = TIC()
    game.get_eff_factor()
    game.get_eff_after_action_ordering()
    print '*'*80
    print 'X will be the first player'
    print '*'*80
    x = raw_input('O or X? ')
    game.play(x, (None,) * 9)