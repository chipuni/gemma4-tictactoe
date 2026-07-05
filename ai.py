import random
import time
from typing import List, Dict, Tuple
from board import Board


class TicTacToeAI:
    def __init__(self, difficulty='Hard'):
        self.difficulty = difficulty # 'Easy', 'Medium', 'Hard'
        self.transposition_table = {}
        self._turn_start_time = 0.0

    def get_move(self, board: Board, player: str = 'O') -> int:
        self._turn_start_time = time.time() # Mark turn start for time-bounded search
        self.transposition_table.clear() 
        if self.difficulty == 'Easy':
            return self._random_move(board)
        
        # Optimization: Check for immediate win or block first
        immediate_move = self._check_immediate_move(board, player)
        if immediate_move != -1:
            return immediate_move
        
        if self.difficulty == 'Medium':
            if random.random() < 0.4:
                return self._random_move(board)
            return self._best_move(board, player)
        else: # Hard
            return self._best_move(board, player)

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

    def _best_move(self, board: Board, player: str) -> int:
        available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
        if not available_moves: return -1

        center = (board.size * board.size) // 2
        sorted_moves = sorted(available_moves, key=lambda m: abs(m - center))
        
        best_move = -1
        # Iterative Deepening: start with depth 1 and increase
        max_depth = 9 if board.size == 3 else 4
        
        for depth in range(1, max_depth + 1):
            current_best_move = -1
            best_score = -float('inf') if player == 'O' else float('inf')

            for move in sorted_moves:
                board.cells[move] = player
                score = self._minimax(board, 0, player != 'O', -float('inf'), float('inf'), depth)
                board.cells[move] = ' '

                if (player == 'O' and score > best_score) or (player == 'X' and score < best_score):
                    best_score = score
                    current_best_move = move
            
            # Update global best move for this depth level
            best_move = current_best_move
            
            # If we found a winning move at this depth, stop early
            if (player == 'O' and best_score >= 90) or (player == 'X' and best_score <= -90):
                break
                
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
        # Time-bounded search: stop if the AI has spent too much time on a single move
        # We'll check elapsed time. To do this properly, we need to pass start_time in.
        # Since modifying signatures of recursive calls is heavy, let's use a class attribute for current turn start.
        if time.time() - self._turn_start_time > 2.0: # 2 second hard cap per move depth search
            return self._evaluate_board(board)

        state_key = (self._get_state_key(board.cells), depth, is_maximizing)
        if state_key in self.transposition_table:
            return self.transposition_table[state_key]
        # ... rest of function remains same

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
        
        # Positional bonuses for center and corners
        center_idx = (board.size * board.size) // 2
        corners = [0, board.size - 1, board.size * (board.size - 1), board.size * board.size - 1]
        
        # Weight for center cell
        if board.cells[center_idx] == 'O': score += 2
        elif board.cells[center_idx] == 'X': score -= 2
        
        # Weights for corners
        for corner in corners:
            if board.cells[corner] == 'O': score += 1
            elif board.cells[corner] == 'X': score -= 1

        for line in lines:
            o_count = sum(1 for i in line if board.cells[i] == 'O')
            x_count = sum(1 for i in line if board.cells[i] == 'X')
            empty_count = len(line) - o_count - x_count
            
            if o_count > 0 and x_count == 0:
                weight = (10 ** o_count) * (board.size - empty_count)
                score += weight
            elif x_count > 0 and o_count == 0:
                weight = (10 ** x_count) * (board.size - empty_count)
                score -= weight
            elif o_count == 0 and x_count == 0:
                score += 0 # Neutral lines don't add value here
        return score


