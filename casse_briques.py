import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional


class GameEngine:
    TICK_MS = 16
    PADDLE_SPEED = 8
    BALL_SPEED = 5

    def __init__(self, canvas: tk.Canvas, score_var: tk.StringVar) -> None:
        self.canvas = canvas
        self.score_var = score_var
        self._after_id: Optional[str] = None
        self.running = False
        self.score = 0

        self.paddle = None
        self.ball = None
        self.ball_dx = self.BALL_SPEED
        self.ball_dy = -self.BALL_SPEED

    def start(self) -> None:
        self.reset()
        self.running = True
        self.bind_keys()
        self._loop()

    def pause(self) -> None:
        self.running = False
        if self._after_id:
            self.canvas.after_cancel(self._after_id)
            self._after_id = None

    def resume(self) -> None:
        if not self.running:
            self.running = True
            self._loop()

    def stop(self) -> None:
        self.pause()

    def reset(self) -> None:
        self.canvas.delete("all")
        self.score = 0
        self.score_var.set(f"Score : {self.score}")
        self._create_paddle()
        self._create_ball()

    def _create_paddle(self) -> None:
        """Crée la raquette du joueur."""
        w = int(self.canvas["width"])
        h = int(self.canvas["height"])
        paddle_width = 100
        paddle_height = 15
        x1 = (w - paddle_width) // 2
        y1 = h - 40
        x2 = x1 + paddle_width
        y2 = y1 + paddle_height
        self.paddle = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

    def _create_ball(self) -> None:
        w = int(self.canvas["width"])
        h = int(self.canvas["height"])
        r = 10
        x = w // 2
        y = h // 2
        self.ball = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red")

    def bind_keys(self) -> None:
        """Lie les touches de déplacement de la raquette."""
        self.canvas.bind_all("<Left>", lambda e: self._move_paddle(-self.PADDLE_SPEED))
        self.canvas.bind_all("<Right>", lambda e: self._move_paddle(self.PADDLE_SPEED))

    def _move_paddle(self, dx: int) -> None:
        if not self.paddle:
            return
        w = int(self.canvas["width"])
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        if x1 + dx < 0:
            dx = -x1
        elif x2 + dx > w:
            dx = w - x2
        self.canvas.move(self.paddle, dx, 0)

    def _loop(self) -> None:
        if not self.running:
            return
        self._move_ball()
        self._after_id = self.canvas.after(self.TICK_MS, self._loop)

    def _move_ball(self) -> None:
        if not self.ball:
            return

        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)
        w = int(self.canvas["width"])
        h = int(self.canvas["height"])

        if x1 <= 0 or x2 >= w:
            self.ball_dx *= -1
        if y1 <= 0:
            self.ball_dy *= -1
        if y2 >= h:
            self.pause()
            self.canvas.create_text(
                w // 2, h // 2,
                text="Perdu !",
                fill="red",
                font=("TkDefaultFont", 18, "bold")
            )
            return

        if self.paddle:
            px1, py1, px2, py2 = self.canvas.coords(self.paddle)
            if (y2 >= py1 and x2 >= px1 and x1 <= px2 and y2 <= py2 + 10):
                self.ball_dy *= -1
                self.score += 1
                self.score_var.set(f"Score : {self.score}")


class BreakoutApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Casse-brique — TP Tkinter")
        self.geometry("900x650")
        self.minsize(720, 520)

        self.score_var = tk.StringVar(value="Score : 0")

        self._build_menu()
        self._build_widgets()
        self._bind_shortcuts()

        self.engine = GameEngine(self.canvas, self.score_var)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_menu(self) -> None:
        menubar = tk.Menu(self)

        menu_file = tk.Menu(menubar, tearoff=False)
        menu_file.add_command(label="Nouvelle partie", command=self.on_start, accelerator="Ctrl+N")
        menu_file.add_separator()
        menu_file.add_command(label="Pause", command=self.on_pause, accelerator="P")
        menu_file.add_command(label="Reprendre", command=self.on_resume, accelerator="R")
        menu_file.add_separator()
        menu_file.add_command(label="Quitter", command=self.on_close, accelerator="Esc")
        menubar.add_cascade(label="Fichier", menu=menu_file)

        menu_help = tk.Menu(menubar, tearoff=False)
        menu_help.add_command(label="À propos", command=self.on_about)
        menubar.add_cascade(label="Aide", menu=menu_help)

        self.config(menu=menubar)

    def _build_widgets(self) -> None:
        topbar = ttk.Frame(self, padding=(10, 8))
        topbar.pack(side=tk.TOP, fill=tk.X)

        score_label = ttk.Label(topbar, textvariable=self.score_var, font=("TkDefaultFont", 12, "bold"))
        score_label.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self, width=800, height=480, bg="#111")
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=6)

        bottombar = ttk.Frame(self, padding=(10, 8))
        bottombar.pack(side=tk.BOTTOM, fill=tk.X)

        self.start_btn = ttk.Button(bottombar, text="Démarrer", command=self.on_start)
        self.start_btn.pack(side=tk.LEFT)

        quit_btn = ttk.Button(bottombar, text="Quitter", command=self.on_close)
        quit_btn.pack(side=tk.RIGHT)

        try:
            self.call("tk", "scaling", 1.2)
        except Exception:
            pass

    def _bind_shortcuts(self) -> None:
        self.bind_all("<Control-n>", lambda e: self.on_start())
        self.bind_all("<Escape>", lambda e: self.on_close())
        self.bind_all("<Key-p>", lambda e: self.on_pause())
        self.bind_all("<Key-r>", lambda e: self.on_resume())

    def on_start(self) -> None:
        self.start_btn.state(["disabled"])
        self.engine.start()

    def on_pause(self) -> None:
        self.engine.pause()
        self.start_btn.state(["!disabled"])

    def on_resume(self) -> None:
        self.engine.resume()
        self.start_btn.state(["disabled"])

    def on_about(self) -> None:
        messagebox.showinfo(
            "À propos",
            "Casse-brique (Breakout, 1976)\nTP Python + Tkinter\n\n"
            "Étape 2.2 : raquette et balle prêtes."
        )

    def on_close(self) -> None:
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
            self.engine.stop()
            self.destroy()


def main() -> None:
    app = BreakoutApp()
    app.mainloop()


if __name__ == "__main__":
    main()
