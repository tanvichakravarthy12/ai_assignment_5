class TicTacToeState:
    # TTT win lines
    WIN_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    def __init__(self, board=None, current_player=1):
        if board is None:
            self.board = (0,) * 9
        else:
            self.board = board
        self.current_player = current_player
        self._winner = self._compute_winner()

    def get_legal_moves(self):
        if self._winner is not None:
            return []
        moves = []
        for i in range(9):
            if self.board[i] == 0:
                moves.append(i)
        return moves

    def make_move(self, move):
        new_board = list(self.board)
        new_board[move] = self.current_player
        return TicTacToeState(tuple(new_board), -self.current_player)

    def is_terminal(self):
        return self._winner is not None

    def get_winner(self):
        return self._winner

    def get_current_player(self):
        return self.current_player

    def get_utility(self, player):
        if self._winner is None:
            return 0.0
        if self._winner == player:
            return 1000000.0
        if self._winner == -player:
            return -1000000.0
        return 0.0

    def _compute_winner(self):
        for a, b, c in self.WIN_LINES:
            total = self.board[a] + self.board[b] + self.board[c]
            if total == 3:
                return 1
            if total == -3:
                return -1
        if 0 not in self.board:
            return 0
        return None

    def to_string(self):
        symbols = {0: ".", 1: "X", -1: "O"}
        lines = []
        for r in range(3):
            row = [symbols[self.board[r * 3 + c]] for c in range(3)]
            lines.append(" | ".join(row))
        return "\n---------\n".join(lines)


class ConnectFourState:
    ROWS = 6
    COLS = 7
    WIN_LINES = []

    if not WIN_LINES:
        for r in range(6):
            for c in range(4):
                WIN_LINES.append((r * 7 + c, r * 7 + c + 1, r * 7 + c + 2, r * 7 + c + 3))
        for r in range(3):
            for c in range(7):
                WIN_LINES.append((r * 7 + c, (r + 1) * 7 + c, (r + 2) * 7 + c, (r + 3) * 7 + c))
        for r in range(3):
            for c in range(4):
                WIN_LINES.append((r * 7 + c, (r + 1) * 7 + c + 1, (r + 2) * 7 + c + 2, (r + 3) * 7 + c + 3))
        for r in range(3, 6):
            for c in range(4):
                WIN_LINES.append((r * 7 + c, (r - 1) * 7 + c + 1, (r - 2) * 7 + c + 2, (r - 3) * 7 + c + 3))

    def __init__(self, board=None, current_player=1):
        if board is None:
            self.board = (0,) * 42
        else:
            self.board = board
        self.current_player = current_player
        self._winner = self._compute_winner()

    def get_legal_moves(self):
        if self._winner is not None:
            return []
        moves = []
        for c in range(7):
            if self.board[c] == 0:
                moves.append(c)
        return moves

    def make_move(self, move):
        new_board = list(self.board)
        for r in range(5, -1, -1):
            idx = r * 7 + move
            if new_board[idx] == 0:
                new_board[idx] = self.current_player
                break
        return ConnectFourState(tuple(new_board), -self.current_player)

    def is_terminal(self):
        return self._winner is not None

    def get_winner(self):
        return self._winner

    def get_current_player(self):
        return self.current_player

    def get_utility(self, player):
        if self._winner is None:
            return 0.0
        if self._winner == player:
            return 1000000.0
        if self._winner == -player:
            return -1000000.0
        return 0.0

    def _compute_winner(self):
        for a, b, c, d in self.WIN_LINES:
            total = self.board[a] + self.board[b] + self.board[c] + self.board[d]
            if total == 4:
                return 1
            if total == -4:
                return -1
        if 0 not in self.board[:7]:
            return 0
        return None

    def to_string(self):
        symbols = {0: ".", 1: "X", -1: "O"}
        lines = []
        for r in range(6):
            row = [symbols[self.board[r * 7 + c]] for c in range(7)]
            lines.append("  ".join(row))
        header = "  ".join(str(c) for c in range(7))
        return "\n".join(lines) + "\n---------------------\n" + header
