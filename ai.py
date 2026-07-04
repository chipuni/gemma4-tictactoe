import random
from typing import List, Dict, Tuple
from board import Board

class TicTacToeAI:
    def __init__(self, difficulty='Hard'):
        self.difficulty = difficulty # 'Easy', 'Medium', 'Hard'
        self.transposition_table = {}

    def get_move(self, board: Board) -> int:
        self.transposition_table.clear() 
        if self.difficulty == 'Easy':
            return self._random_move(board)
        
        # Optimization: Check for immediate win or block first
        immediate_move = self._check_immediate_move(board, 'O') # AI usually plays O
        if immediate_move != -1:
            return immediate_move

        if self.difficulty == 'Medium':
            if random.random() < 0.4:
                return self._random_move(board)
            return self._best_move(board)
        else: # Hard
            return self._best_move(board)

    def _check_immediate_move(self, board: Board, player: str) -> int:
        """Checks if there is a move that immediately wins or blocks the opponent."""
        # 1. Can I win right now?
        available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
        for move in available_moves:
            board.cells[move] = player
            if board.check_winner() == player:
                board.cells[move] = ' '
                return move
            board.cells[move] = ' '
            
        # 2. Must I block the opponent?
        opponent = 'X' if player == 'O' else 'O'
        for move in available_moves:
            board.cells[move] = opponent
            if board.check_winner() == opponent:
                board.cells[move] = ' '
                return move
            board.cells[move] = ' '
            
        return -1

    def get_suggested_move(self, board: Board) -> int:
        """Provides the optimal move for a human player (X)."""
        # We simulate as if X is playing and wants to maximize their own score.
        # In our minimax, 'O' is usually maximizing. 
        # For the hint, we can just use _best_move but adjust logic if needed.
        # Since get_move handles 'O', let's create a generic best move.
        return self._get_optimal_move(board, player='X')

    def _random_move(self, board: Board) -> int:
        available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
        return random.choice(available_moves) if available_moves else -1

    def _best_move(self, board: Board) -> int:
        available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
        if not available_moves: return -1

        # Depth increases as the game progresses or based on board size
        depth_limit = 4 if board.size > 3 else 9
        center = (board.size * board.size) // 2
        sorted_moves = sorted(available_moves, key=lambda m: abs(m - center))

        best_score = -float('inf')
        best_move = -1

        for move in sorted_moves:
            board.cells[move] = 'O'
            score = self._minimax(board, 0, False, -float('inf'), float('inf'), depth_limit)
            board.cells[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move if best_move != -1 else self._random_move(board)

    def _get_optimal_move(self, board: Board, player: str) -> int:
        best_score = -float('inf') if player == 'O' else float('inf')
        best_move = -1
        available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
        if not available_moves: return -1

        # Iterative Deepening approach to prevent long freezes on large boards
        # We start with a small depth and increase it if time permits (simplified here as fixed max)
        max_depth = 4 if board.size > 3 else 9
        
        center = (board.size * board.size) // 2
        sorted_moves = sorted(available_moves, key=lambda m: abs(m - center))

        for move in sorted_moves:
            board.cells[move] = player
            score = self._minimax(board, 0, player != 'O', -float('inf'), float('inf'), max_depth)
            board.cells[move] = ' '
            
            if player == 'O':
                if score > best_score:
                    best_score = score
                    best_move = move
            else: # Player X
                if score < best_score:
                    best_score = score
                    best_move = move
        
        return best_move if best_move != -1 else self._random_move(board)

    def _get_state_key(self, cells: List[str]) -> Tuple:
        return tuple(cells)

    def _minimax(self, board: Board, depth: int, is_maximizing: bool, alpha: float, beta: float, max_depth: int) -> int:
        state_key = (self._get_state_key(board.cells), depth, is_maximizing)
        if state_key in self.transposition_table:
            return self.transposition_table[state_key]

        winner = board.check_winner()
        if winner == 'O': return 100 - depth
        if winner == 'X': return depth - 100
        if winner == 'Draw': return 0
        if depth >= max_depth:
            return self._evaluate_board(board)

        if is_maximizing:
            max_eval = -float('inf')
            available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
            center = (board.size * board.size) // 2
            for i in sorted(available_moves, key=lambda m: abs(m - center)):
                board.cells[i] = 'O'
                eval_score = self._minimax(board, depth + 1, False, alpha, beta, max_depth)
                board.cells[i] = ' '
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            self.transposition_table[state_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
            center = (board.size * board.size) // 2
            for i in sorted(available_moves, key=lambda m: abs(m - center)):
                board.cells[i] = 'X'
                eval_score = self._minimax(board, depth + 1, True, alpha, beta, max_depth)
                board.cells[i] = ' '
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            self.transposition_table[state_key] = min_eval
            return min_eval

    def _evaluate_board(self, board: Board) -> int:
        score = 0
        lines = board.get_winning_lines()
        for line in lines:
            o_count = sum(1 for i in line if board.cells[i] == 'O')
            x_count = sum(1 for i in line if board.cells[i] == 'X')
            empty_count = len(line) - o_count - x_count
            
            # Priority to lines that are close to winning
            if o_count > 0 and x_count == 0:
                # Higher weight for lines that are almost complete
                weight = (10 ** o_count) * (board.size - empty_count)
                score += weight
            elif x_count > 0 and o_count == 0:
                # Higher weight for lines that are almost complete
                weight = (10 ** x_count) * (board.size - empty_count)
                score -= weight
            elif o_count == 0 and x_count == 0:
                # Favor center slightly more for larger boards
                score += 1
        return score


