class Button:

    def __init__(self, x, y, width, height, name, text):
        self.name = name
        self.width = width
        self.height = height
        self.pos_x = x
        self.pos_y = y
        self.text = text

    def check_pressed(self, pos):
        x, y = pos
        if self.pos_x <= x <= self.pos_x + self.width and self.pos_y <= y <= self.pos_y + self.height:
            return True
        return False
