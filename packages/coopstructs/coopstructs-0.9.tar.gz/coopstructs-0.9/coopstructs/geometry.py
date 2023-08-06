class Rectangle:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width


    def __str__(self):
        return f"TopLeft: <{self.x}, {self.y}>, Size: H{self.height} x W{self.width}"
