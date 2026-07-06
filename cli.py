import json
import os
import time
import sys
import select
from board import Board, Colors
from game_manager import GameSession
from history_manager import save_game_to_history, load_game_history
from save_manager import save_game, load_game, list_save_slots
from puzzles import get_puzzles
from score_manager import load_stats, save_stats, update_stats

class GameCLI:
    def __init__(self):
        self.scores = self._load_scores()
        self.settings = self._load_settings()

    def _load_scores(self):
        return load_stats()

    def _save_scores(self, scores):
        save_stats(scores)

    def _load_settings(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    pass
        return {'size': 3, 'marker_x': 'X', 'marker_o': 'O', 'cpu_speed': 1.0, 'theme': 'Classic'}

    def _save_settings(self, settings):
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def thinking_spinner(self, duration=1.0):
        chars = ['|', '/', '-', '\\']
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{Colors.CYAN}CPU is thinking... {chars[i % 4]}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.2)
            i += 1
        print("\n")

    def print_logo(self):
        logo = f"""
{Colors.CYAN}  _   _  _   _  _____  _   _  _____  _____  _   _ 
 | \ | || | | ||_   _|| | | || {Colors.RESET}Tic{Colors.CYAN} Tac Toe{Colors.RESET}
 |  \| || | | |  | |  | | | {Colors.RESET}v2.3{Colors.CYAN} 
 | . ` || | | |  | |  | |_| | {Colors.RESET}Elite Edition{Colors.CYAN}
 | |\  || |_| |  | |  |  _  | 
 |_| \_||___|_|  |_|  |_| |_| {Colors.RESET}
        """
        print(logo)

    def get_input_with_timeout(self, prompt, timeout):
        sys.stdout.write(prompt)
        sys.stdout.flush()
        ready = select.select([sys.stdin], [], [], timeout)
        if ready[0]:
            return sys.stdin.readline().strip().lower()
        else:
            return None

    def play_game(self, session: GameSession):
        while True:
            self.clear_screen()
            print(f"{Colors.BOLD}--- CONNECT {session.board.win_condition} ---{Colors.RESET} (Size: {session.board.size}x{session.board.size})")
            if session.blitz_time:
                print(f"{Colors.YELLOW}{Colors.BOLD}BLITZ MODE: {session.blitz_time}s per move!{Colors.RESET}")
            print(f"{Colors.BLUE}{session.players['X']}{Colors.RESET} ({session.markers['X']}) | {Colors.RED}{session.players['O']}{Colors.RESET} ({session.markers['O']})")
            session.board.display_fixed(session.markers, theme_name=self.settings['theme'])
            
            history_str = " | ".join([f"{session.markers[p]}: {session.board.get_coord(pos)}" for pos, p in session.board.history])
            if history_str:
                print(f"\n{Colors.BOLD}Move History:{Colors.RESET} {history_str}")
            
            if session.mode != 'CpuCpu':
                print("\nCommands: [move 0-N], ['u' undo], ['s' save], ['h' hint]")
            else:
                print("\nSpectating CPU vs CPU...")

            is_human_turn = False
            if session.mode == 'PvP': is_human_turn = True
            elif session.mode == 'PvE': is_human_turn = (session.current_player == 'X')
            elif session.mode == 'CpuCpu': is_human_turn = False

            if is_human_turn:
                try:
                    prompt = f"{Colors.BOLD}{session.players[session.current_player]}{Colors.RESET}, enter move: "
                    if session.blitz_time:
                        user_input = self.get_input_with_timeout(prompt, session.blitz_time)
                        if user_input is None:
                            print(f"\n{Colors.RED}{Colors.BOLD}TIME OUT! {session.players[session.current_player]} loses turn.{Colors.RESET}")
                            input("Press Enter to continue...")
                            session.current_player = 'O' if session.current_player == 'X' else 'X'
                            continue
                    else:
                        user_input = input(prompt).strip().lower()
                    
                    if user_input == 'q': return "QUIT"
                    elif user_input == 'u':
                        if session.undo_move(): continue
                        else:
                            print(f"{Colors.RED}Nothing to undo!{Colors.RESET}")
                            input("Press Enter to continue...")
                            continue
                    elif user_input == 's':
                        session.save_game()
                        print(f"{Colors.GREEN}Game saved successfully!{Colors.RESET}")
                        input("Press Enter to continue...")
                        continue
                    elif user_input == 'h':
                        hint = session.get_hint()
                        if hint != -1: print(f"{Colors.YELLOW}AI suggests move: {Colors.BOLD}{hint}{Colors.RESET}")
                        else: print(f"{Colors.RED}No moves available!{Colors.RESET}")
                        input("Press Enter to continue...")
                        continue
                    
                    move = -1
                    if user_input and user_input.isdigit(): move = int(user_input)
                    elif user_input and len(user_input) >= 2 and user_input[0].isalpha() and user_input[1:].isdigit():
                        col_char = user_input[0].upper()
                        row_val = int(user_input[1:]) - 1
                        col_char_val = ord(col_char) - ord('A')
                        if 0 <= row_val < session.board.size and 0 <= col_char_val < session.board.size:
                            move = row_val * session.board.size + col_char_val
                    else:
                        if user_input is not None:
                            print(f"{Colors.RED}Invalid format. Use index (e.g. '4') or coordinate (e.g. 'A1').{Colors.RESET}")
                            input("Press Enter to continue...")
                            continue
                        else: continue
                except ValueError:
                    print(f"{Colors.RED}Invalid input. Please enter a number, 'u', 's', or 'h'.{Colors.RESET}")
                    input("Press Enter to continue...")
                    continue
            else:
                active_ai = session.ai_x if session.current_player == 'X' else session.ai_o
                self.thinking_spinner(session.cpu_speed)
                move = active_ai.get_move(session.board, session.current_player)
                print(f"CPU chose position {Colors.BOLD}{move}{Colors.RESET}")
                if session.mode != 'CpuCpu': input("Press Enter to continue...")

            if session.board.make_move(move, session.current_player):
                winner = session.check_winner()
                if winner:
                    save_game_to_history(session)
                    self.clear_screen()
                    print(f"{Colors.BOLD}--- GAME OVER ---{Colors.RESET}")
                    winning_line = session.get_winning_line()
                    session.board.display_fixed(session.markers, highlight_line=winning_line)
                    total_moves = len(session.board.history)
                    print(f"\n{Colors.BOLD}Match Summary:{Colors.RESET}")
                    print(f"Total Moves: {total_moves}")
                    if winner == 'Draw': print(f"{Colors.YELLOW}{Colors.BOLD}Result: It's a draw!{Colors.RESET}")
                    else: print(f"{Colors.GREEN}{Colors.BOLD}Result: {session.players[winner]} wins!{Colors.RESET}")
                    input("\nPress Enter to return to menu...")
                    return winner
                session.current_player = 'O' if session.current_player == 'X' else 'X'
            else:
                if move < 0 or move >= len(session.board.cells): print(f"{Colors.RED}Move {move} is out of bounds!{Colors.RESET}")
                elif session.board.cells[move] != ' ': print(f"{Colors.RED}Position {move} is already occupied by {session.board.cells[move]}!{Colors.RESET}")
                else: print(f"{Colors.RED}Invalid move.{Colors.RESET}")
                input("Press Enter to continue...")

    def handle_puzzles(self):
        self.clear_screen()
        print(f"{Colors.BOLD}--- PUZZLE MODE ---{Colors.RESET}")
        puzzles = get_puzzles()
        if not puzzles:
            print("No puzzles available.")
            input("\nPress Enter to return to menu...")
            return

        for i, puzzle in enumerate(puzzles):
            print(f"{i+1}. {puzzle['name']} (Size: {puzzle['size']}x{puzzle['size']})")
        
        choice = input("\nSelect a puzzle to solve (or 'c' to cancel): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(puzzles):
                puzzle = puzzles[idx]
                board = Board(size=puzzle['size'], win_condition=puzzle['win_condition'])
                board.cells = list(puzzle['cells'])
                player = puzzle.get('player', 'X')
                while True:
                    self.clear_screen()
                    print(f"{Colors.BOLD}Puzzle: {puzzle['name']}{Colors.RESET}")
                    print(f"You are playing as: {Colors.BOLD}{player}{Colors.RESET}")
                        board.display_fixed({'X': 'X', 'O': 'O'}, theme_name=self.settings['theme'])
                    move = input(f"Enter move for {player} (or 'h' for hint, 'c' to cancel): ").strip().lower()
                    if move == 'c': break
                    elif move == 'h':
                        print(f"{Colors.YELLOW}HINT: {puzzle['hint']}{Colors.RESET}")
                        input("Press Enter to continue...")
                        continue
                    elif move.isdigit():
                        move_idx = int(move)
                        if move_idx == puzzle['solution']:
                            print(f"\n{Colors.GREEN}{Colors.BOLD}CORRECT! You solved the puzzle!{Colors.RESET}")
                            board.cells[move_idx] = player
                            board.display_fixed({'X': 'X', 'O': 'O'}, theme_name=self.settings['theme'])
                        else: print(f"\n{Colors.RED}{Colors.BOLD}INCORRECT! Try again.{Colors.RESET}")
                        input("\nPress Enter to continue...")
                    else: print("Invalid input.")
            else: print("Invalid selection.")
        else: print("Cancelled.")
        input("\nPress Enter to return to menu...")

    def handle_view_stats(self):
        self.clear_screen()
        print(f"{Colors.BOLD}Overall Statistics:{Colors.RESET}")
        total = self.scores.get('Total', 0)
        if total > 0:
            win_rate_x = (self.scores.get('X', 0) / total) * 100
            win_rate_o = (self.scores.get('O', 0) / total) * 100
            draw_rate = (self.scores.get('Draw', 0) / total) * 100
            print(f"Total Games: {total}")
            print(f"Player X Wins: {self.scores.get('X', 0)} ({win_rate_x:.1f}%)")
            print(f"Player O Wins: {self.scores.get('O', 0)} ({win_rate_o:.1f}%)")
            print(f"Draws:        {self.scores.get('Draw', 0)} ({draw_rate:.1f}%)")
            if 'avg_length' in self.scores: print(f"Average Game Length: {self.scores['avg_length']:.2f} moves")
        else: print("No games played yet.")
        input("\nPress Enter to return to menu...")

    def handle_replay_games(self):
        history = load_game_history()
        if not history:
            print(f"{Colors.RED}No game history found!{Colors.RESET}")
        else:
            print(f"\n{Colors.BOLD}--- GAME HISTORY ---{Colors.RESET}")
            for i, game in enumerate(history):
                print(f"{i+1}. {game['mode']} - Winner: {game['winner']} (Size: {game['size']}x{game['size']})")
            replay_choice = input("\nSelect a game to replay (or 'c' to cancel): ")
            if replay_choice.isdigit():
                idx = int(replay_choice) - 1
                if 0 <= idx < len(history):
                    game = history[idx]
                    temp_board = Board(size=game['size'], win_condition=game['win_condition'])
                    for move_data in game['moves']:
                        temp_board.make_move(move_data['move'], move_data['player'])
                        self.clear_screen()
                        print(f"{Colors.BOLD}--- REPLAYING GAME ---{Colors.RESET}")
                        session.board.display_fixed(game['markers'], theme_name=self.settings['theme'])
                        time.sleep(0.5)
                    winner = game['winner']
                    winning_line = temp_board.get_winning_line()
                        temp_board.display_fixed(game['markers'], highlight_line=winning_line, theme_name=self.settings['theme'])
                    print(f"Final Result: {winner}")
                    input("\nPress Enter to return to menu...")
                else: print(f"{Colors.RED}Invalid selection!{Colors.RESET}")
        input("\nPress Enter to continue...")

    def handle_settings(self):
        self.clear_screen()
        print(f"{Colors.BOLD}--- SETTINGS ---{Colors.RESET}")
        print("1. Change Default Board Size")
        print("2. Change Default Marker X")
        print("3. Change Default Marker O")
        print("4. Change AI Speed")
        print("5. Change Theme")
        print("6. Return to Main Menu")
        set_choice = input("\nSelect an option: ")
        if set_choice == '1':
            val = input(f"New board size [default {self.settings['size']}]: ")
            if val != "" and val.isdigit() and int(val) > 0: self.settings['size'] = int(val)
        elif set_choice == '2':
            val = input(f"New marker X [default {self.settings['marker_x']}]: ").strip() or self.settings['marker_x']
            if len(val) <= 3: self.settings['marker_x'] = val
        elif set_choice == '3':
            val = input(f"New marker O [default {self.settings['marker_o']}]: ").strip() or self.settings['marker_o']
            if len(val) <= 3: self.settings['marker_o'] = val
        elif set_choice == '4':
            val = input(f"New AI speed [default {self.settings['cpu_speed']}s]: ")
            if val.replace('.','',1).isdigit(): self.settings['cpu_speed'] = float(val)
        elif set_choice == '5':
            print("\nAvailable Themes:\n- Classic\n- Neon\n- Pastel")
            val = input(f"New theme [default {self.settings['theme']}]: ").strip() or self.settings['theme']
            if val in ['Classic', 'Neon', 'Pastel']: self.settings['theme'] = val
        self._save_settings(self.settings)
        input("\nPress Enter to return to menu...")

    def get_game_settings(self):
        settings = self.settings
        size_input = input(f"Enter board size [default {settings['size']}]: ")
        if size_input == "": size = settings['size']
        elif size_input.isdigit() and int(size_input) > 0: size = int(size_input)
        else:
            print(f"{Colors.RED}Invalid size. Using default {settings['size']}.{Colors.RESET}")
            size = settings['size']
        win_input = input(f"Enter win condition (Connect K) [default 3]: ")
        if win_input == "": win_condition = 3
        elif win_input.isdigit() and 2 <= int(win_input) <= size: win_condition = int(win_input)
        else:
            print(f"{Colors.RED}Invalid size. Using default 3.{Colors.RESET}")
            win_condition = 3
        print("\nCustomize Markers:")
        mX = input(f"Marker for Player X [{settings['marker_x']}]: ").strip() or settings['marker_x']
        while len(mX) > 3: mX = input("Too long! Marker must be < 4 chars. Enter Player X marker: ").strip()
        mO = input(f"Marker for Player O [{settings['marker_o']}]: ").strip() or settings['marker_o']
        while len(mO) > 3: mO = input("Too long! Marker must be < 4 chars. Enter Player O marker: ").strip()
        markers = {'X': mX, 'O': mO}
        
        print("\nCustomize Player Names:")
        pX = input(f"Name for Player X [Player X]: ").strip() or "Player X"
        pO = input(f"Name for Player O [Player O]: ").strip() or "Player O"
        players = {'X': pX, 'O': pO}

        return size, win_condition, markers, players

    def handle_play_game(self):
        choice = input("\nSelect Game Mode:\n1. Human vs Human (PvP)\n2. Human vs CPU (PvE)\n3. CPU vs CPU (Spectator)\nChoice: ")
        if choice not in ['1', '2', '3']: return self.scores
        size, win_condition, markers, players = self.get_game_settings()
        blitz_choice = input("Enable Blitz Mode (turn timers)? (y/n): ").lower()
        blitz_time = None
        if blitz_choice == 'y':
            b_val = input("Enter time per move in seconds [default]: ")
            blitz_time = float(b_val) if b_val.replace('.','',1).isdigit() else 10.0
        if choice == '1': session = GameSession(mode='PvP', size=size, win_condition=win_condition, markers=markers, blitz_time=blitz_time, players=players)
        elif choice == '2':
            print("\nChoose Difficulty:\n1. Easy\n2. Medium\n3. Hard")
            diff_choice = input("Select (1-3): ")
            difficulty = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}.get(diff_choice, 'Hard')
            speed_input = input(f"AI thinking speed [default {self.settings['cpu_speed']}s]: ")
            speed = float(speed_input) if speed_input.replace('.','',1).isdigit() else self.settings['cpu_speed']
            session = GameSession(mode='PvE', difficulty=difficulty, size=size, win_condition=win_condition, markers=markers, cpu_speed=speed, blitz_time=blitz_time, players=players)
        else:
            print("\nChoose AI Difficulty:\n1. Easy\n2. Medium\n3. Hard")
            diff_choice = input("Select (1-3): ")
            difficulty = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}.get(diff_choice, 'Hard')
            speed_input = input(f"AI thinking speed [default {self.settings['cpu_speed']}s]: ")
            speed = float(speed_input) if speed_input.replace('.','',1).isdigit() else self.settings['cpu_speed']
            session = GameSession(mode='CpuCpu', difficulty=difficulty, size=size, win_condition=win_condition, markers=markers, cpu_speed=speed, blitz_time=blitz_time, players=players)
        result = self.play_game(session)
        if result and result != "QUIT":
            self.scores['Total'] += 1
            if result != 'Draw': self.scores[result] += 1
            else: self.scores['Draw'] += 1
            self._save_scores(self.scores)
        return self.scores

    def run(self):
        try:
            while True:
                self.clear_screen()
                self.print_logo()
                print("\n" + "="*40)
                print(f"{Colors.BOLD}MAIN MENU{Colors.RESET}")
                print("0. Quick Play (3x3 PvP)")
                print("1. Play Single Game")
                print("2. Tournament Mode (Best of N)")
                print("3. Load Saved Game")
                print("4. Puzzle Mode")
                print("5. View Statistics")
                print("6. Replay Past Games")
                print("7. Reset All Scores")
                print("8. Help & Commands")
                print("9. Settings")
                print("10. Quit")
                choice = input("\nSelect an option: ")
                if choice == '0':
                    session = GameSession(mode='PvP', size=3, win_condition=3)
                    result = self.play_game(session)
                    if result and result != "QUIT":
                        self.scores['Total'] += 1
                        if result != 'Draw': self.scores[result] += 1
                        else: self.scores['Draw'] += 1
                        self._save_scores(self.scores)
                elif choice == '1': self.handle_play_game()
                elif choice == '2':
                    self.clear_screen()
                    print(f"{Colors.BOLD}--- TOURNAMENT MODE ---{Colors.RESET}")
                    try:
                        n_games = int(input("Enter number of games for the tournament (e.g., 3 or 5): "))
                        if n_games < 1: raise ValueError
                    except ValueError:
                        print(f"{Colors.RED}Invalid number of games!{Colors.RESET}")
                        input("\nPress Enter to return to menu...")
                        continue
                    size, win_condition, markers = self.get_game_settings()
                    blitz_choice = input("Enable Blitz Mode (turn timers)? (y/n): ").lower()
                    blitz_time = None
                    if blitz_choice == 'y':
                        b_val = input("Enter time per move in seconds [default 10]: ")
                        blitz_time = float(b_val) if b_val.replace('.','',1).isdigit() else 10.0
                    tournament_scores = {'X': 0, 'O': 0, 'Draw': 0}
                    for g in range(n_games):
                        self.clear_screen()
                        print(f"{Colors.BOLD}--- GAME {g+1}/{n_games} ---{Colors.RESET}")
                        mode = 'PvP' if 'X' in markers and 'O' in markers else 'PvE' # simplified
                        session = GameSession(mode=mode, size=size, win_condition=win_condition, markers=markers, blitz_time=blitz_time)
                        result = self.play_game(session)
                        if result:
                            tournament_scores[result] += 1
                            self.scores['Total'] += 1
                            if result != 'Draw': self.scores[result] += 1
                            else: self.scores['Draw'] += 1
                            self._save_scores(self.scores)
                        if (tournament_scores['X'] > n_games // 2) or (tournament_scores['O'] > n_games // 2): break
                    self.clear_screen()
                    print(f"{Colors.BOLD}--- TOURNAMENT RESULTS ---{Colors.RESET}")
                    print(f"X: {tournament_scores['X']} | O: {tournament_scores['O']} | Draw: {tournament_scores['Draw']}")
                    if tournament_scores['X'] > tournament_scores['O']: print(f"{Colors.GREEN}{Colors.BOLD}OVERALL WINNER: PLAYER X!{Colors.RESET}")
                    elif tournament_scores['O'] and tournament_scores['O'] > tournament_scores['X']: print(f"{Colors.GREEN}{Colors.BOLD}OVERALL WINNER: PLAYER O!{Colors.RESET}")
                    else: print(f"{Colors.YELLOW}TOURNAMENT ENDED IN A DRAW!{Colors.RESET}")
                    input("\nPress Enter to return to menu...")
                elif choice == '3':
                    slots = list_save_slots()
                    if not slots:
                        print(f"{Colors.RED}No saved games found!{Colors.RESET}")
                        input("\nPress Enter to continue...")
                        continue
                    print(f"\n{Colors.BOLD}Available Save Slots:{Colors.RESET}")
                    for s in slots: print(f"Slot {s}")
                    slot_choice = input("Select a slot to load (or 'c' to cancel): ")
                    if slot_choice.isdigit():
                        slot = int(slot_choice)
                        filename = f"savegame_{slot}.json" 
                        session = GameSession()
                        if session.load_game(filename):
                            result = self.play_game(session)
                            if result and result != "QUIT":
                                self.scores['Total'] += 1
                                if result != 'Draw': self.scores[result] += 1
                                else: self.scores['Draw'] += 1
                                self._save_scores(self.scores)
                        else: print(f"{Colors.RED}Failed to load slot {slot}!{Colors.RESET}")
                    elif slot_choice == 'c': continue
                    else: print(f"{Colors.RED}Invalid slot choice!{Colors.RESET}")
                    input("\nPress Enter to continue...")
                elif choice == '4': self.handle_puzzles()
                elif choice == '5': self.handle_view_stats()
                elif choice == '6': self.handle_replay_games()
                elif choice == '7':
                    confirm = input("Are you sure you want to reset all scores? (y/n): ")
                    if confirm.lower() == 'y':
                        self.scores = {'X': 0, 'O': 0, 'Draw': 0, 'Total': 0}
                        self._save_scores(self.scores)
                        print(f"{Colors.GREEN}Statistics reset successfully!{Colors.RESET}")
                    else: print("Reset cancelled.")
                    input("\nPress Enter to return to menu...")
                elif choice == '8':
                    self.clear_screen()
                    print(f"{Colors.BOLD}--- HELP & COMMANDS ---{Colors.RESET}")
                    print("\nGame Rules:")
                    print("- Align N markers horizontally, vertically, or diagonally to win.")
                    print("- The board size (N) is selectable at the start of a match.")
                    print("\nIn-Game Commands:")
                    print(f"  {Colors.CYAN}'u'{Colors.RESET} : Undo the last move made.")
                    print(f"  {Colors.CYAN}'s'{Colors.RESET} {Colors.RESET} : Save current game state to disk.")
                    print(f"  {Colors.CYAN}'h'{Colors.RESET} : Request a best-move hint from the AI.")
                    print(f"  {Colors.CYAN}'0-N'{Colors.RESET}: Enter the index of the cell you wish to occupy.")
                    input("\nPress Enter to return to menu...")
                elif choice == '9': self.handle_settings()
                elif choice == '10':
                    print("Thanks for playing!")
                    break
                else: print(f"{Colors.RED}Invalid selection.{Colors.RESET}, try again.")
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Application interrupted by user. Exiting gracefully...{Colors.RESET}")
                sys.exit(0)

if __name__ == "__main__":
    cli = GameCLI()
    cli.run()
