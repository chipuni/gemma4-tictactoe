import json
import os

def load_stats():
    if os.path.exists('scores.json'):
        with open('scores.json', 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return {'X': 0, 'O': 0, 'Draw': 0, 'Total': 0, 'total_moves': 0, 'avg_length': 0}

def save_stats(stats):
    with open('scores.json', 'w') as f:
        json.dump(stats, f, indent=2)

def update_stats(stats, winner, move_count):
    stats['Total'] += 1
    if winner != 'Draw' and winner is not None:
        stats[winner] += 1
    elif winner == 'Draw':
        stats['Draw'] += 1
    
    stats['total_moves'] += move_count
    stats['avg_length'] = stats['total_moves'] / stats['Total'] if stats['Total'] > 0 else 0
    return stats
