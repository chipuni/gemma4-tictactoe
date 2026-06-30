import random
from typing import List
from board import Board

class TicTacToeAI:
    def __init__(self, difficulty='Hard'):
        self.difficulty = difficulty # 'Easy', 'Medium', 'Hard'

    def get_move(self, board: Board) -> int:
        if self.difficulty == 'Easy':
            return self._random_move(board)
        elif self.difficulty == 'Medium':
            if random.random() < 0.4:
                return self._random_move(board)
            return self._best_move(board)
        else: # Hard
            return self._best_move(board)

    def _random_move(self, board: Board) -> int:
        available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
        return random.choice(available_moves) if available_moves else -1

    def _best_move(self, board: Board) -> int:
        best_score = -float('inf')
        best_move = -1
        
        # Set search depth based on board size to keep it responsive
        search_depth = 6 if board.size > 3 else 9
        
        available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
        if not available_moves: return -1

        # Heuristic: prioritize center
        center = (board.size * board.size) // 2
        if center in available_moves:
            # We still check if it's a good move via minimax, but could be an optimization
            pass

        for move in available_moves:
            board.cells[move] = 'O'
            score = self._minimax(board, 0, False, -float('inf'), float('inf'), search_depth)
            board.cells[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move if best_move != -1 else self._random_move(board)

    def _evaluate_board(self, board: Board) -> int:
        winner = board.check_winner()
        if winner == 'O': return 100
        if winner == 'X': return -100
        return 0

    def _minimax(self, board: Board, depth: int, is_maximizing: bool, alpha: float, beta: float, max_depth: int) -> int:
        winner = board.check_winner()
        if winner == 'O': return 100 - depth
        if winner == 'X': return depth - 100
        if winner == 'Draw': return 0
        if depth >= max_depth:
            return self._evaluate_board(board)

        if is_maximizing:
            max_eval = -float('inf')
            for i in range(len(board.cells)):
                if board.cells[i] == ' ':
                    board.cells[i] = 'O'
                    eval_score = self._minimax(board, depth + 1, False, alpha, beta, max_depth)
                    board.cells[i] = ' '
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(len(board.cells)):
                if board.cells[i] == ' ':
                    board.cells[i] = 'X'
                    eval_score = self._minimax(board, depth + 1, True, alpha, beta, max_depth)
                    board.cells[i] = ' '
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval
