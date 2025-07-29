from ai import *
from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import numpy as np
from logic import judge, put_logic


class App(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        
        self.master.geometry("400x400")
        self.master.title("reversi")
        self.master.resizable(False, False)
        self.master.withdraw()
        
        # 盤面
        self.board = [[0]*8 for _ in range(8)]
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[3][3] = -1
        self.board[4][4] = -1
        
        self.turn = 1 # 現在の手番
        # 実装済みの手法
        self.value = {"human": Human(), 
                      "random": RandomAI(), 
                      "greedy": GreedyAI(), 
                      "montecarlo": MonteCarloAI(), 
                      }
        self.player = {1 : None, -1 : None}
        
        self.create_widget()
        self.setting()
    
    # ウィジェットの配置
    def create_widget(self):
        # キャンバス作成
        self.canvas = Canvas(self.master, height=400, width=400, bg="green")
        self.canvas.pack()
        
        # 線引き
        for line in range(1,8,1):
            self.canvas.create_line(50*line, 0, 50*line, 400)
            self.canvas.create_line(0, 50*line, 400, 50*line)
            
        # 初期石配置
        self.canvas.create_oval(150+3,150+3,200-3,200-3, fill="white", outline="white", tag="stone_3_3")
        self.canvas.create_oval(200+3,200+3,250-3,250-3, fill="white", outline="white", tag="stone_4_4")
        self.canvas.create_oval(200+3,150+3,250-3,200-3, fill="black", tag="stone_3_4")
        self.canvas.create_oval(150+3,200+3,200-3,250-3, fill="black", tag="stone_4_3")
        self.canvas.update()
    
    # ターン制御
    def execute_turn(self):
        self.result = judge(self.board, self.turn)
        if not self.result: # パス
            self.turn *= -1
            self.result = judge(self.board, self.turn)
            if not self.result: # お互いにパス(ゲーム終了)
                self.board = np.array(self.board)
                white = np.count_nonzero(self.board == -1)
                black = np.count_nonzero(self.board == 1)
                if white < black:
                    text = "先手の勝利"
                elif black < white:
                    text = "後手の勝利"
                else:
                    text = "引き分け"
                messagebox.showinfo(title="ゲーム結果", message=f"{text}\n黒石({self.player[1].name}) : {black}個\n白石({self.player[-1].name}) : {white}個")
                self.master.destroy()
                return
        self.show_move()
        if isinstance(self.player[self.turn], Human):
            self.canvas.bind("<Button>", self.click)
        else:
            self.after(500)
            y, x = self.player[self.turn].get_move(self.board, self.result, self.turn)
            self.canvas.delete("legal_move")
            self.put(y, x)
            self.turn *= -1
            self.execute_turn()
    
    # 設定画面を閉じる
    def setting_destroy(self, combo, func):
        # 黒石
        self.player[1] = self.value[combo[0]]
        if combo[0] == "human":
            self.player[1].name = simpledialog.askstring(" ", "あなたは黒石です\nニックネームを決めてください")
        # 白石
        self.player[-1] = self.value[combo[1]]
        if combo[1] == "human":
            self.player[-1].name = simpledialog.askstring(" ", "あなたは白石です\nニックネームを決めてください")
        
        func()
        self.master.deiconify()
        self.execute_turn()
    
    # 設定
    def setting(self):
        setting_frame = Toplevel(self.master)
        setting_frame.geometry("175x100")
        setting_frame.title("設定")
        setting_frame.resizable(False, False)
        setting_frame.attributes("-toolwindow", 1)
        setting_frame.grab_set()
        setting_frame.focus_set()
        setting_frame.protocol("WM_DELETE_WINDOW", lambda: self.setting_destroy([combo1.get(), combo2.get()],setting_frame.destroy))
        
        label1 = Label(setting_frame, text="先手(黒石)")
        label1.place(x=10, y=10)
        
        label2 = Label(setting_frame, text="後手(白石)")
        label2.place(x=10, y=40)
        
        combo1 = ttk.Combobox(setting_frame, values=list(self.value.keys()), width=10, state="readonly")
        combo1.set(list(self.value.keys())[0])
        combo1.place(x=80, y=10)
        
        combo2 = ttk.Combobox(setting_frame, values=list(self.value.keys()), width=10, state="readonly")
        combo2.set(list(self.value.keys())[0])
        combo2.place(x=80, y=40)
        
        button = Button(setting_frame, text="ゲームを始める", command=lambda: self.setting_destroy([combo1.get(), combo2.get()],setting_frame.destroy))
        button.place(x=90, y=70)
    
    # クリック
    def click(self, event):
        x = event.x//50
        y = event.y//50
        if [y, x] not in self.result:
            return
        self.canvas.unbind("<Button>")
        self.canvas.delete("legal_move")
        self.put(y, x)
        self.turn *= -1
        self.execute_turn()
    
    # 石を描画
    def draw_stone(self, y, x, turn):
        tag = f"stone_{y}_{x}"
        color = "black" if turn == 1 else "white"
        
        self.canvas.create_oval(x*50+3,y*50+3,(x+1)*50-3,(y+1)*50-3, fill=color, outline=color, tag=tag)
    
    # 石を置く
    def put(self, y, x):
        self.board, flipped = put_logic(self.board, y, x, self.turn)
        self.draw_stone(y, x, self.turn)
        
        for fy, fx in flipped:
            self.canvas.delete(f"stone_{fy}_{fx}")
            self.draw_stone(fy, fx, self.turn)
    
    # 置ける手を表示
    def show_move(self):
        for b in self.result:
            color = "black" if self.turn == 1 else "white"
            
            self.canvas.create_oval(b[1]*50+20,b[0]*50+20,(b[1]+1)*50-20,(b[0]+1)*50-20, fill=color, outline=color, tag="legal_move")
        self.canvas.update()
        
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    app.mainloop()