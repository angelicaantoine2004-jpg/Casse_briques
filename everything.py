import tkinter as tk
import random

class Ball:
    def __init__(self, canvas, x, y, size, dx, dy, color="purple"):
        self.canvas = canvas
        self.size = size
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.id = self.canvas.create_oval(
            self.x, self.y,
            self.x + self.size, self.y + self.size,
            fill=color
        )
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.canvas.coords(
            self.id,
            self.x, self.y,
            self.x + self.size, self.y + self.size
        )
    def bounce_horizontal(self):
        self.dx = -self.dx

    def bounce_vertical(self):
        self.dy = -self.dy

    def reset(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.canvas.coords(
            self.id,
            self.x, self.y,
            self.x + self.size, self.y + self.size
        )

class Brick:
    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x+width, y+height, fill=color, outline="white")
        self.alive = True

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

        # Paddle attributes
        self.paddle_width = 100
        self.paddle_height = 12
        self.paddle_x = (600 - self.paddle_width) // 2
        self.paddle_y = 480
        self.paddle_speed = 20
        self.paddle = self.canvas.create_rectangle(
            self.paddle_x, self.paddle_y,
            self.paddle_x + self.paddle_width, self.paddle_y + self.paddle_height,
            fill= "blue"
        )
        self.window.bind("<Left>", self.move_paddle_left)
        self.window.bind("<Right>", self.move_paddle_right)

        self.ball = Ball(self.canvas, 300, 300, 15, 5, -5)

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
        if self.paddle_x > 0:
            self.paddle_x = max(0, self.paddle_x - self.paddle_speed)
            self.canvas.coords(
                self.paddle,
                self.paddle_x, self.paddle_y,
                self.paddle_x + self.paddle_width, self.paddle_y+ self.paddle_height
            )
    def move_paddle_right(self, event=None):
        if self.paddle_x + self.paddle_width <600:
            self.paddle_x = min(600-self.paddle_width, self.paddle_x + self.paddle_speed)
            self.canvas.coords(
                self.paddle,
                self.paddle_x, self.paddle_y,
                self.paddle_x + self.paddle_width, self.paddle_y+ self.paddle_height
            )

    def move_ball(self):
        self.ball.move()
        #bounce off left/right wall
        if self.ball.x <= 0 or self.ball.x + self.ball.size >= 600:
            self.ball.bounce_horizontal()
        #bounce off top 
        if self.ball.y <= 0:
            self.ball.bounce_vertical()
        #bounce of paddle
        if self.ball.y + self.ball.size >= self.paddle_y:
            if(self.paddle_x < self.ball.x + self.ball.size and self.ball.x < self.paddle_x + self.paddle_width):
                self.ball.bounce_vertical()
                self.ball.y = self.paddle_y - self.ball.size

        #if ball falls out, you lose one life
        if self.ball.y + self.ball.size > 500:
            self.lives -= 1
            self.update_text()
            if self.lives <=0:
                self.running = False
                if self.game_over_text_id is None:
                    self.game_over_text_id = self.canvas.create_text(300,250, text= "game over", fill="white", font=("arial", 32))
                return
            self.ball.reset(300, 300, random.choice([-5, 5]), -5)

        #bounce off bricks
        hit_brick = None
        for brick in self.bricks:
            brick_coords = self.canvas.coords(brick.id)
            bx1, by1, bx2, by2 = brick_coords
            ball_center_x = self.ball.x + self.ball.size/2
            ball_center_y = self.ball.y + self.ball.size/2
            if bx1 < ball_center_x < bx2 and by1 < ball_center_y < by2:
                hit_brick = brick
                break
        if hit_brick:
            self.canvas.delete(hit_brick.id)
            self.bricks.remove(hit_brick)
            self.ball.bounce_vertical()
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
        self.ball.reset(300, 300, 5, -5)
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