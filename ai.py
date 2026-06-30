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
            # Mix of random and minimax
            if random.random() < 0.4:
                return self._random_move(board)
            return self._best_move(board)
        else: # Hard
            return self._best_move(board)

    def _random_move(self, board: Board) -> int:
        available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
        return random.choice(available_moves)

    def _best_move(self, board: Board) -> int:
        best_score = -float('inf')
        best_move = -1
        
        available_moves = [i for i, x in enumerate(board.cells) if x == ' ']
        for move in available_moves:
            board.cells[move] = 'O'
            # Use alpha-beta pruning for optimization
            score = self._minimax(board.cells, 0, False, -float('inf'), float('inf'))
            board.cells[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move if best_move != -1 else self._random_move(board)

    def _minimax(self, cells: List[str], depth: int, is_maximizing: bool, alpha: float, beta: float) -> int:
        # We create a temporary board to check victory without modifying state too much
        temp_board = Board()
        temp_board.cells = cells[:]
        winner = temp_board.check_winner()

        if winner == 'O': return 10 - depth
        if winner == 'X': return depth - 10
        if winner == 'Draw': return 0

        if is_maximizing:
            max_eval = -float('inf')
            for i in range(9):
                if cells[i] == ' ':
                    cells[i] = 'O'
                    eval_score = self._minimax(cells, depth + 1, False, alpha, beta)
                    cells[i] = ' '
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(9):
                if cells[i] == ' ':
                    cells[i] = 'X'
                    eval_score = self._minimax(cells, depth + 1, True, alpha, beta)
                    cells[i] = ' '
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval
