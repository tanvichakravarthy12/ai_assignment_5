import unittest
import random
from game import TicTacToeState, ConnectFourState
from search import (
    minimax_search,
    alpha_beta_search,
    heuristic_alpha_beta_search,
    mcts_search,
    tictactoe_heuristic,
    connectfour_heuristic
)

class TestSearchAlgorithms(unittest.TestCase):
    def setUp(self):
        print("Running test:", self._testMethodName)

    def tearDown(self):
        print("Passed test:", self._testMethodName)
        print()


class TestTicTacToe(TestSearchAlgorithms):
    def test_initial_state(self):
        state = TicTacToeState()
        self.assertEqual(len(state.get_legal_moves()), 9)
        self.assertEqual(state.get_current_player(), 1)
        self.assertFalse(state.is_terminal())
        self.assertIsNone(state.get_winner())

    def test_win_detection(self):
        board = (
            1,  1,  1,
            -1, 0, -1,
            0,  0,  0
        )
        state = TicTacToeState(board, current_player=-1)
        self.assertTrue(state.is_terminal())
        self.assertEqual(state.get_winner(), 1)
        self.assertEqual(state.get_utility(1), 1000000.0)
        self.assertEqual(state.get_utility(-1), -1000000.0)

    def test_draw_detection(self):
        board = (
            1, -1,  1,
            1, -1, -1,
           -1,  1,  1
        )
        state = TicTacToeState(board, current_player=1)
        self.assertTrue(state.is_terminal())
        self.assertEqual(state.get_winner(), 0)

    def test_immediate_win_ttt(self):
        board = (
            1,  1,  0,
           -1, -1,  0,
            0,  0,  0
        )
        state = TicTacToeState(board, current_player=1)
        
        # Test Minimax
        _, move_m, nodes_m = minimax_search(state)
        print("Minimax move:", move_m, "nodes:", nodes_m)
        self.assertEqual(move_m, 2)

        # Test Alpha-Beta
        _, move_ab, nodes_ab = alpha_beta_search(state)
        print("Alpha-Beta move:", move_ab, "nodes:", nodes_ab)
        self.assertEqual(move_ab, 2)

        # Test Heuristic Alpha-Beta
        _, move_hab, nodes_hab = heuristic_alpha_beta_search(state, max_depth=2, heuristic_func=tictactoe_heuristic)
        print("Heuristic move:", move_hab, "nodes:", nodes_hab)
        self.assertEqual(move_hab, 2)

        # Test MCTS
        move_mcts, nodes_mcts = mcts_search(state, iterations=800)
        print("MCTS move:", move_mcts, "iterations:", nodes_mcts)
        self.assertEqual(move_mcts, 2)

    def test_defensive_block_ttt(self):
        board = (
           -1, -1,  0,
            1,  0,  0,
            0,  0,  0
        )
        state = TicTacToeState(board, current_player=1)

        _, move_m, nodes_m = minimax_search(state)
        print("Minimax block:", move_m, "nodes:", nodes_m)
        self.assertEqual(move_m, 2)

        _, move_ab, nodes_ab = alpha_beta_search(state)
        print("Alpha-Beta block:", move_ab, "nodes:", nodes_ab)
        self.assertEqual(move_ab, 2)

        _, move_hab, nodes_hab = heuristic_alpha_beta_search(state, max_depth=3, heuristic_func=tictactoe_heuristic)
        print("Heuristic block:", move_hab, "nodes:", nodes_hab)
        self.assertEqual(move_hab, 2)

        move_mcts, nodes_mcts = mcts_search(state, iterations=1000)
        print("MCTS block:", move_mcts, "iterations:", nodes_mcts)
        self.assertEqual(move_mcts, 2)


class TestConnectFour(TestSearchAlgorithms):
    def test_drop_physics(self):
        state = ConnectFourState()
        next_state = state.make_move(3)
        self.assertEqual(next_state.board[38], 1)
        self.assertEqual(next_state.get_current_player(), -1)

    def test_win_horizontal(self):
        board = [0] * 42
        for c in range(4):
            board[5 * 7 + c] = 1
        state = ConnectFourState(tuple(board), current_player=-1)
        self.assertTrue(state.is_terminal())
        self.assertEqual(state.get_winner(), 1)

    def test_win_vertical(self):
        board = [0] * 42
        for r in range(2, 6):
            board[r * 7 + 0] = -1
        state = ConnectFourState(tuple(board), current_player=1)
        self.assertTrue(state.is_terminal())
        self.assertEqual(state.get_winner(), -1)

    def test_immediate_win_c4(self):
        board = [0] * 42
        board[5 * 7 + 0] = 1
        board[4 * 7 + 0] = 1
        board[3 * 7 + 0] = 1
        state = ConnectFourState(tuple(board), current_player=1)

        # Test Heuristic Alpha-Beta
        _, move_hab, nodes_hab = heuristic_alpha_beta_search(state, max_depth=3, heuristic_func=connectfour_heuristic)
        print("Heuristic move:", move_hab, "nodes:", nodes_hab)
        self.assertEqual(move_hab, 0)

        # Test MCTS
        move_mcts, nodes_mcts = mcts_search(state, iterations=800)
        print("MCTS move:", move_mcts, "iterations:", nodes_mcts)
        self.assertEqual(move_mcts, 0)

    def test_defensive_block_c4(self):
        board = [0] * 42
        board[5 * 7 + 4] = -1
        board[4 * 7 + 4] = -1
        board[3 * 7 + 4] = -1
        state = ConnectFourState(tuple(board), current_player=1)

        # Test Heuristic Alpha-Beta
        _, move_hab, nodes_hab = heuristic_alpha_beta_search(state, max_depth=4, heuristic_func=connectfour_heuristic)
        print("Heuristic block:", move_hab, "nodes:", nodes_hab)
        self.assertEqual(move_hab, 4)

        # Test MCTS
        move_mcts, nodes_mcts = mcts_search(state, iterations=1000)
        print("MCTS block:", move_mcts, "iterations:", nodes_mcts)
        self.assertEqual(move_mcts, 4)


def play_game_interactive():
    print("====================================")
    print("     SEARCH ALGORITHMS PLAYGROUND   ")
    print("====================================")
    print("Select a game:")
    print("1. Tic-Tac-Toe")
    print("2. Connect Four")
    try:
        game_choice = input("Enter choice (1 or 2): ").strip()
    except (KeyboardInterrupt, SystemExit):
        return

    if game_choice not in ["1", "2"]:
        print("Invalid choice. Exiting.")
        return

    print("\nSelect AI Algorithm to play against:")
    print("1. Minimax Search")
    print("2. Alpha-Beta Pruning Search")
    print("3. Heuristic Alpha-Beta Search (depth limited)")
    print("4. Monte-Carlo Tree Search (MCTS)")
    try:
        algo_choice = input("Enter choice (1-4): ").strip()
    except (KeyboardInterrupt, SystemExit):
        return

    if algo_choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Exiting.")
        return

    print("\nChoose your turn:")
    print("1. Go first (Player X)")
    print("2. Go second (Player O)")
    try:
        turn_choice = input("Enter choice (1 or 2): ").strip()
    except (KeyboardInterrupt, SystemExit):
        return

    if turn_choice not in ["1", "2"]:
        print("Invalid choice. Exiting.")
        return

    human_player = 1 if turn_choice == "1" else -1

    # Initialize State
    if game_choice == "1":
        state = TicTacToeState()
        game_name = "Tic-Tac-Toe"
    else:
        state = ConnectFourState()
        game_name = "Connect Four"

    print(f"\nStarting {game_name} game against AI!")
    print(state.to_string())

    while not state.is_terminal():
        current_player = state.get_current_player()
        if current_player == human_player:
            legal = state.get_legal_moves()
            if game_choice == "1":
                prompt = f"Your turn (X/O) - Enter cell 0-8 (legal: {legal}): "
            else:
                prompt = f"Your turn (X/O) - Enter col 0-6 (legal: {legal}): "
            
            try:
                move_input = input(prompt).strip()
            except (KeyboardInterrupt, SystemExit):
                return
                
            try:
                move = int(move_input)
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue

            if move not in legal:
                print(f"Illegal move. Please choose from {legal}.")
                continue

            state = state.make_move(move)
        else:
            print("\nAI is thinking...")
            if game_choice == "1":  # TTT
                if algo_choice == "1":
                    val, move, nodes = minimax_search(state)
                    print(f"AI chose move {move} using Minimax (nodes visited: {nodes})")
                elif algo_choice == "2":
                    val, move, nodes = alpha_beta_search(state)
                    print(f"AI chose move {move} using Alpha-Beta (nodes visited: {nodes})")
                elif algo_choice == "3":
                    val, move, nodes = heuristic_alpha_beta_search(state, max_depth=3, heuristic_func=tictactoe_heuristic)
                    print(f"AI chose move {move} using Heuristic Alpha-Beta (nodes visited: {nodes})")
                else:
                    move, iterations = mcts_search(state, iterations=1000)
                    print(f"AI chose move {move} using MCTS (iterations: {iterations})")
            else:  # Connect Four
                if algo_choice == "1":
                    print("Warning: Minimax on standard Connect Four is too slow. Falling back to Alpha-Beta.")
                    val, move, nodes = alpha_beta_search(state)
                    print(f"AI chose move {move} using Alpha-Beta (nodes visited: {nodes})")
                elif algo_choice == "2":
                    val, move, nodes = alpha_beta_search(state)
                    print(f"AI chose move {move} using Alpha-Beta (nodes visited: {nodes})")
                elif algo_choice == "3":
                    val, move, nodes = heuristic_alpha_beta_search(state, max_depth=4, heuristic_func=connectfour_heuristic)
                    print(f"AI chose move {move} using Heuristic Alpha-Beta (nodes visited: {nodes})")
                else:
                    move, iterations = mcts_search(state, iterations=1000)
                    print(f"AI chose move {move} using MCTS (iterations: {iterations})")

            state = state.make_move(move)

        print("\n" + state.to_string())

    winner = state.get_winner()
    print("\nGame Over!")
    if winner == 0:
        print("Result: It is a draw!")
    elif winner == human_player:
        print("Result: Congratulations! You won!")
    else:
        print("Result: AI won!")


if __name__ == '__main__':
    print("=== SEARCH TESTS ===")
    
    import sys
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower().strip()
        if arg in ["play", "interactive"]:
            play_game_interactive()
        elif arg in ["ttt", "tictactoe"]:
            suite = unittest.TestLoader().loadTestsFromTestCase(TestTicTacToe)
            unittest.TextTestRunner().run(suite)
        elif arg in ["c4", "connectfour"]:
            suite = unittest.TestLoader().loadTestsFromTestCase(TestConnectFour)
            unittest.TextTestRunner().run(suite)
        else:
            found = False
            for test_class in [TestTicTacToe, TestConnectFour]:
                for attr in dir(test_class):
                    if attr.lower() == arg or attr.lower() == ("test_" + arg) or arg in attr.lower():
                        suite = unittest.TestSuite()
                        suite.addTest(test_class(attr))
                        unittest.TextTestRunner().run(suite)
                        found = True
                        break
                if found:
                    break
            if not found:
                print(f"Error: Unknown argument '{sys.argv[1]}'.")
    else:
        unittest.main()
