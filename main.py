import json
import os
import time
import sys
from board import Board, Colors
from ai import TicTacToeAI

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def thinking_spinner(duration=1.0):
    """Displays a simple spinner animation for CPU turns."""
    chars = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Colors.CYAN}CPU is thinking... {chars[i % 4]}{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(0.2)
        i += 1
    print("\n")

def print_logo():
    logo = f"""
{Colors.CYAN}  _   _  _   _  _____  _   _  _____  _____  _   _ 
 | \ | || | | ||_   _|| | | || {Colors.RESET}Tic{Colors.CYAN} Tac Toe{Colors.RESET}
 |  \| || | | |  | |  | | | | {Colors.RESET}v2.0{Colors.CYAN} 
 | . ` || | | |  | |  | |_| | {Colors.RESET}Professional Edition{Colors.CYAN}
 | |\  || |_| |  | |  |  _  | 
 |_| \_||___|_|  |_|  |_| |_| {Colors.RESET}
    """
    print(logo)

class GameSession:
    def __init__(self, mode='PvP', difficulty='Hard', size=3, markers=None, cpu_speed=1.0):
        self.board = Board(size=size)
        self.current_player = 'X'
        self.mode = mode 
        self.difficulty = difficulty
        self.cpu_speed = cpu_speed
        self.markers = markers if markers else {'X': 'X', 'O': 'O'}
        self.ai_x = TicTacToeAI(difficulty=difficulty) if mode in ['PvE', 'CpuCpu'] else None
        self.ai_o = TicTacToeAI(difficulty=difficulty) if mode in ['PvE', 'CpuCpu'] else None
        self.hint_ai = TicTacToeAI(difficulty='Hard')

    def save_game(self, filename="savegame.json"):
        data = {
            'board': self.board.to_dict(),
            'current_player': self.current_player,
            'mode': self.mode,
            'difficulty': self.difficulty,
            'markers': self.markers,
            'cpu_speed': self.cpu_speed
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_game(self, filename="savegame.json"):
        if not os.path.exists(filename):
            return False
        with open(filename, 'r') as f:
            data = json.load(f)
        self.board = Board.from_dict(data['board'])
        self.current_player = data['current_player']
        self.mode = data['mode']
        self.difficulty = data['difficulty']
        self.markers = data['markers']
        self.cpu_speed = data.get('cpu_speed', 1.0)
        self.ai_x = TicTacToeAI(difficulty=self.difficulty) if self.mode in ['PvE', 'CpuCpu'] else None
        self.ai_o = TicTacToeAI(difficulty=self.difficulty) if self.mode in ['PvE', 'CpuCpu'] else None
        return True

    def play(self):
        while True:
            clear_screen()
            print(f"{Colors.BOLD}--- TIC TAC TOE {Colors.RESET} (Size: {self.board.size}x{self.board.size})")
            print(f"Player X: {Colors.BLUE}{self.markers['X']}{Colors.RESET} | Player O: {Colors.RED}{self.markers['O']}{Colors.RESET}")
            self.board.display_fixed(self.markers)
            
            if self.mode != 'CpuCpu':
                print("\nCommands: [move 0-N], ['u' undo], ['s' save], ['h' hint]")
            else:
                print("\nSpectating CPU vs CPU...")

            is_human_turn = False
            if self.mode == 'PvP':
                is_human_turn = True
            elif self.mode == 'PvE':
                is_human_turn = (self.current_player == 'X')
            elif self.mode == 'CpuCpu':
                is_human_turn = False

            if is_human_turn:
                try:
                    prompt = f"Player {Colors.BOLD}{self.current_player}{Colors.RESET}, enter move: "
                    user_input = input(prompt).strip().lower()
                    
                    if user_input == 'q':
                        print(f"{Colors.YELLOW}Returning to menu...{Colors.RESET}")
                        return "QUIT"
                    elif user_input == 'u':
                        if self.board.undo_move():
                            self.current_player = 'O' if self.current_player == 'X' else 'X'
                            continue
                        else:
                            print(f"{Colors.RED}Nothing to undo!{Colors.RESET}")
                            input("Press Enter to continue...")
                            continue
                    elif user_input == 's':
                        self.save_game()
                        print(f"{Colors.GREEN}Game saved successfully!{Colors.RESET}")
                        input("Press Enter to continue...")
                        continue
                    elif user_input == 'h':
                        hint = self.hint_ai.get_suggested_move(self.board)
                        if hint != -1:
                            print(f"{Colors.YELLOW}AI suggests move: {Colors.BOLD}{hint}{Colors.RESET}")
                        else:
                            print(f"{Colors.RED}No moves available!{Colors.RESET}")
                        input("Press Enter to continue...")
                        continue
                    
                    # Parse coordinate or index
                    move = -1
                    if user_input.isdigit():
                        move = int(user_input)
                    elif len(user_input) >= 2 and user_input[0].isalpha() and user_input[1:].isdigit():
                        col_char = user_input[0].upper()
                        row_val = int(user_input[1:]) - 1
                        col_val = ord(col_char) - ord('A')
                        if 0 <= row_val < self.board.size and 0 <= col_val < self.board.size:
                            move = row_val * self.board.size + col_val
                    else:
                        print(f"{Colors.RED}Invalid format. Use index (e.g. '4') or coordinate (e.g. 'A1').{Colors.RESET}")
                        input("Press Enter to continue...")
                        continue

                except ValueError:
                    print(f"{Colors.RED}Invalid input. Please enter a number, 'u', 's', or 'h'.{Colors.RESET}")
                    input("Press Enter to continue...")
                    continue
            else:
                active_ai = self.ai_x if self.current_player == 'X' else self.ai_o
                thinking_spinner(self.cpu_speed)
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
    return {'X': 0, 'O': 0, 'Draw': 0, 'Total': 0}

def save_scores(scores):
    with open('scores.json', 'w') as f:
        json.dump(scores, f)

def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            return json.load(f)
    return {'size': 3, 'marker_x': 'X', 'marker_o': 'O', 'cpu_speed': 1.0}

def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

def get_game_settings():
    """Handles the input for game startup settings."""
    settings = load_settings()
    size_input = input(f"Enter board size [default {settings['size']}]: ")
    if size_input == "":
        size = settings['size']
    elif size_input.isdigit() and int(size_input) > 0:
        size = int(size_input)
    else:
        print(f"{Colors.RED}Invalid size. Using default {settings['size']}.{Colors.RESET}")
        size = settings['size']

    print("\nCustomize Markers:")
    mX = input(f"Marker for Player X [{settings['marker_x']}]: ").strip() or settings['marker_x']
    while len(mX) > 3:
        mX = input("Too long! Marker must be < 4 chars. Enter Player X marker: ").strip()
    mO = input(f"Marker for Player O [{settings['marker_o']}]: ").strip() or settings['marker_o']
    while len(mO) > 3:
        mO = input("Too long! Marker must be < 4 chars. Enter Player O marker: ").strip()
    markers = {'X': mX, 'O': mO}

    return size, markers

def main():
    try:
        scores = load_scores()
        if 'Total' not in scores:
            scores['Total'] = scores['X'] + scores['O'] + scores['Draw']
        
        settings = load_settings()
        
        while True:
            clear_screen()
            print_logo()
            print("\n" + "="*40)
            print(f"{Colors.BOLD}MAIN MENU{Colors.RESET}")
            print("1. Play Human vs Human (PvP)")
            print("2. Play Human vs CPU (PvE)")
            print("3. Play CPU vs CPU (Spectator)")
            print("4. Load Saved Game")
            print("5. View Statistics")
            print("6. Reset All Scores")
            print("7. Help & Commands")
            print("8. Settings")
            print("9. Quit")
            
            choice = input("\nSelect an option: ")
            
            if choice in ['1', '2', '3']:
                size, markers = get_game_settings()
        
                if choice == '1':
                    session = GameSession(mode='PvP', size=size, markers=markers)
                    result = session.play()
                    if result == "QUIT":
                        continue
                    if result:
                        scores['Total'] += 1
                        if result != 'Draw': scores[result] += 1
                        else: scores['Draw'] += 1
                        save_scores(scores)
                elif choice == '2':
                    print("\nChoose Difficulty:")
                    print("1. Easy")
                    print("2. Medium")
                    print("3. Hard")
                    diff_choice = input("Select (1-3): ")
                    difficulty = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}.get(diff_choice, 'Hard')
                    speed_input = input(f"AI thinking speed [default {settings['cpu_speed']}s]: ")
                    speed = float(speed_input) if speed_input.replace('.','',1).isdigit() else settings['cpu_speed']
                    session = GameSession(mode='PvE', difficulty=difficulty, size=size, markers=markers, cpu_speed=speed)
                    result = session.play()
                    if result == "QUIT":
                        continue
                    if result:
                        scores['Total'] += 1
                        if result != 'Draw': scores[result] += 1
                        else: scores['Draw'] += 1
                        save_scores(scores)
                elif choice == '3':
                    print("\nChoose AI Difficulty:")
                    print("1. Easy")
                    print("2. Medium")
                    print("3. Hard")
                    diff_choice = input("Select (1-3): ")
                    difficulty = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}.get(diff_choice, 'Hard')
                    speed_input = input(f"AI thinking speed [default {settings['cpu_speed']}s]: ")
                    speed = float(speed_input) if speed_input.replace('.','',1).isdigit() else settings['cpu_speed']
                    session = GameSession(mode='CpuCpu', difficulty=difficulty, size=size, markers=markers, cpu_speed=speed)
                    result = session.play()
                    if result == "QUIT":
                        continue
                    if result:
                        scores['Total'] += 1
                        if result != 'Draw': scores[result] += 1
                        else: scores['Draw'] += 1
                        save_scores(scores)
            elif choice == '4':
                session = GameSession() 
                if session.load_game():
                    result = session.play()
                    if result == "QUIT":
                        continue
                    if result:
                        scores['Total'] += 1
                        if result != 'Draw': scores[result] += 1
                        else: scores['Draw'] += 1
                        save_scores(scores)
                else:
                    print(f"{Colors.RED}No saved game found!{Colors.RESET}")
                    input("Press Enter to continue...")
            elif choice == '5':
                clear_screen()
                print(f"{Colors.BOLD}Overall Statistics:{Colors.RESET}")
                total = scores['Total']
                if total > 0:
                    win_rate_x = (scores['X'] / total) * 100
                    win_rate_o = (scores['O'] / total) * 100
                    draw_rate = (scores['Draw'] / total) * 100
                    print(f"Total Games: {total}")
                    print(f"Player X Wins: {scores['X']} ({win_rate_x:.1f}%)")
                    print(f"Player O Wins: {scores['O']} ({win_rate_o:.1f}%)")
                    print(f"Draws:        {scores['Draw']} ({draw_rate:.1f}%)")
                else:
                    print("No games played yet.")
                input("\nPress Enter to return to menu...")
            elif choice == '6':
                confirm = input("Are you sure you want to reset all scores? (y/n): ")
                if confirm.lower() == 'y':
                    scores = {'X': 0, 'O': 0, 'Draw': 0, 'Total': 0}
                    save_scores(scores)
                    print(f"{Colors.GREEN}Statistics reset successfully!{Colors.RESET}")
                else:
                    print("Reset cancelled.")
                input("\nPress Enter to return to menu...")
            elif choice == '7':
                clear_screen()
                print(f"{Colors.BOLD}--- HELP & COMMANDS ---{Colors.RESET}")
                print("\nGame Rules:")
                print("- Align N markers horizontally, vertically, or diagonally to win.")
                print("- The board size (N) is selectable at the start of a match.")
                print("\nIn-Game Commands:")
                print(f"  {Colors.CYAN}'u'{Colors.RESET} : Undo the last move made.")
                print(f"  {Colors.CYAN}'s'{Colors.RESET} : Save current game state to disk.")
                print(f"  {Colors.CYAN}'h'{Colors.RESET} : Request a best-move hint from the AI.")
                print(f"  {Colors.CYAN}'0-N'{Colors.RESET}: Enter the index of the cell you wish to occupy.")
                input("\nPress Enter to return to menu...")
            elif choice == '8':
                clear_screen()
                print(f"{Colors.BOLD}--- SETTINGS ---{Colors.RESET}")
                print("1. Change Default Board Size")
                print("2. Change Default Marker X")
                print("3. Change Default Marker O")
                print("4. Change AI Speed")
                print("5. Return to Main Menu")
                
                set_choice = input("\nSelect an option: ")
                if set_choice == '1':
                    val = input(f"New board size [default {settings['size']}]: ")
                    if val == "":
                        pass
                    elif val.isdigit() and int(val) > 0:
                        settings['size'] = int(val)
                    else:
                        print(f"{Colors.RED}Invalid size.{Colors.RESET}")
                elif set_choice == '2':
                    val = input(f"New marker X [default {settings['marker_x']}]: ").strip() or settings['marker_x']
                    if len(val) <= 3: settings['marker_x'] = val
                elif set_choice == '3':
                    val = input(f"New marker O [default {settings['marker_o']}]: ").strip() or settings['marker_o']
                    if len(val) <= 3: settings['marker_o'] = val
                elif set_choice == '4':
                    val = input(f"New AI speed [default {settings['cpu_speed']}s]: ")
                    if val.replace('.','',1).isdigit(): settings['cpu_speed'] = float(val)
                save_settings(settings)
                input("\nPress Enter to return to menu...")
            elif choice == '9':
                print("Thanks for playing!")
                break
            else:
                print(f"{Colors.RED}Invalid selection.{Colors.RESET}, try again.")
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Application interrupted by user. Exiting gracefully...{Colors.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
