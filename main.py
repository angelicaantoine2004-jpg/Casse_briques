#qui : Angelica/ Radu/ Sebastian 
#quand : 07/10/2025
#quoi : Fichier principal du jeu, contenant les bouttons, et appelant les différents objets

''''Importation des bibliothèques'''

import tkinter as tk
import random
from bricks import Brick #les briques à casser
from racket import Racket #la raquette pour casser les briques 
#from menu import Menu # le menu qui permet de choisir sa difficulté. 
from ball import Ball # la balle


class Game:
    def __init__(self):  
        self.window = tk.Tk()
        self.window.title("Casse-brique")
        self.canvas = tk.Canvas(self.window, width=600, height=500, bg="black")
        self.canvas.pack()

        self.score = 0
        self.lives = 3 
        self.game_over_text_id = None
        self.win_text_id = None
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 16), text=f"Score:{self.score}")
        self.lives_text = self.canvas.create_text(590, 10, anchor="ne", fill="white", font=("Arial", 16), text=f"Lives:{self.lives}")

        # Add start button 
        self.start_button = tk.Button(self.window, text="Start", font=("Arial", 14), command=self.start_game)
        self.start_button.pack(pady=20)
        # Add stop button
        self.stop_button = tk.Button(self.window, text="Stop", font=("Arial",14), command=self.stop_game, state=tk.DISABLED)
        self.stop_button.pack(pady=20)
        self.running = False

        # Bricks
        self.bricks = []
        self.create_bricks()

        self.racket = Racket(self.canvas, self.window)
        self.Ball = Ball(self.canvas, 300, 300, 15, 4, -4)


    def create_bricks(self):
        # Example: 5 rows, 10 columns
        rows = 5
        cols = 10
        brick_width = 55
        brick_height = 20
        padding = 5
        offset_x = 10
        offset_y = 40
        colors = ["red", "orange", "yellow", "green", "blue"]

        for row in range(rows):
            for col in range(cols):
                x = offset_x + col * (brick_width + padding)
                y = offset_y + row * (brick_height + padding)
                color = colors[row % len(colors)]
                brick = Brick(self.canvas, x, y, brick_width, brick_height, color)
                self.bricks.append(brick)

    def move_paddle_left(self, event=None):
        if self.racket.paddle_x > 0:
            self.racket.paddle_x = max(0, self.racket.paddle_x - self.racket.paddle_speed)
            self.canvas.coords(
                self.racket.paddle,
                self.racket.paddle_x, self.racket.paddle_y,
                self.racket.paddle_x + self.racket.paddle_width, self.racket.paddle_y+ self.racket.paddle_height
            )
    def move_paddle_right(self, event=None):
        if self.racket.paddle_x + self.racket.paddle_width <600:
            self.racket.paddle_x = min(600-self.racket.paddle_width, self.racket.paddle_x + self.racket.paddle_speed)
            self.canvas.coords(
                self.racket.paddle,
                self.racket.paddle_x, self.racket.paddle_y,
                self.racket.paddle_x + self.racket.paddle_width, self.racket.paddle_y+ self.racket.paddle_height
            )

    def move_ball(self):
        self.Ball.move()
        #bounce off left/right wall
        if self.Ball.x <= 0 or self.Ball.x + self.Ball.size >= 600:
            self.Ball.bounce_horizontal()
        #bounce off top 
        if self.Ball.y <= 0:
            self.Ball.bounce_vertical()
        #bounce of paddle
        if self.Ball.y + self.Ball.size >= self.racket.paddle_y:
            if(self.racket.paddle_x < self.Ball.x + self.Ball.size and self.Ball.x < self.racket.paddle_x + self.racket.paddle_width):
                self.Ball.bounce_vertical()
                self.Ball.y = self.racket.paddle_y - self.Ball.size

        #if Ball falls out, you lose one life
        if self.Ball.y + self.Ball.size > 500:
            self.lives -= 1
            self.update_text()
            if self.lives <=0:
                self.running = False
                if self.game_over_text_id is None:
                    self.game_over_text_id = self.canvas.create_text(300,250, text= "game over", fill="white", font=("arial", 32))
                return
            self.Ball.reset(300, 300, random.choice([-5, 5]), -5)

        #bounce off bricks
        hit_brick = None
        for brick in self.bricks:
            brick_coords = self.canvas.coords(brick.id)
            bx1, by1, bx2, by2 = brick_coords
            Ball_center_x = self.Ball.x + self.Ball.size/2
            Ball_center_y = self.Ball.y + self.Ball.size/2
            if bx1 < Ball_center_x < bx2 and by1 < Ball_center_y < by2:
                hit_brick = brick
                break
        if hit_brick:
            self.canvas.delete(hit_brick.id)
            self.bricks.remove(hit_brick)
            self.Ball.bounce_vertical()
            self.score += 10
            self.update_text()
            if not self.bricks:
                self.running = False
                if self.win_text_id is None:
                    self.win_text_id = self.canvas.create_text(300, 250, text="congratulations! you beat the game :D", fill="yellow", font=("Arial", 28), justify="center")

    def update_text(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")

    def run_game(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.game_loop()

    def game_loop(self):
        if self.running:
            self.move_ball()
            self.update_text()
            self.window.after(15, self.game_loop)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def start_game(self):
        if self.game_over_text_id is not None:
            self.canvas.delete(self.game_over_text_id)
            self.game_over_text_id = None
        if self.win_text_id is not None:
            self.canvas.delete(self.win_text_id)
            self.win_text_id = None
        self.score = 0
        self.lives = 3
        self.update_text()
        self.Ball.reset(300, 300, 4, -4)
        for brick in self.bricks:
            self.canvas.delete(brick.id)
        self.bricks = []
        self.create_bricks()
        if not self.running:
            self.run_game()
    
    def stop_game(self):
        self.running = False
        self.window.destroy()

if __name__ == "__main__":
    game = Game()
    game.window.mainloop()