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

