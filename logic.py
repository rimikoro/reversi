import numpy as np
# 自石が置ける場所を判断する
def judge(board, turn):
    move = [(1,0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    return_board = []
    for row_board in range(8):
        for col_board in range(8):
            if board[row_board][col_board] != 0:
                continue
            # 8方向確認
            for vec in move:
                y = row_board + vec[0]
                x = col_board + vec[1]
                # 盤面を外れたらやり直し
                if not (0 <= y <= 7 and 0 <= x <= 7):
                    continue
                # 値が0ならやり直し
                if board[y][x] == 0:
                    continue
                # 値が自分の石ならやり直し
                if board[y][x] == turn:
                    continue
                while True:
                    y += vec[0]
                    x += vec[1]
                    if not (0 <= y <= 7 and 0 <= x <= 7):
                        break
                    elif board[y][x] == 0:
                        break
                    # 値が自分の石の時
                    if board[y][x] == turn:
                        return_board.append([row_board, col_board])
                        break
                if [row_board, col_board] in return_board:
                    break
    return return_board

# ひっくり返す場所を判断
def put_logic(board, y, x, turn):
    board[y][x] = turn
    flipped = []
    
    move = [(1,0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    for vec in move:
        put_stone = []
        new_y = y + vec[0]
        new_x = x + vec[1]
        while 0 <= new_y <= 7 and 0 <= new_x <= 7:
            if board[new_y][new_x] == 0:
                break
            if board[new_y][new_x] == turn:
                for stone in put_stone:
                    board[stone[0]][stone[1]] = turn
                flipped.extend(put_stone)
                break
            put_stone.append([new_y, new_x])
            new_y += vec[0]
            new_x += vec[1]
    return board, flipped

# 盤面をコピーして返す
def board_copy(board):
    return np.array(board, copy=True)