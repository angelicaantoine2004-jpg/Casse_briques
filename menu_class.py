import tkinter as tk
from tkinter import ttk

class Menu(tk.Toplevel):


    def __init__(self, parent, on_difficulty_selected):
        super().__init__(parent)
        self.title("Menu — Sélection de la difficulté")
        self.geometry("320x260")
        self.resizable(False, False)
        self.on_difficulty_selected = on_difficulty_selected
        self._build_widgets()

    def _build_widgets(self):
        """Construit l’interface du menu."""
        ttk.Label(
            self,
            text="Choisissez un niveau de difficulté :",
            font=("TkDefaultFont", 12, "bold")
        ).pack(pady=20)

        ttk.Button(
            self,
            text="Facile",
            command=lambda: self._select_difficulty("facile")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Moyen",
            command=lambda: self._select_difficulty("moyen")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Difficile",
            command=lambda: self._select_difficulty("difficile")
        ).pack(pady=10)

    def _select_difficulty(self, level: str):
        """Définit les paramètres du niveau choisi et notifie le parent."""
        settings = {}

        if level == "facile":
            settings = {
                "rows": 2,
                "cols": 6,
                "paddle_ratio": 1.0,
                "ball_speed": 4
            }
        elif level == "moyen":
            settings = {
                "rows": 4,
                "cols": 8,
                "paddle_ratio": 0.8,
                "ball_speed": 5
            }
        elif level == "difficile":
            settings = {
                "rows": 6,
                "cols": 10,
                "paddle_ratio": 0.6,
                "ball_speed": 6
            }

        # Appelle le callback si défini
        if callable(self.on_difficulty_selected):
            self.on_difficulty_selected(level, settings)

        self.destroy()
