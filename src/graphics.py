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
        self.__width = width
        self.__height = height
        # Forces the window to take focus from other applications
        self.__root.focus_force()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        #self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.redraw()

    def bind_key(self, key, callback):
        self.__root.bind(key, callback)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line: Line, color="black"):
        line.draw(self.__canvas, color=color)

    def draw_oval(self, x1, y1, x2, y2, color="red"):
        padding = 5
        return self.__canvas.create_oval(x1 + padding, y1 + padding, x2 - padding, y2 - padding, fill=color, outline="")
    
    def delete_shape(self, shape_id):
        if shape_id is not None:
             self.__canvas.delete(shape_id)

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

    def return_to_menu(self):
        # Clear the canvas and show the main menu again
        self.__canvas.pack_forget()  # Hide the canvas
        self.show_main_menu()  # Show the main menu

    def return_to_main_menu(self, current_frame):
        current_frame.destroy()
        self.show_main_menu()

    def unbind_all_keys(self):
        for key in ["<Up>", "<Down>", "<Left>", "<Right>"]:
            self.__root.unbind(key)
        
    def show_size_selection(self, current_frame):
        # Remove the old menu
        current_frame.destroy()
    
        # Create the new selection frame
        selection_frame = tk.Frame(self.__root)
        selection_frame.pack(expand=True)
    
        label = tk.Label(selection_frame, text="Choose Grid Size:")
        label.pack(pady=10)

        small_btn = tk.Button(selection_frame, text="Small (5x5)", command=lambda: self.start_game(5, 5, selection_frame))
        small_btn.pack(pady=5)
    
        large_btn = tk.Button(selection_frame, text="Medium (10x10)", command=lambda: self.start_game(10, 10, selection_frame))
        large_btn.pack(pady=5)
        
        large_btn = tk.Button(selection_frame, text="Large (25x25)", command=lambda: self.start_game(25, 25, selection_frame))
        large_btn.pack(pady=5)

        custom_btn = tk.Button(selection_frame, text="Custom", command=lambda: self.show_custom_size_input(selection_frame))
        custom_btn.pack(pady=5)

    def show_custom_size_input(self, current_frame):
        current_frame.destroy()
    
        input_frame = tk.Frame(self.__root)
        input_frame.pack(expand=True)

        tk.Label(input_frame, text="Rows:").pack()
        rows_entry = tk.Entry(input_frame)
        rows_entry.insert(0, "20") # Default value
        rows_entry.pack(pady=5)

        tk.Label(input_frame, text="Columns:").pack()
        cols_entry = tk.Entry(input_frame)
        cols_entry.insert(0, "20") # Default value
        cols_entry.pack(pady=5)

        # The button needs to get the data from the entries when clicked
        start_btn = tk.Button(
            input_frame, 
            text="Generate Maze", 
            command=lambda: self.validate_and_start(rows_entry.get(), cols_entry.get(), input_frame)
        )
        start_btn.pack(pady=20)

    def show_win_menu(self, last_rows, last_cols):
        # Clear the canvas and show the main menu again
        self.__canvas.pack_forget()  # Hide the canvas
        
        win_frame = tk.Frame(self.__root)
        win_frame.pack(expand=True)

        label = tk.Label(win_frame, text="Congratulations! You've solved the maze!", font=("Arial", 18))
        label.pack(pady=20)

        play_again_btn = tk.Button(win_frame, text="Play Again", command=lambda: self.start_game(last_rows, last_cols, win_frame))
        play_again_btn.pack(pady=10)

        change_size_btn = tk.Button(win_frame, text="Change Size", command=lambda: self.show_size_selection(win_frame))
        change_size_btn.pack(pady=10)

        exit_btn = tk.Button(win_frame, text="Exit", command=self.close)
        exit_btn.pack(pady=10)

    def delay_win_menu(self, ms, rows, cols):
        self.__root.after(ms, lambda: self.show_win_menu(rows, cols))

    def validate_and_start(self, rows_str, cols_str, frame):
        try:
            rows = int(rows_str)
            cols = int(cols_str)
        
            # Keep the maze within reasonable limits
            if rows < 2 or cols < 2:
                raise ValueError("Too small")
            if rows > 100 or cols > 100:
                raise ValueError("Too large")
            
            self.start_game(rows, cols, frame)
        
        except ValueError:
            # Show an error message if the input isn't a valid number
            from tkinter import messagebox
            messagebox.showerror("Invalid Input", "Please enter a number between 2 and 100.")
    
    def start_game(self, rows, cols, frame):
        from maze import Maze
        # 1. Clear the menu
        frame.destroy()
    
        # 2. Show the canvas
        self.__canvas.delete("all")
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__root.update()
    
        # 3. Logic to create the maze
        # Note: You'll need to calculate cell sizes based on window width/height
        margin = 50
        cell_x = (self.__width - 2 * margin) / cols
        cell_y = (self.__height - 2 * margin) / rows
    
        new_maze = Maze(margin, margin, rows, cols, cell_x, cell_y, self)
        self.bind_key("<Up>", new_maze.move_up)
        self.bind_key("<w>", new_maze.move_up)
        self.bind_key("<Down>", new_maze.move_down)
        self.bind_key("<s>", new_maze.move_down)
        self.bind_key("<Left>", new_maze.move_left)
        self.bind_key("<a>", new_maze.move_left)
        self.bind_key("<Right>", new_maze.move_right)
        self.bind_key("<d>", new_maze.move_right)