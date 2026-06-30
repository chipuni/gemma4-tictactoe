import json
import os
from board import Board, Colors
from ai import TicTacToeAI

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class GameSession:
    def __init__(self, mode='PvP', difficulty='Hard', size=3):
        self.board = Board(size=size)
        self.current_player = 'X'
        self.mode = mode 
        self.difficulty = difficulty
        self.ai = TicTacToeAI(difficulty=difficulty) if mode == 'PvE' else None

    def play(self):
        while True:
            clear_screen()
            print(f"{Colors.BOLD}--- TIC TAC TOE {Colors.RESET} (Size: {self.board.size}x{self.board.size})")
            self.board.display()
            
            if self.current_player == 'X' or (self.mode == 'PvP' and self.current_player == 'O'):
                try:
                    prompt = f"Player {Colors.BOLD}{self.current_player}{Colors.RESET}, enter move (0-{len(self.board.cells)-1}): "
                    move = int(input(prompt))
                except ValueError:
                    print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.RESET}")
                    input("Press Enter to continue...")
                    continue
            else:
                print(f"{Colors.CYAN}CPU is thinking...{Colors.RESET}")
                move = self.ai.get_move(self.board)
                print(f"CPU chose position {Colors.BOLD}{move}{Colors.RESET}")

            if self.board.make_move(move, self.current_player):
                winner = self.board.check_winner()
                if winner:
                    clear_screen()
                    print(f"{Colors.BOLD}--- GAME OVER ---{Colors.RESET}")
                    self.board.display()
                    if winner == 'Draw':
                        print(f"{Colors.YELLOW}{Colors.BOLD}It's a draw!{Colors.RESET}")
                    else:
                        print(f"{Colors.GREEN}{Colors.BOLD}Player {winner} wins!{Colors.RESET}")
                    input("\nPress Enter to return to menu...")
                    return winner
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            else:
                print(f"{Colors.RED}Invalid move. Position occupied or out of bounds.{Colors.RESET}")
                input("Press Enter to continue...")

def load_scores():
    if os.path.exists('scores.json'):
        with open('scores.json', 'r') as f:
            return json.load(f)
    return {'X': 0, 'O': 0, 'Draw': 0}

def save_scores(scores):
    with open('scores.json', 'w') as f:
        json.dump(scores, f)

def main():
    scores = load_scores()
    
    while True:
        clear_screen()
        print("\n" + "="*30)
        print(f"{Colors.BOLD}MAIN MENU{Colors.RESET}")
        print("1. Play Human vs Human (PvP)")
        print("2. Play Human vs CPU (PvE)")
        print("3. View Scores")
        print("4. Quit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            size_input = input("Enter board size (default 3): ")
            size = int(size_input) if size_input.isdigit() else 3
            session = GameSession(mode='PvP', size=size)
            result = session.play()
            if result and result != 'Draw': scores[result] += 1
            elif result == 'Draw': scores['Draw'] += 1
            save_scores(scores)
        elif choice == '2':
            size_input = input("Enter board size (default 3): ")
            size = int(size_input) if size_input.isdigit() else 3
            
            print("\nChoose Difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            diff_choice = input("Select (1-3): ")
            difficulty = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}.get(diff_choice, 'Hard')
            
            session = GameSession(mode='PvE', difficulty=difficulty, size=size)
            result = session.play()
            if result and result != 'Draw': scores[result] += 1
            elif result == 'Draw': scores['Draw'] += 1
            save_scores(scores)
        elif choice == '3':
            clear_screen()
            print(f"{Colors.BOLD}Current Scores:{Colors.RESET}")
            print(f"Player X: {scores['X']}")
            print(f"Player O: {scores['O']}")
            print(f"Draws:    {scores['Draw']}")
            input("\nPress Enter to return to menu...")
        elif choice == '4':
            print("Thanks for playing!")
            break
        else:
            print(f"{Colors.RED}Invalid selection.{Colors.RESET}")

if __name__ == "__main__":
    main()
