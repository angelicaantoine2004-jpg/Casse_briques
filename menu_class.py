
class Menu(tk.Toplevel):
    """Fenêtre de sélection de la difficulté."""
    def __init__(self, parent, engine):
        super().__init__(parent)
        self.title("Menu — Difficulté")
        self.geometry("300x250")
        self.resizable(False, False)
        self.engine = engine
        self._build_widgets()

    def _build_widgets(self):
        ttk.Label(self, text="Sélectionnez la difficulté :", font=("TkDefaultFont", 12, "bold")).pack(pady=20)

        ttk.Button(self, text="Facile", command=lambda: self._set_difficulty("facile")).pack(pady=10)
        ttk.Button(self, text="Moyen", command=lambda: self._set_difficulty("moyen")).pack(pady=10)
        ttk.Button(self, text="Difficile", command=lambda: self._set_difficulty("difficile")).pack(pady=10)

    def _set_difficulty(self, level: str):
        """Applique les paramètres selon la difficulté choisie."""
        if level == "facile":
            self.engine.BRICK_ROWS = 1
            self.engine.paddle_width_ratio = 1.0
        elif level == "moyen":
            self.engine.BRICK_ROWS = 2
            self.engine.paddle_width_ratio = 0.8
        else:
            self.engine.BRICK_ROWS = 3
            self.engine.paddle_width_ratio = 0.6

        self.engine._queue_message(f"Difficulté : {level.capitalize()} sélectionnée")
        self.destroy()