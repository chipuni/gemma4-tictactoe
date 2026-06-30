import json
import os
import time
from board import Board, Colors
from ai import TicTacToeAI

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class GameSession:
    def __init__(self, mode='PvP', difficulty='Hard', size=3, markers=None):
        self.board = Board(size=size)
        self.current_player = 'X'
        self.mode = mode 
        self.difficulty = difficulty
        self.markers = markers if markers else {'X': 'X', 'O': 'O'}
        # Create separate AI instances for each player if needed (especially for CPUvsCPU)
        self.ai_x = TicTacToeAI(difficulty=difficulty) if mode in ['PvE', 'CpuCpu'] else None
        self.ai_o = TicTacToeAI(difficulty=difficulty) if mode in ['PvE', 'CpuCpu'] else None

    def play(self):
        while True:
            clear_screen()
            print(f"{Colors.BOLD}--- TIC TAC TOE {Colors.RESET} (Size: {self.board.size}x{self.board.size})")
            print(f"Player X: {Colors.BLUE}{self.markers['X']}{Colors.RESET} | Player O: {Colors.RED}{self.markers['O']}{Colors.RESET}")
            self.board.display_fixed(self.markers)
            
            if self.mode != 'CpuCpu':
                print("\nCommands: [move 0-N] or ['u' to undo]")
            else:
                print("\nSpectating CPU vs CPU...")

            # Determine who moves
            is_human_turn = False
            if self.mode == 'PvP':
                is_human_turn = True
            elif self.mode == 'PvE':
                is_human_turn = (self.current_player == 'X') # Human is X, CPU is O
            elif self.mode == 'CpuCpu':
                is_human_turn = False

            if is_human_turn:
                try:
                    prompt = f"Player {Colors.BOLD}{self.current_player}{Colors.RESET}, enter move: "
                    user_input = input(prompt).strip().lower()
                    
                    if user_input == 'u':
                        if self.board.undo_move():
                            self.current_player = 'O' if self.current_player == 'X' else 'X'
                            continue
                        else:
                            print(f"{Colors.RED}Nothing to undo!{Colors.RESET}")
                            input("Press Enter to continue...")
                            continue
                    
                    move = int(user_input)
                except ValueError:
                    print(f"{Colors.RED}Invalid input. Please enter a number or 'u'.{Colors.RESET}")
                    input("Press Enter to continue...")
                    continue
            else:
                # CPU Turn
                active_ai = self.ai_x if self.current_player == 'X' else self.ai_o
                print(f"{Colors.CYAN}CPU ({self.current_player}) is thinking...{Colors.RESET}")
                time.sleep(0.8) # Add pacing delay
                move = active_ai.get_move(self.board)
                print(f"CPU chose position {Colors.BOLD}{move}{Colors.RESET}")
                if self.mode != 'CpuCpu':
                    input("Press Enter to continue...")

            if self.board.make_move(move, self.current_player):
                winner = self.board.check_winner()
                if winner:
                    clear_screen()
                    print(f"{Colors.BOLD}--- GAME OVER ---{Colors.RESET}")
                    self.board.display_fixed(self.markers)
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
        print("3. Play CPU vs CPU (Spectator)")
        print("4. View Scores")
        print("5. Quit")
        
        choice = input("\nSelect an option: ")
        
        if choice in ['1', '2', '3']:
            size_input = input("Enter board size (default 3): ")
            size = int(size_input) if size_input.isdigit() else 3
            
            print("\nCustomize Markers:")
            mX = input("Marker for Player X [X]: ").strip() or 'X'
            mO = input("Marker for Player O [O]: ").strip() or 'O'
            markers = {'X': mX, 'O': mO}

            if choice == '1':
                session = GameSession(mode='PvP', size=size, markers=markers)
                result = session.play()
                if result and result != 'Draw': scores[result] += 1
                elif result == 'Draw': scores['Draw'] += 1
                save_scores(scores)
            elif choice == '2':
                print("\nChoose Difficulty:")
                print("1. Easy")
                print("2. Medium")
                print("3. Hard")
                diff_choice = input("Select (1-3): ")
                difficulty = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}.get(diff_choice, 'Hard')
                session = GameSession(mode='PvE', difficulty=difficulty, size=size, markers=markers)
                result = session.play()
                if result and result != 'Draw': scores[result] += 1
                elif result == 'Draw': scores['Draw'] += 1
                save_scores(scores)
            elif choice == '3':
                print("\nChoose AI Difficulty:")
                print("1. Easy")
                print("2. Medium")
                print("3. Hard")
                diff_choice = input("Select (1-3): ")
                difficulty = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}.get(diff_choice, 'Harda') # Fixed typo in thought but applying here
                difficulty = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}.get(diff_choice, 'Hard')
                session = GameSession(mode='CpuCpu', difficulty=difficulty, size=size, markers=markers)
                result = session.play()
                if result and result != 'Draw': scores[result] += 1
                elif result == 'Draw': scores['Draw'] += 1
                save_scores(scores)
        elif choice == '4':
            clear_screen()
            print(f"{Colors.BOLD}Current Scores:{Colors.RESET}")
            print(f"Player X: {scores['X']}")
            print(f"Player O: {scores['O']}")
            print(f"Draws:    {scores['Draw']}")
            input("\nPress Enter to return to menu...")
        elif choice == '5':
            print("Thanks for playing!")
            break
        else:
            print(f"{Colors.RED}Invalid selection.{Colors.RESET}")

if __name__ == "__main__":
    main()
