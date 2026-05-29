import math
import random

def sort_moves(state, legal_moves, player):
    # Sort moves to improve pruning
    if hasattr(state, 'COLS') and state.COLS == 7:
        return sorted(legal_moves, key=lambda col: abs(col - 3))
    elif len(legal_moves) <= 9:
        pref = {4: 0, 0: 1, 2: 1, 6: 1, 8: 1, 1: 2, 3: 2, 5: 2, 7: 2}
        return sorted(legal_moves, key=lambda m: pref.get(m, 3))
    return legal_moves


# Minimax
def minimax_search(state):
    nodes_visited = [0]
    player = state.get_current_player()

    def search(s, depth):
        nodes_visited[0] += 1
        
        if s.is_terminal():
            utility = s.get_utility(player)
            if utility > 0:
                return utility - 1000.0 * depth, None
            elif utility < 0:
                return utility + 1000.0 * depth, None
            return 0.0, None

        moves = s.get_legal_moves()
        is_max = s.get_current_player() == player

        if is_max:
            best_val = -float('inf')
            best_move = None
            for m in moves:
                val, _ = search(s.make_move(m), depth + 1)
                if val > best_val:
                    best_val = val
                    best_move = m
            return best_val, best_move
        else:
            best_val = float('inf')
            best_move = None
            for m in moves:
                val, _ = search(s.make_move(m), depth + 1)
                if val < best_val:
                    best_val = val
                    best_move = m
            return best_val, best_move

    val, move = search(state, 0)
    return val, move, nodes_visited[0]


# Alpha-Beta 
def alpha_beta_search(state):
    nodes_visited = [0]
    player = state.get_current_player()

    def search(s, depth, alpha, beta):
        nodes_visited[0] += 1
        
        if s.is_terminal():
            utility = s.get_utility(player)
            if utility > 0:
                return utility - 1000.0 * depth, None
            elif utility < 0:
                return utility + 1000.0 * depth, None
            return 0.0, None

        moves = s.get_legal_moves()
        sorted_moves = sort_moves(s, moves, player)
        is_max = s.get_current_player() == player

        if is_max:
            best_val = -float('inf')
            best_move = None
            for m in sorted_moves:
                val, _ = search(s.make_move(m), depth + 1, alpha, beta)
                if val > best_val:
                    best_val = val
                    best_move = m
                alpha = max(alpha, best_val)
                if best_val >= beta:
                    break
            return best_val, best_move
        else:
            best_val = float('inf')
            best_move = None
            for m in sorted_moves:
                val, _ = search(s.make_move(m), depth + 1, alpha, beta)
                if val < best_val:
                    best_val = val
                    best_move = m
                beta = min(beta, best_val)
                if best_val <= alpha:
                    break
            return best_val, best_move

    val, move = search(state, 0, -float('inf'), float('inf'))
    return val, move, nodes_visited[0]


# Heuristic Alpha-Beta 
def heuristic_alpha_beta_search(state, max_depth, heuristic_func):
    nodes_visited = [0]
    player = state.get_current_player()

    def search(s, depth, alpha, beta):
        nodes_visited[0] += 1
        
        if s.is_terminal():
            utility = s.get_utility(player)
            if utility > 0:
                return utility - 1000.0 * depth, None
            elif utility < 0:
                return utility + 1000.0 * depth, None
            return 0.0, None
            
        if depth >= max_depth:
            return heuristic_func(s, player), None

        moves = s.get_legal_moves()
        sorted_moves = sort_moves(s, moves, player)
        is_max = s.get_current_player() == player

        if is_max:
            best_val = -float('inf')
            best_move = None
            for m in sorted_moves:
                val, _ = search(s.make_move(m), depth + 1, alpha, beta)
                if val > best_val:
                    best_val = val
                    best_move = m
                alpha = max(alpha, best_val)
                if best_val >= beta:
                    break
            return best_val, best_move
        else:
            best_val = float('inf')
            best_move = None
            for m in sorted_moves:
                val, _ = search(s.make_move(m), depth + 1, alpha, beta)
                if val < best_val:
                    best_val = val
                    best_move = m
                beta = min(beta, best_val)
                if best_val <= alpha:
                    break
            return best_val, best_move

    val, move = search(state, 0, -float('inf'), float('inf'))
    return val, move, nodes_visited[0]


# Heuristic Evaluation 
def tictactoe_heuristic(state, player):
    winner = state.get_winner()
    if winner is not None:
        if winner == player: return 100000.0
        elif winner == -player: return -100000.0
        return 0.0

    score = 0.0
    b = state.board
    for line in state.WIN_LINES:
        cells = [b[idx] for idx in line]
        p_count = cells.count(player)
        o_count = cells.count(-player)
        e_count = cells.count(0)

        if p_count == 2 and e_count == 1:
            score += 10.0
        elif p_count == 1 and e_count == 2:
            score += 1.0
        elif o_count == 2 and e_count == 1:
            score -= 10.0
        elif o_count == 1 and e_count == 2:
            score -= 1.0
    return score


def connectfour_heuristic(state, player):
    winner = state.get_winner()
    if winner is not None:
        if winner == player: return 1000000.0
        elif winner == -player: return -1000000.0
        return 0.0

    score = 0.0
    b = state.board
    for a, cb, c, d in state.WIN_LINES:
        cells = [b[a], b[cb], b[c], b[d]]
        p_count = cells.count(player)
        o_count = cells.count(-player)
        e_count = cells.count(0)

        if p_count == 3 and e_count == 1:
            score += 50.0
        elif p_count == 2 and e_count == 2:
            score += 10.0
        elif o_count == 3 and e_count == 1:
            score -= 100.0
        elif o_count == 2 and e_count == 2:
            score -= 10.0

    center_cells = [r * 7 + 3 for r in range(6)]
    for idx in center_cells:
        if b[idx] == player: score += 4.0
        elif b[idx] == -player: score -= 4.0
    return score


# Monte Carlo tree search 
class MCTSNode:
    def __init__(self, state, parent=None, move_leading_here=None):
        self.state = state
        self.parent = parent
        self.move_leading_here = move_leading_here
        self.children = {}
        self.n = 0
        self.q = 0.0
        self.untried_moves = state.get_legal_moves()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal(self):
        return self.state.is_terminal()


def mcts_search(state, iterations=1000, exploration_const=1.414):
    root = MCTSNode(state)
    nodes_visited = 1

    for _ in range(iterations):
        node = root
        while not node.is_terminal() and node.is_fully_expanded():
            best_score = -float('inf')
            best_child = None
            n_p = node.n
            for child in node.children.values():
                exploit = child.q / child.n
                explore = exploration_const * math.sqrt(math.log(n_p) / child.n)
                uct = exploit + explore
                if uct > best_score:
                    best_score = uct
                    best_child = child
            node = best_child

        if not node.is_terminal():
            move = node.untried_moves.pop()
            next_state = node.state.make_move(move)
            child = MCTSNode(next_state, parent=node, move_leading_here=move)
            node.children[move] = child
            node = child
            nodes_visited += 1

        sim_state = node.state
        while not sim_state.is_terminal():
            moves = sim_state.get_legal_moves()
            sim_state = sim_state.make_move(random.choice(moves))

        winner = sim_state.get_winner()
        curr = node
        while curr is not None:
            curr.n += 1
            if curr.parent is not None:
                parent_player = curr.parent.state.get_current_player()
                if winner == 0: reward = 0.0
                elif winner == parent_player: reward = 1.0
                else: reward = -1.0
                curr.q += reward
            curr = curr.parent

    if not root.children:
        legal = state.get_legal_moves()
        return (legal[0] if legal else None), nodes_visited

    best_move = max(root.children.items(), key=lambda item: item[1].n)[0]
    return best_move, nodes_visited
