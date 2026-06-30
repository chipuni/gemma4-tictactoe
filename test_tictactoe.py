import unittest
from board import Board

class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        # We will test both standard and larger boards in specific tests
        self.board3 = Board(size=3)

    def test_initial_board_default(self):
        self.assertEqual(self.board3.cells, [' '] * 9)

    def test_initial_board_custom_size(self):
        board4 = Board(size=4)
        self.assertEqual(len(board4.cells), 16)

    def test_make_move_valid(self):
        self.assertTrue(self.board3.make_move(0, 'X'))
        self.assertEqual(self.board3.cells[0], 'X')

    def test_make_move_invalid_occupied(self):
        self.board3.make_move(0, 'X')
        self.assertFalse(self.board3.make_move(0, 'O'))
        self.assertEqual(self.board3.cells[0], 'X')

    def test_make_move_invalid_out_of_bounds(self):
        self.assertFalse(self.board3.make_move(9, 'X'))
        self.assertFalse(self.board3.make_move(-1, 'X'))

    def test_win_row(self):
        # X wins top row 3x3
        self.board3.cells = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertEqual(self.board3.check_winner(), 'X')

    def test_win_col(self):
        # O wins middle column 3x3
        self.board3.cells = [' ', 'O', ' ', ' ', 'O', ' ', ' ', 'O', ' ']
        self.assertEqual(self.board3.check_winner(), 'O')

    def test_win_diag(self):
        # X wins main diagonal 3x3
        self.board3.cells = ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X']
        self.assertEqual(self.board3.check_winner(), 'X')

    def test_win_row_4x4(self):
        # X wins middle row 4x4
        board4 = Board(size=4)
        board4.cells[4] = 'X'
        board4.cells[5] = 'X'
        board4.cells[6] = 'X'
        board4.cells[7] = 'X'
        self.assertEqual(board4.check_winner(), 'X')

    def test_win_col_4x4(self):
        # O wins first column 4x4
        board4 = Board(size=4)
        board4.cells[0] = 'O'
        board4.cells[4] = 'O'
        board4.cells[8] = 'O'
        board4.cells[12] = 'O'
        self.assertEqual(board4.check_winner(), 'O')

    def test_win_diag_4x4(self):
        # X wins main diagonal 4x4
        board4 = Board(size=4)
        board4.cells[0] = 'X'
        board4.cells[5] = 'X'
        board4.cells[10] = 'X'
        board4.cells[15] = 'X'
        self.assertEqual(board4.check_winner(), 'X')

    def test_draw(self):
        # Draw state 3x3
        self.board3.cells = [
            'X', 'O', 'X',
            'X', 'O', 'O',
            'O', 'X', 'X'
        ]
        self.assertEqual(self.board3.check_winner(), 'Draw')

    def test_undo_move(self):
        # Test undoing a move
        self.assertTrue(self.board3.make_move(0, 'X'))
        self.assertEqual(self.board3.cells[0], 'X')
        self.assertTrue(self.board3.undo_move())
        self.assertEqual(self.board3.cells[0], ' ')

    def test_undo_empty(self):
        # Test undo on empty board
        self.assertFalse(self.board3.undo_move())

    def test_no_winner_yet(self):
        # Partial game
        self.board3.cells = ['X', ' ', 'O', ' ', 'X', ' ', ' ', ' ', ' ']
        self.assertIsNone(self.board3.check_winner())

if __name__ == '__main__':
    unittest.main()
