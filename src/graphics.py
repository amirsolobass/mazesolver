from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def draw(self, canvas: Canvas, color="black"):
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill=color, width=2)


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        # Forces the window to take focus from other applications
        self.__root.focus_force()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line: Line, color="black"):
        line.draw(self.__canvas, color=color)

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__root.destroy()
        self.__running = False