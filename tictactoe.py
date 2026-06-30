import random
from typing import List, Optional

class Board:
    def __init__(self):
        self.cells = [' ' for _ in range(9)]

    def display(self):
        print("\n")
        for i in range(0, 9, 3):
            print(f" {self.cells[i]} | {self.cells[i+1]} | {self.cells[i+2]} ")
            if i < 6:
                print("-----------")
        print("\n")

    def make_move(self, position: int, player: str) -> bool:
        if 0 <= position < 9 and self.cells[position] == ' ':
            self.cells[position] = player
            return True
        return False

    def check_winner(self) -> Optional[str]:
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Cols
            [0, 4, 8], [2, 4, 6]             # Diags
        ]
        for condition in win_conditions:
            if self.cells[condition[0]] == self.cells[condition[1]] == self.cells[condition[2]] != ' ':
                return self.cells[condition[0]]
        
        if ' ' not in self.cells:
            return 'Draw'
        
        return None

class TicTacToe:
    def __init__(self, mode='PvP'):
        self.board = Board()
        self.current_player = 'X'
        self.mode = mode # 'PvP' or 'PvE'

    def get_cpu_move(self) -> int:
        # Basic AI: 1. Try to win, 2. Block opponent, 3. Center, 4. Random
        cells = self.board.cells
        available_moves = [i for i, x in enumerate(cells) if x == ' ']
        
        for player in ['O', 'X']:
            if player == 'O': # Try to win (CPU is O)
                continue 
            # This logic is simplified. Let's just do a basic implementation:
            pass

        # Improved CPU Logic
        def check_move_wins(player):
            for move in available_moves:
                self.board.cells[move] = player
                winner = self.board.check_winner()
                self.board.cells[move] = ' '
                if winner == player: return move
            return None

        # Try to win
        move = check_move_wins('O')
        if move is not None: return move
        
        # Block opponent
        move = check_move_wins('X')
        if move is not None: return move
        
        # Center
        if 4 in available_moves: return 4
        
        return random.choice(available_moves)

    def play(self):
        print("Welcome to Tic Tac Toe!")
        print("Positions are 0-8, starting from top-left.")
        
        while True:
            self.board.display()
            
            if self.current_player == 'X' or (self.mode == 'PvP' and self.current_player == 'O'):
                try:
                    move = int(input(f"Player {self.current_player}, enter move (0-8): "))
                except ValueError:
                    print("Invalid input. Please enter a number between 0-8.")
                    continue
            else:
                print("CPU is thinking...")
                move = self.get_cpu_move()
                print(f"CPU chose position {move}")

            if self.board.make_move(move, self.current_player):
                winner = self.board.check_winner()
                if winner:
                    self.board.display()
                    if winner == 'Draw':
                        print("It's a draw!")
                    else:
                        print(f"Player {winner} wins!")
                    break
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            else:
                print("Invalid move. Try again.")

if __name__ == "__main__":
    mode_choice = input("Choose mode: (1) PvP or (2) PvE: ")
    game_mode = 'PvP' if mode_choice == '1' else 'PvE'
    game = TicTacToe(mode=game_mode)
    game.play()
