import unittest
from maze import Maze
from cell import Cell

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_draw_cell_no_window(self):
        m1 = Maze(0, 0, 10, 10, 10, 10)
        m1._Maze__draw_cell(0, 0)
        self.assertEqual(m1._Maze__cells[0][0]._Cell__x1, -1)
        self.assertEqual(m1._Maze__cells[0][0]._Cell__y1, -1)
        self.assertEqual(m1._Maze__cells[0][0]._Cell__x2, -1)
        self.assertEqual(m1._Maze__cells[0][0]._Cell__y2, -1)

    def test_cell_draw_no_window(self):
        c1 = Cell()
        c1.draw(0, 0, 10, 10)
        self.assertEqual(c1._Cell__x1, -1)
        self.assertEqual(c1._Cell__y1, -1)
        self.assertEqual(c1._Cell__x2, -1)
        self.assertEqual(c1._Cell__y2, -1)

    def test_cell_draw_move_no_window(self):
        c1 = Cell()
        c2 = Cell()
        c1.draw_move(c2)
        self.assertEqual(c1._Cell__x1, -1)
        self.assertEqual(c1._Cell__y1, -1)
        self.assertEqual(c1._Cell__x2, -1)
        self.assertEqual(c1._Cell__y2, -1)

    def test_cell_draw_move_undo_no_window(self):
        c1 = Cell()
        c2 = Cell()
        c1.draw_move(c2, undo=True)
        self.assertEqual(c1._Cell__x1, -1)
        self.assertEqual(c1._Cell__y1, -1)
        self.assertEqual(c1._Cell__x2, -1)
        self.assertEqual(c1._Cell__y2, -1)

    def test_cell_animate_no_window(self):
        c1 = Cell()
        c1._Cell__animate()
        self.assertEqual(c1._Cell__x1, -1)
        self.assertEqual(c1._Cell__y1, -1)
        self.assertEqual(c1._Cell__x2, -1)
        self.assertEqual(c1._Cell__y2, -1)

    def test_maze_animate_no_window(self):
        m1 = Maze(0, 0, 10, 10, 10, 10)
        m1._Maze__animate()
        self.assertEqual(
            len(m1._Maze__cells),
            10,
        )

    def test_break_entrance_and_exit_no_window(self):
        m1 = Maze(0, 0, 10, 10, 10, 10)
        m1._Maze__break_entrance_and_exit()
        self.assertFalse(m1._Maze__cells[0][0].has_top_wall)
        self.assertFalse(m1._Maze__cells[9][9].has_bottom_wall)

    def test_break_entrance_and_exit(self):
        m1 = Maze(0, 0, 10, 10, 10, 10)
        m1._Maze__break_entrance_and_exit()
        self.assertFalse(m1._Maze__cells[0][0].has_top_wall)
        self.assertFalse(m1._Maze__cells[9][9].has_bottom_wall)

    def test_break_walls_r_no_window(self):
        m1 = Maze(0, 0, 10, 10, 10, 10)
        m1._Maze__break_walls_r(0, 0)
        visited_count = 0
        for i in range(10):
            for j in range(10):
                if m1._Maze__cells[i][j].visited:
                    visited_count += 1
        self.assertEqual(visited_count, 100)

    def test_break_walls_r(self):
        m1 = Maze(0, 0, 10, 10, 10, 10)
        m1._Maze__break_walls_r(0, 0)
        visited_count = 0
        for i in range(10):
            for j in range(10):
                if m1._Maze__cells[i][j].visited:
                    visited_count += 1
        self.assertEqual(visited_count, 100)

    def test_reset_cells_visited_no_window(self):
        m1 = Maze(0, 0, 10, 10, 10, 10)
        m1._Maze__break_walls_r(0, 0)
        m1._Maze__reset_cells_visited()
        visited_count = 0
        for i in range(10):
            for j in range(10):
                if m1._Maze__cells[i][j].visited:
                    visited_count += 1
        self.assertEqual(visited_count, 0)
    
    def test_reset_cells_visited(self):
        m1 = Maze(0, 0, 10, 10, 10, 10)
        m1._Maze__break_walls_r(0, 0)
        m1._Maze__reset_cells_visited()
        visited_count = 0
        for i in range(10):
            for j in range(10):
                if m1._Maze__cells[i][j].visited:
                    visited_count += 1
        self.assertEqual(visited_count, 0)

if __name__ == "__main__":
    unittest.main()