from graphics import Line, Point
from cell import Cell
import time
import random
from tkinter import messagebox


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self.__cells = []
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        if seed:
            random.seed(seed)
        self.__draw_count = 0
        self.player_row = 0
        self.player_col = 0
        self.player_id = None
        self.draw_player()
        self.path_history = [(0, 0)]

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_iterative(0,0)
        self.__reset_cells_visited()
        if self.__win is not None:
            self.__win.redraw()

    def __create_cells(self):
        for i in range(self.__num_cols):
            cols = []
            for j in range(self.__num_rows):
                cols.append(Cell(self.__win))
            self.__cells.append(cols)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        if self.__win is None:
            return
        self.__cells[i][j].draw(
            self.__x1 + i * self.__cell_size_x,
            self.__y1 + j * self.__cell_size_y,
            self.__x1 + (i + 1) * self.__cell_size_x,
            self.__y1 + (j + 1) * self.__cell_size_y,
        )
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__draw_count += 1
        if self.__draw_count % 100 == 0:
            self.__win.redraw()
            time.sleep(0.000001)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            next_index_list = []
            if i > 0 and not self.__cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            if j > 0 and not self.__cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
            if len(next_index_list) == 0:
                self.__draw_cell(i, j)
                return
            # randomly select a neighbor to break the wall with
            next_index = random.choice(next_index_list)
            if next_index[0] == i + 1:  # next cell is to the right
                self.__cells[i][j].has_right_wall = False
                self.__cells[i + 1][j].has_left_wall = False
            elif next_index[0] == i - 1:  # next cell is to the left
                self.__cells[i][j].has_left_wall = False
                self.__cells[i - 1][j].has_right_wall = False
            elif next_index[1] == j + 1:  # next cell is below
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j + 1].has_top_wall = False
            elif next_index[1] == j - 1:  # next cell is above
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j - 1].has_bottom_wall = False
            self.__break_walls_r(next_index[0], next_index[1])

    def __break_walls_iterative(self, i, j):
        stack = [(i, j)]
        self.__cells[i][j].visited = True

        while len(stack) > 0:
            curr_i, curr_j = stack[-1]

            next_index_list = []

            # Use self.__cells and self.__num_cols/rows (Double Underscores!)
            if curr_i > 0 and not self.__cells[curr_i - 1][curr_j].visited:
                next_index_list.append((curr_i - 1, curr_j, "left"))
            if curr_i < self.__num_cols - 1 and not self.__cells[curr_i + 1][curr_j].visited:
                next_index_list.append((curr_i + 1, curr_j, "right"))
            if curr_j > 0 and not self.__cells[curr_i][curr_j - 1].visited:
                next_index_list.append((curr_i, curr_j - 1, "up"))
            if curr_j < self.__num_rows - 1 and not self.__cells[curr_i][curr_j + 1].visited:
                next_index_list.append((curr_i, curr_j + 1, "down"))

            if len(next_index_list) == 0:
                stack.pop()
                continue

            next_i, next_j, direction = random.choice(next_index_list)
            
            if direction == "left":
                self.__cells[curr_i][curr_j].has_left_wall = False
                self.__cells[next_i][next_j].has_right_wall = False
            elif direction == "right":
                self.__cells[curr_i][curr_j].has_right_wall = False
                self.__cells[next_i][next_j].has_left_wall = False
            elif direction == "up":
                self.__cells[curr_i][curr_j].has_top_wall = False
                self.__cells[next_i][next_j].has_bottom_wall = False
            elif direction == "down":
                self.__cells[curr_i][curr_j].has_bottom_wall = False
                self.__cells[next_i][next_j].has_top_wall = False

            self.__cells[next_i][next_j].visited = True
            stack.append((next_i, next_j))

            self.__draw_cell(curr_i, curr_j)
            self.__draw_cell(next_i, next_j)
            self.__animate()

    def __reset_cells_visited(self):
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__cells[i][j].visited = False

    def solve(self):
        if self._solve_r(0,0):
            return True
        return False
    
    def _solve_r(self, i, j):
        self.__animate()
        self.__cells[i][j].visited = True
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True
        # try to move right
        if not self.__cells[i][j].has_right_wall and not self.__cells[i + 1][j].visited:
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            self.__cells[i][j].draw_move(self.__cells[i + 1][j], undo=True)
        # try to move down
        if not self.__cells[i][j].has_bottom_wall and not self.__cells[i][j + 1].visited:
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            self.__cells[i][j].draw_move(self.__cells[i][j + 1], undo=True)
        # try to move left
        if not self.__cells[i][j].has_left_wall and not self.__cells[i - 1][j].visited:
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            self.__cells[i][j].draw_move(self.__cells[i - 1][j], undo=True)
        # try to move up
        if not self.__cells[i][j].has_top_wall and not self.__cells[i][j - 1].visited:
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            self.__cells[i][j].draw_move(self.__cells[i][j - 1], undo=True)
        return False
    
    def draw_player(self, color="red"):
        # Calculate the top-left and bottom-right pixels of the player's cell
        x1 = self.__x1 + (self.player_col * self.__cell_size_x)
        y1 = self.__y1 + (self.player_row * self.__cell_size_y)
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
    
        # Use the window's new method to draw the player
        self.player_id = self.__win.draw_oval(x1, y1, x2, y2, color)

    def move_up(self, event):
        # Check if we're at the top boundary or if there's a top wall
        if self.player_row > 0 and not self.__cells[self.player_col][self.player_row].has_top_wall:
            self.player_row -= 1
            self.path_history.append((self.player_row, self.player_col))
            self.update_player_position()

    def move_down(self, event):
        if self.player_row < self.__num_rows - 1 and not self.__cells[self.player_col][self.player_row].has_bottom_wall:
            self.player_row += 1
            self.path_history.append((self.player_row, self.player_col))
            self.update_player_position()

    def move_left(self, event):
        if self.player_col > 0 and not self.__cells[self.player_col][self.player_row].has_left_wall:
            self.player_col -= 1
            self.path_history.append((self.player_row, self.player_col))
            self.update_player_position()
    
    def move_right(self, event):
        if self.player_col < self.__num_cols - 1 and not self.__cells[self.player_col][self.player_row].has_right_wall:
            self.player_col += 1
            self.path_history.append((self.player_row, self.player_col))
            self.update_player_position()

    def update_player_position(self):
    # 1. Delete the old player shape from the canvas
        self.__win.delete_shape(self.player_id)
    # 2. Draw the player at the new coordinates
        self.draw_player()
    # 3. Check if the player has reached the exit
        if self.player_row == self.__num_rows - 1 and self.player_col == self.__num_cols - 1:
            self.handle_win()

    def handle_win(self):
        # Unbind movement keys to prevent further movement after winning
        self.__win.unbind_all_keys()
        self.__win.delete_shape(self.player_id)
        self.draw_player("gold") 
        self.animate_path()
        self.__win.delay_win_menu(1500, self.__num_rows, self.__num_cols)

# In maze.py, inside class Maze:
    def animate_path(self):
    # Iterate through the history and draw lines between the points
        for i in range(len(self.path_history) - 1):
            pos1 = self.path_history[i]
            pos2 = self.path_history[i + 1]
        
        # Calculate centers of the two cells
            c1_x = self.__x1 + (pos1[1] * self.__cell_size_x) + (self.__cell_size_x / 2)
            c1_y = self.__y1 + (pos1[0] * self.__cell_size_y) + (self.__cell_size_y / 2)
            c2_x = self.__x1 + (pos2[1] * self.__cell_size_x) + (self.__cell_size_x / 2)
            c2_y = self.__y1 + (pos2[0] * self.__cell_size_y) + (self.__cell_size_y / 2)
        
        # Draw a line between the two centers
            line = Line(Point(c1_x, c1_y), Point(c2_x, c2_y))
            self.__win.draw_line(line, "gold")
        
        # Pause slightly between steps to create the animation effect
            self.__win.redraw()
            time.sleep(0.005)

        