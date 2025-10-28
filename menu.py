import tkinter as tk

class Menu:
    def __init__(self, master, callback):
        self.callback = callback
        self.window = tk.Toplevel(master)
        self.window.title("Select difficulty")
        self.window.geometry("400x300")
        self.window.config(bg="#222")

        title = tk.Label(self.window, text="Select difficulty", font=("Arial", 20, "bold"), fg="white", bg="#222")
        title.pack(pady=30)

        btn_easy = tk.Button(self.window, text="easy", width=15, font=("Arial", 14), bg="lightgreen",
                             command=lambda: self.select("easy"))
        btn_easy.pack(pady=10)

        btn_medium = tk.Button(self.window, text="medium", width=15, font=("Arial", 14), bg="gold",
                               command=lambda: self.select("medium"))
        btn_medium.pack(pady=10)

        btn_hard = tk.Button(self.window, text="difficult", width=15, font=("Arial", 14), bg="tomato",
                             command=lambda: self.select("difficult"))
        btn_hard.pack(pady=10)

    def select(self, level):
        if level == "easy":
            rows = 4
            paddle_width = 120
            ball_speed = 4
        elif level == "medium":
            rows = 6
            paddle_width = 100
            ball_speed = 5
        else:  
            rows = 8
            paddle_width = 80
            ball_speed = 6

        self.window.destroy()

        self.callback(rows, paddle_width, ball_speed)
