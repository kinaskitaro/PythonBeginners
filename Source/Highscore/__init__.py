import json
import os
from typing import List, Dict, Optional


class HighscoreManager:
    """Centralized highscore management for all games"""
    
    def __init__(self, game_name: str, highscore_dir: str = "Highscore"):
        self.game_name = game_name
        self.highscore_dir = highscore_dir
        self.highscore_file = self._get_highscore_path()
        
    def _get_highscore_path(self) -> str:
        """Get the full path to the highscore file"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        highscore_path = os.path.join(base_dir, self.highscore_dir, f"{self.game_name}_highscore.json")
        return highscore_path
    
    def ensure_directory(self):
        """Create highscore directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.highscore_file), exist_ok=True)
    
    def load_highscore(self) -> int:
        """Load single highscore value"""
        self.ensure_directory()
        if os.path.exists(self.highscore_file):
            try:
                with open(self.highscore_file, 'r') as f:
                    data = json.load(f)
                    return data.get('highscore', 0)
            except:
                return 0
        return 0
    
    def save_highscore(self, highscore: int):
        """Save single highscore value"""
        self.ensure_directory()
        with open(self.highscore_file, 'w') as f:
            json.dump({'highscore': highscore}, f)
    
    def load_highscores(self, limit: int = 10) -> List[Dict]:
        """Load multiple highscore entries (for games that track top scores)"""
        self.ensure_directory()
        if os.path.exists(self.highscore_file):
            try:
                with open(self.highscore_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data[:limit]
            except:
                return []
        return []
    
    def save_highscores(self, highscores: List[Dict]):
        """Save multiple highscore entries"""
        self.ensure_directory()
        with open(self.highscore_file, 'w') as f:
            json.dump(highscores, f)
    
    def add_score(self, name: str, score: int, limit: int = 10) -> List[Dict]:
        """Add a new score and return updated list"""
        highscores = self.load_highscores(limit)
        highscores.append({'name': name, 'score': score})
        highscores = sorted(highscores, key=lambda x: x['score'], reverse=True)[:limit]
        self.save_highscores(highscores)
        return highscores
    
    def update_highscore(self, score: int) -> int:
        """Update highscore if new score is higher, return current highscore"""
        current_highscore = self.load_highscore()
        if score > current_highscore:
            self.save_highscore(score)
            return score
        return current_highscore
    
    def get_highscore(self) -> int:
        """Get current highscore"""
        return self.load_highscore()
