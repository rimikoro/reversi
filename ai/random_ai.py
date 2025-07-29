from random import choice
from .base import BasePlayer

# ランダムに行動
class RandomAI(BasePlayer):
    def __init__(self):
        super().__init__()
        self.name = "random AI"
        
    def get_move(self, board, legal_move, turn):
        return choice(legal_move)