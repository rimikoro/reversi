from logic import board_copy, put_logic, judge
from .base import BasePlayer
from random import choice
import numpy as np

# モンテカルロ法
class MonteCarloAI(BasePlayer):
    def __init__(self):
        super().__init__()
        self.name = "montecarlo AI"
        
    def get_move(self, board, legal_move, turn):
        n = 50
        return_dic = {}
        now_turn = turn
        for y, x in legal_move:
            return_dic[y ,x] = 0
            for _ in range(n):
                # 引数のboardをコピー(numpy配列)
                start_board = board_copy(board)
                # turnの初期化
                turn = now_turn
                # start_boardの更新
                start_board, _ = put_logic(start_board, y, x, turn)
                # ターンを返す
                turn *= -1
                # ランダム全探索
                while True:
                    # 合法手の2次元リストを返す
                    result = judge(start_board, turn)
                    if not result:# 空ならパス判定
                        turn *= -1
                        if not judge(start_board, turn): # 2連続パスでゲーム終了
                            mine = np.count_nonzero(start_board == now_turn)
                            yours = np.count_nonzero(start_board == -now_turn)
                            if yours < mine: # 石の数を判定
                                return_dic[y, x] += mine - yours # 勝っていたら差分を追加
                            break
                        continue
                    # start_boardの更新
                    start_board, _ = put_logic(start_board, *choice(result), turn)
                    # ターンを返す
                    turn *= -1
        # 一番評価が高い合法手を返す
        return max(return_dic, key=return_dic.get)