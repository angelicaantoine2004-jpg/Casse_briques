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

