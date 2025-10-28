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
from menu import Menu



class Game:
    def __init__(self, rows=None, paddle_width=None, ball_speed=None):
        self.window = tk.Tk()
        self.window.title("Casse-brique")
        self.canvas = tk.Canvas(self.window, width=600, height=500, bg="black")
        self.canvas.pack()

        self.rows = rows if rows is not None else 5
        self.paddle_width = paddle_width if paddle_width is not None else 100
        self.ball_speed = ball_speed if ball_speed is not None else 4
        self.difficulty_selected = False 

        self.score = 0
        self.lives = 3 
        self.game_over_text_id = None
        self.win_text_id = None
        self.score_text = self.canvas.create_text(
            10, 10, anchor="nw", fill="white", font=("Arial", 16),
            text=f"Score:{self.score}"
        )
        self.lives_text = self.canvas.create_text(
            590, 10, anchor="ne", fill="white", font=("Arial", 16),
            text=f"Lives:{self.lives}"
        )

        self.button_frame = tk.Frame(self.window, bg="black")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(
            self.button_frame, text="Start", font=("Arial", 14),
            command=self.start_game, state=tk.DISABLED
        )
        self.start_button.grid(row=0, column=0, padx=10)

        self.menu_button = tk.Button(
            self.button_frame, text="Menu", font=("Arial", 14),
            command=self.open_menu
        )
        self.menu_button.grid(row=0, column=1, padx=10)


        self.stop_button = tk.Button(
            self.button_frame, text="Quit", font=("Arial", 14),
            command=self.stop_game
        )
        self.stop_button.grid(row=0, column=2, padx=10)

        self.running = False

        self.bricks = []


        self.racket = Racket(self.canvas, self.window)
        self.racket.paddle_width = self.paddle_width
        self.canvas.coords(
            self.racket.paddle,
            self.racket.paddle_x, self.racket.paddle_y,
            self.racket.paddle_x + self.racket.paddle_width,
            self.racket.paddle_y + self.racket.paddle_height
        )

        self.Ball = Ball(self.canvas, 300, 300, 15, self.ball_speed, -self.ball_speed)



    def open_menu(self):
        Menu(self.window, self.set_difficulty)

    def set_difficulty(self, rows, paddle_width, ball_speed):
        self.rows = rows
        self.paddle_width = paddle_width
        self.ball_speed = ball_speed
        self.difficulty_selected = True

        self.start_button.config(state=tk.NORMAL)  

        for brick in self.bricks:
            self.canvas.delete(brick.id)
        self.bricks = []
        self.create_bricks()

        self.racket.paddle_width = self.paddle_width
        self.canvas.coords(
            self.racket.paddle,
            self.racket.paddle_x, self.racket.paddle_y,
            self.racket.paddle_x + self.racket.paddle_width, self.racket.paddle_y + self.racket.paddle_height
        )


    def create_bricks(self):
        rows = self.rows
        cols = 10
        brick_width = 55
        brick_height = 20
        padding = 5
        offset_x = 10
        offset_y = 40
        colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "cyan"]

        for row in range(rows):
            for col in range(cols):
                x = offset_x + col * (brick_width + padding)
                y = offset_y + row * (brick_height + padding)
                color = colors[row % len(colors)]
                brick = Brick(self.canvas, x, y, brick_width, brick_height, color)
                self.bricks.append(brick)

            #definition of the movement of the racket
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
            if self.lives <=0: # if amount of lives <= 0 you lost the game
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
            self.bricks.remove(hit_brick) #delete the brick that was hit
            self.Ball.bounce_vertical()
            self.score += 10
            self.update_text()
            if not self.bricks: #if there are no more bricks left, then you won
                self.running = False
                if self.win_text_id is None:
                    self.win_text_id = self.canvas.create_text(300, 250, text="congratulations you beat the game :D", fill="yellow", font=("Arial", 28), justify="center")

    def update_text(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")

    def run_game(self):
        self.running = True # the game is set to run on it s own after start
        self.start_button.config(state=tk.DISABLED) #the start button is disabled until the stop button is pressed
        self.stop_button.config(state=tk.NORMAL)
        self.game_loop()

    def game_loop(self):
        if self.running:
            self.move_ball()
            self.update_text()
            self.window.after(15, self.game_loop) # we want the ball to move automatically, and the score to be updated every 15 ms
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def start_game(self):
        if not self.difficulty_selected:
            self.canvas.create_text(
                300, 250,
                text="Choose a difficulty from the Menu !",
                fill="yellow", font=("Arial", 16)
            )
            return

        if self.ball_speed is None:
            self.ball_speed = 4
        if self.rows is None:
            self.rows = 5
        if self.paddle_width is None:
            self.paddle_width = 100

        if self.game_over_text_id is not None:
            self.canvas.delete(self.game_over_text_id)
            self.game_over_text_id = None
        if self.win_text_id is not None:
            self.canvas.delete(self.win_text_id)
            self.win_text_id = None

        self.score = 0
        self.lives = 3
        self.update_text()

        self.Ball.reset(300, 300, self.ball_speed, -abs(self.ball_speed))

        self.run_game()



    
    def stop_game(self):
        self.running = False
        self.window.destroy()


if __name__ == "__main__":
    def start_game(rows, paddle_width, ball_speed):
        game = Game(rows, paddle_width, ball_speed)
        game.window.mainloop()

    app = Game()
    app.window.mainloop()
