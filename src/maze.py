from cell import Cell
import time
import random


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

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0,0)
        self.__reset_cells_visited()

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
        self.__win.redraw()
        time.sleep(0.01)

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