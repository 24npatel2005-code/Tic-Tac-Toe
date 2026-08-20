import tkinter as tk
from tkinter import messagebox, font
import random

# ===================== AI LOGIC =====================
def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return (i, 0), (i, 2)
        if all(board[j][i] == player for j in range(3)):
            return (0, i), (2, i)
    if all(board[i][i] == player for i in range(3)):
        return (0, 0), (2, 2)
    if all(board[i][2 - i] == player for i in range(3)):
        return (0, 2), (2, 0)
    return None

def get_empty(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def is_full(board):
    return len(get_empty(board)) == 0

def minimax(board, depth, is_max, alpha, beta):
    w = check_winner(board, "O")
    if w:
        return 10 - depth
    w = check_winner(board, "X")
    if w:
        return depth - 10
    if is_full(board):
        return 0

    if is_max:
        best = -100
        for i, j in get_empty(board):
            board[i][j] = "O"
            s = minimax(board, depth + 1, False, alpha, beta)
            board[i][j] = " "
            best = max(best, s)
            alpha = max(alpha, s)
            if beta <= alpha:
                break
        return best
    else:
        best = 100
        for i, j in get_empty(board):
            board[i][j] = "X"
            s = minimax(board, depth + 1, True, alpha, beta)
            board[i][j] = " "
            best = min(best, s)
            beta = min(beta, s)
            if beta <= alpha:
                break
        return best

def ai_easy(board):
    empty = get_empty(board)
    if random.random() < 0.25:
        for i, j in empty:
            board[i][j] = "X"
            if check_winner(board, "X"):
                board[i][j] = "O"
                return
            board[i][j] = " "
    i, j = random.choice(empty)
    board[i][j] = "O"

def ai_medium(board):
    empty = get_empty(board)
    for i, j in empty:
        board[i][j] = "O"
        if check_winner(board, "O"):
            return
        board[i][j] = " "
    for i, j in empty:
        board[i][j] = "X"
        if check_winner(board, "X"):
            board[i][j] = "O"
            return
        board[i][j] = " "
    if board[1][1] == " ":
        board[1][1] = "O"
        return
    corners = [(0,0),(0,2),(2,0),(2,2)]
    random.shuffle(corners)
    for i, j in corners:
        if board[i][j] == " ":
            board[i][j] = "O"
            return
    i, j = random.choice(empty)
    board[i][j] = "O"

def ai_hard(board):
    empty = get_empty(board)
    if len(empty) == 9:
        board[1][1] = "O"
        return
    best_s, best_m = -100, None
    for i, j in empty:
        board[i][j] = "O"
        s = minimax(board, 0, False, -100, 100)
        board[i][j] = " "
        if s > best_s:
            best_s, best_m = s, (i, j)
    board[best_m[0]][best_m[1]] = "O"

# ===================== COLORS =====================
C_BG      = "#0f0f23"
C_BOARD   = "#1a1a3e"
C_CELL    = "#12122e"
C_HOVER   = "#222255"
C_GRID    = "#4444aa"
C_X       = "#ff4466"
C_O       = "#00ccff"
C_TXT     = "#eeeeee"
C_DIM     = "#666688"
C_WIN     = "#ffdd00"
C_BTN     = "#2a2a5e"
C_BTN_H   = "#4444aa"
C_GREEN   = "#44cc66"
C_ORANGE  = "#ff9922"
C_RED     = "#ff3355"
C_PURPLE  = "#8844cc"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg=C_BG)
        self.root.resizable(False, False)

        self.sz = 130
        self.gap = 12
        self.board_px = self.sz * 3 + self.gap * 4
        self.pad = 14

        self.F = font.Font(family="Segoe UI", size=14, weight="bold")
        self.FT = font.Font(family="Segoe UI", size=32, weight="bold")
        self.FS = font.Font(family="Segoe UI", size=11)
        self.FB = font.Font(family="Segoe UI", size=10)

        self.scores = {"x": 0, "o": 0, "d": 0}
        self.mode = None
        self.level = 1
        self.board = [[" "]*3 for _ in range(3)]
        self.drawn = [[False]*3 for _ in range(3)]
        self.over = False
        self.turn = 0
        self.p1 = True
        self.win_line = None

        self._center(460, 650)
        self.menu()

    def _center(self, w, h):
        x = self.root.winfo_screenwidth()//2 - w//2
        y = self.root.winfo_screenheight()//2 - h//2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _kill(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _btn(self, parent, text, cmd, color=C_BTN, **kw):
        b = tk.Button(parent, text=text, font=kw.get("font", self.F),
                      fg=C_TXT, bg=color, activebackground=color,
                      activeforeground=C_TXT, relief="flat", cursor="hand2",
                      command=cmd, padx=kw.get("padx", 12),
                      pady=kw.get("pady", 4))
        return b

    # ===================== MAIN MENU =====================
    def menu(self):
        self._kill()
        self._center(460, 680)
        self.mode = None

        tk.Label(self.root, text="TIC TAC TOE", font=self.FT,
                 fg=C_TXT, bg=C_BG).pack(pady=(30, 0))
        tk.Label(self.root, text="v2.0", font=self.FS,
                 fg=C_DIM, bg=C_BG).pack(pady=(0, 30))

        tk.Label(self.root, text="SELECT MODE", font=self.F,
                 fg=C_DIM, bg=C_BG).pack()

        f = tk.Frame(self.root, bg=C_BG)
        f.pack(fill="x", padx=60, pady=10)
        self._btn(f, "  SINGLE PLAYER  ", lambda: self.diff_menu("single"),
                  C_PURPLE).pack(fill="x", ipady=6, pady=4)
        self._btn(f, "  TWO PLAYERS  ", lambda: self.diff_menu("two"),
                  C_GRID).pack(fill="x", ipady=6, pady=4)

        sf = tk.Frame(self.root, bg=C_BG)
        sf.pack(pady=(25, 0))
        for k, l, c in [("x","Wins",C_GREEN),("o","Losses",C_RED),("d","Draws",C_DIM)]:
            tk.Label(sf, text=f"{l}: {self.scores[k]}", font=self.F,
                     fg=c, bg=C_BG).pack(side="left", padx=14)

        self._btn(self.root, "  RESET SCORES  ", self.reset_scores,
                  C_RED, font=self.FB, padx=8, pady=2).pack(pady=15)

    def reset_scores(self):
        self.scores = {"x": 0, "o": 0, "d": 0}
        self.menu()

    # ===================== DIFFICULTY MENU =====================
    def diff_menu(self, mode):
        self._kill()
        self.mode = mode

        tk.Label(self.root, text="SELECT DIFFICULTY", font=self.F,
                 fg=C_TXT, bg=C_BG).pack(pady=(50, 25))

        single = mode == "single"
        for text, desc, clr, lvl in [
            ("EASY", "Weak AI, you can win", C_GREEN, 1),
            ("MEDIUM", "Smart AI, blocks & attacks", C_ORANGE, 2),
            ("HARD", "UNBEATABLE AI (Minimax)", C_RED, 3),
        ]:
            f = tk.Frame(self.root, bg=C_BG)
            f.pack(fill="x", padx=50, pady=5)
            if single:
                self._btn(f, f"  {text}  ",
                          lambda l=lvl: self.play(l), clr).pack(fill="x", ipady=6)
            else:
                self._btn(f, f"  {text}  ",
                          lambda l=lvl: self.play(l), clr).pack(fill="x", ipady=6)
            tk.Label(f, text=desc, font=self.FB, fg=C_DIM, bg=C_BG).pack()

        self._btn(self.root, "  BACK  ", self.menu,
                  C_BTN, font=self.FS, padx=8, pady=2).pack(pady=20)

    # ===================== START GAME =====================
    def play(self, level):
        self._kill()
        self.level = level
        self.board = [[" "]*3 for _ in range(3)]
        self.drawn = [[False]*3 for _ in range(3)]
        self.over = False
        self.turn = 0
        self.p1 = True
        self.win_line = None
        self._center(460, 680)

        names = {1:"EASY", 2:"MEDIUM", 3:"HARD"}
        clrs  = {1:C_GREEN, 2:C_ORANGE, 3:C_RED}
        mode_txt = "SINGLE PLAYER" if self.mode == "single" else "TWO PLAYERS"

        top = tk.Frame(self.root, bg=C_BG)
        top.pack(fill="x", padx=16, pady=(10,0))
        self._btn(top, "< BACK", lambda: self.diff_menu(self.mode),
                  C_BTN, font=self.FB, padx=6, pady=1).pack(side="left")
        tk.Label(top, text=f"{mode_txt}  |  {names[self.level]}",
                 font=self.F, fg=clrs[self.level], bg=C_BG).pack(side="right")

        self.score_lbl = tk.Label(self.root,
            text=f"X: {self.scores['x']}    O: {self.scores['o']}    "
                 f"Draw: {self.scores['d']}", font=self.FS, fg=C_DIM, bg=C_BG)
        self.score_lbl.pack(pady=(6,2))

        self.turn_lbl = tk.Label(self.root, text="", font=self.FS,
                                 fg=C_TXT, bg=C_BG)
        self.turn_lbl.pack(pady=(0,4))

        self.status_lbl = tk.Label(self.root, text="", font=self.F,
                                   fg=C_TXT, bg=C_BG)
        self.status_lbl.pack(pady=(0,6))

        self.canvas = tk.Canvas(self.root, width=self.board_px,
                                height=self.board_px, bg=C_BOARD,
                                highlightthickness=0)
        self.canvas.pack()

        self.rects = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                x1 = self.gap + j*(self.sz + self.gap) + 4
                y1 = self.gap + i*(self.sz + self.gap) + 4
                x2, y2 = x1 + self.sz - 8, y1 + self.sz - 8
                self.rects[i][j] = (x1, y1, x2, y2)
                tag = f"r{i}{j}"
                rid = self.canvas.create_rectangle(x1, y1, x2, y2,
                    fill=C_CELL, outline=C_GRID, width=2, tags=tag)
                self.canvas.tag_bind(tag, "<Enter>",
                    lambda e, c=rid: self.canvas.itemconfig(c, fill=C_HOVER))
                self.canvas.tag_bind(tag, "<Leave>",
                    lambda e, c=rid: self.canvas.itemconfig(c, fill=C_CELL))
                self.canvas.tag_bind(tag, "<Button-1>",
                    lambda e, r=i, c=j: self.click(r, c))

        bf = tk.Frame(self.root, bg=C_BG)
        bf.pack(pady=8)
        self._btn(bf, "RESTART", lambda: self.play(self.level)).pack(side="left", padx=8)
        self._btn(bf, "MENU", self.menu).pack(side="left", padx=8)

        self._set_turn()
        self._set_status("")

    # ===================== UI HELPERS =====================
    def _set_status(self, t, c=None):
        self.status_lbl.config(text=t, fg=c or C_TXT)

    def _set_turn(self):
        if self.mode == "single":
            if self.p1:
                self.turn_lbl.config(text="Your turn  (X)", fg=C_X)
            else:
                self.turn_lbl.config(text="Computer's turn  (O)", fg=C_O)
        else:
            if self.turn % 2 == 0:
                self.turn_lbl.config(text="Player 1's turn  (X)", fg=C_X)
            else:
                self.turn_lbl.config(text="Player 2's turn  (O)", fg=C_O)

    def _upd_score(self):
        self.score_lbl.config(
            text=f"X: {self.scores['x']}    O: {self.scores['o']}    "
                 f"Draw: {self.scores['d']}")

    # ===================== DRAW X (CROSS) =====================
    def _draw_x(self, r, c):
        x1, y1, x2, y2 = self.rects[r][c]
        cx, cy = (x1+x2)/2, (y1+y2)/2
        s = (x2-x1)/2 - self.pad
        w = 5
        self.canvas.create_line(cx-s, cy-s, cx+s, cy+s,
            fill=C_X, width=w, capstyle="round")
        self.canvas.create_line(cx+s, cy-s, cx-s, cy+s,
            fill=C_X, width=w, capstyle="round")
        self.drawn[r][c] = True

    # ===================== DRAW O (CIRCLE) =====================
    def _draw_o(self, r, c):
        x1, y1, x2, y2 = self.rects[r][c]
        cx, cy = (x1+x2)/2, (y1+y2)/2
        rad = (x2-x1)/2 - self.pad
        self.canvas.create_oval(cx-rad, cy-rad, cx+rad, cy+rad,
            outline=C_O, width=5, fill="")
        self.drawn[r][c] = True

    def _draw_line(self, cells, color):
        (r1,c1), (r2,c2) = cells
        x1 = (self.rects[r1][c1][0]+self.rects[r1][c1][2])/2
        y1 = (self.rects[r1][c1][1]+self.rects[r1][c1][3])/2
        x2 = (self.rects[r2][c2][0]+self.rects[r2][c2][2])/2
        y2 = (self.rects[r2][c2][1]+self.rects[r2][c2][3])/2
        self.canvas.create_line(x1, y1, x2, y2,
            fill=color, width=8, capstyle="round")

    def _place(self, r, c, player):
        self.board[r][c] = player
        if player == "X":
            self._draw_x(r, c)
        else:
            self._draw_o(r, c)

    # ===================== CLICK =====================
    def click(self, r, c):
        if self.over or self.board[r][c] != " ":
            return

        if self.mode == "single":
            if not self.p1:
                return
            self._place(r, c, "X")
            w = check_winner(self.board, "X")
            if w:
                self.end("p1", w)
                return
            if is_full(self.board):
                self.end("draw")
                return
            self.p1 = False
            self._set_turn()
            self._set_status("Thinking...")
            self.root.after(300, self.ai_move)
        else:
            player = "X" if self.turn % 2 == 0 else "O"
            self._place(r, c, player)
            w = check_winner(self.board, player)
            if w:
                self.end("p1" if player == "X" else "p2", w)
                return
            if is_full(self.board):
                self.end("draw")
                return
            self.turn += 1
            self._set_turn()

    # ===================== AI =====================
    def ai_move(self):
        if self.over:
            return
        if self.level == 1:
            ai_easy(self.board)
        elif self.level == 2:
            ai_medium(self.board)
        else:
            ai_hard(self.board)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "O" and not self.drawn[i][j]:
                    self._draw_o(i, j)

        w = check_winner(self.board, "O")
        if w:
            self.end("cpu", w)
            return
        if is_full(self.board):
            self.end("draw")
            return
        self.p1 = True
        self._set_turn()
        self._set_status("")

    # ===================== END GAME =====================
    def end(self, result, wc=None):
        self.over = True
        self.win_line = wc

        if result == "p1":
            self.scores["x"] += 1
            self._set_status("X WINS!", C_WIN)
            msg = "Player X Wins!"
            lc = C_X
        elif result == "p2":
            self.scores["o"] += 1
            self._set_status("O WINS!", C_WIN)
            msg = "Player O Wins!"
            lc = C_O
        elif result == "cpu":
            self.scores["o"] += 1
            self._set_status("COMPUTER WINS!", C_RED)
            msg = "Computer Wins!"
            lc = C_O
        else:
            self.scores["d"] += 1
            self._set_status("DRAW!", C_DIM)
            msg = "It's a Draw!"
            lc = C_DIM

        self._upd_score()
        self.turn_lbl.config(text="", fg=C_TXT)

        if wc:
            self._draw_line(wc, lc)

        for i in range(3):
            for j in range(3):
                tag = f"r{i}{j}"
                self.canvas.tag_unbind(tag, "<Button-1>")
                self.canvas.tag_unbind(tag, "<Enter>")
                self.canvas.tag_unbind(tag, "<Leave>")

        self.root.after(600, lambda: self._game_over_popup(msg))

    def _game_over_popup(self, msg):
        result = messagebox.askyesno("Game Over", f"{msg}\n\nPlay Again?")
        if result:
            self.play(self.level)
        else:
            self.menu()

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
