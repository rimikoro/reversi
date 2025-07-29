# 基底クラス
class BasePlayer:
    def __init__(self):
        self.name = "player name"
        
    def get_move(self, board, legal_move, turn):
        raise NotImplementedError