import unittest
from tictactoe import Board

class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board(self):
        self.assertEqual(self.board.cells, [' '] * 9)

    def test_make_move_valid(self):
        self.assertTrue(self.board.make_move(0, 'X'))
        self.assertEqual(self.board.cells[0], 'X')

    def test_make_move_invalid_occupied(self):
        self.board.make_move(0, 'X')
        self.assertFalse(self.board.make_move(0, 'O'))
        self.assertEqual(self.board.cells[0], 'X')

    def test_make_move_invalid_out_of_bounds(self):
        self.assertFalse(self.board.make_move(9, 'X'))
        self.assertFalse(self.board.make_move(-1, 'X'))

    def test_win_row(self):
        # X wins top row
        self.board.cells = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertEqual(self.board.check_winner(), 'X')

    def test_win_col(self):
        # O wins middle column
        self.board.cells = [' ', 'O', ' ', ' ', 'O', ' ', ' ', 'O', ' ']
        self.assertEqual(self.board.check_winner(), 'O')

    def test_win_diag(self):
        # X wins main diagonal
        self.board.cells = ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X']
        self.assertEqual(self.board.check_winner(), 'X')

    def test_draw(self):
        # Draw state
        self.board.cells = [
            'X', 'O', 'X',
            'X', 'O', 'O',
            'O', 'X', 'X'
        ]
        self.assertEqual(self.board.check_winner(), 'Draw')

    def test_no_winner_yet(self):
        # Partial game
        self.board.cells = ['X', ' ', 'O', ' ', 'X', ' ', ' ', ' ', ' ']
        self.assertIsNone(self.board.check_winner())

if __name__ == '__main__':
    unittest.main()
