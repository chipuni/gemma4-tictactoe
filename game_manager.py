from typing import Optional, Dict, Tuple
import json
import os
from board import Board

class GameSession:
    def __init__(self, mode='PvP', difficulty='Hard', size=3, win_condition=3, markers=None, cpu_speed=1.0, blitz_time=None):
        self.board = Board(size=size, win_condition=win_condition)
        self.current_player = 'X'
        self.mode = mode 
        self.difficulty = difficulty
        self.cpu_speed = cpu_speed
        self.blitz_time = blitz_time # Time in seconds per move
        self.markers = markers if markers else {'X': 'X', 'O': 'O'}
        from ai import TicTacToeAI
        self.ai_x = TicTacToeAI(difficulty=difficulty) if mode in ['PvE', 'CpuCpu'] else None
        self.ai_o = TicTacToeAI(difficulty=difficulty) if mode in ['PvE', 'CpuCpu'] else None
        self.hint_ai = TicTacToeAI(difficulty='Hard')
        self.move_history = [] # Track moves for replay/logging

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
        from ai import TicTacToeAI
        self.ai_x = TicTacToeAI(difficulty=self.difficulty) if self.mode in ['PvE', 'CpuCpu'] else None
        self.ai_o = TicTacToeAI(difficulty=self.difficulty) if self.mode in ['PvE', 'CpuCpu'] else None
        return True

    def make_move(self, move: int, player: str) -> bool:
        if self.board.make_move(move, player):
            self.move_history.append({'player': player, 'move': move})
            return True
        return False

    def undo_move(self) -> bool:
        if self.board.undo_move():
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        return self.board.check_winner()

    def get_winning_line(self):
        return self.board.get_winning_line()

    def get_hint(self) -> int:
        return self.hint_ai.get_suggested_move(self.board)
