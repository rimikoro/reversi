from .base import BasePlayer

class Human(BasePlayer):
    def __init__(self, name = "human"):
        super().__init__()
        self.name = name
    
    def get_move(self, board, legal_move, turn):
        raise NotImplementedError