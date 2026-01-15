import time

class LcdApi:
    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0
        self.impl_init()

    def clear(self):
        self.impl_clear()
        self.cursor_x = 0
        self.cursor_y = 0

    def putstr(self, string):
        for char in string:
            if char == '\n':
                self.cursor_x = 0
                self.cursor_y += 1
                if self.cursor_y >= self.num_lines:
                    self.cursor_y = 0
            else:
                self.impl_putchar(char)
                self.cursor_x += 1
                if self.cursor_x >= self.num_columns:
                    self.cursor_x = 0
                    self.cursor_y += 1
                    if self.cursor_y >= self.num_lines:
                        self.cursor_y = 0

    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        self.impl_move_to(cursor_x, cursor_y)