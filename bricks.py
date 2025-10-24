
class Brick:
   def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x+width, y+height, fill=color, outline="white")
        self.alive = True
