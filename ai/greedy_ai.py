from logic import board_copy, put_logic
from .base import BasePlayer

# 一番多くひっくり返せる所に置く
class GreedyAI(BasePlayer):
    def __init__(self):
        super().__init__()
        self.name = "greedy AI"
        
    def get_move(self, board, legal_move, turn):
        flip = {}
        board = board_copy(board)
        for y, x in legal_move:
            flip[y, x] = len(put_logic(board, y, x, turn)[1])
        return max(flip, key=flip.get)