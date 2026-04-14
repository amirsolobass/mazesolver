from logging import root
from tkinter import BOTH, Canvas
import tkinter as tk
from tkinter import Tk


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
        #self.__canvas.pack(fill=BOTH, expand=1)
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

    def create_main_menu(self):
        menu_frame = tk.Frame(self.__root)
        menu_frame.pack(expand=True)

        title = tk.Label(
            menu_frame,
            text="Maze Solver",
            font=("Arial", 24)
            )
        title.pack(pady=20)

        play_button = tk.Button(
            menu_frame,
            text="Play",
            font=("Arial", 18),
            command=lambda: self.show_size_selection(menu_frame)
            )
        play_button.pack(pady=10)

        exit_button = tk.Button(
            menu_frame,
            text="Exit",
            font=("Arial", 18),
            command=self.close
            )
        exit_button.pack(pady=10)

    def show_main_menu(self):
        self.create_main_menu()
        
    def show_size_selection(self, current_frame):
        # Remove the old menu
        current_frame.destroy()
    
        # Create the new selection frame
        selection_frame = tk.Frame(self.__root)
        selection_frame.pack(expand=True)
    
        label = tk.Label(selection_frame, text="Choose Grid Size:")
        label.pack(pady=10)

        small_btn = tk.Button(selection_frame, text="Small (10x10)", command=lambda: self.start_game(10, 10, selection_frame))
        small_btn.pack(pady=5)
    
        large_btn = tk.Button(selection_frame, text="Large (25x25)", command=lambda: self.start_game(25, 25, selection_frame))
        large_btn.pack(pady=5)
    
    def start_game(self, rows, cols, frame):
        from maze import Maze
        # 1. Clear the menu
        frame.destroy()
    
        # 2. Show the canvas
        self.__canvas.pack(fill=BOTH, expand=1)
    
        # 3. Logic to create the maze
        # Note: You'll need to calculate cell sizes based on window width/height
        margin = 50
        cell_size_x = (800 - 2 * margin) / cols
        cell_size_y = (600 - 2 * margin) / rows
    
        new_maze = Maze(margin, margin, rows, cols, cell_size_x, cell_size_y, self)
        new_maze.solve()
        