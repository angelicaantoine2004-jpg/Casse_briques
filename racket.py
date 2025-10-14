class Racket:

    def __init__(self, canvas, window):  
        # Paddle attributes
        self.canvas = canvas
        self.paddle_width = 100
        self.paddle_height = 12
        self.paddle_x = (600 - self.paddle_width) // 2
        self.paddle_y = 480
        self.paddle_speed = 20
        self.paddle = canvas.create_rectangle(
        self.paddle_x, self.paddle_y,
        self.paddle_x + self.paddle_width, self.paddle_y + self.paddle_height,
        fill= "white"
        )
        window.bind("<Left>", self.move_paddle_left)
        window.bind("<Right>", self.move_paddle_right)

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