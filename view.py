import tkinter as tk
import random

class View:
    
    _CELL_SIZE = 60
    _CANVAS_WIDTH = 235
    _CANVAS_HEIGHT = 235
    _WINDOW_TITLE = "15 puzzle"
    _COLORS = ["black", "silver", "silver", "silver", "silver", "silver",
              "silver", "silver", "silver", "silver", "silver", "silver",
              "silver", "silver", "silver", "silver"]
   
    def __init__(self):
        self._init_root()
        self._init_canvas()
        self._init_bind()
        self._init_bind_2_()
        self._elems = ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8",
             "e9", "e10", "e11", "e12", "e13", "e14", "e15", "e0"]
        self._game_over = -1

    def _init_root(self):
        self._root = tk.Tk()
        self._root.title(self._WINDOW_TITLE)

    def _init_canvas(self):
        """The function create a canvas and text on the canvas at start of game"""
        self._canvas = tk.Canvas(self._root,
                                 width=self._CANVAS_WIDTH,
                                 height=self._CANVAS_HEIGHT)
        a = "    15 puzzle \n  press <Enter>"
        self._canvas.create_text(120, 120, text=a, font=("Arial", 20), tag="txt")
        self._canvas.pack()

    def _init_canvas_rectangle(self, elem_num):
        """The function create rectangle(cells) on canvas,
        paints them in a certain color according to the cell number without the letter 'e',
        create text on the cell, displays it`s number"""
        el = self._elems[elem_num]
        row_num = elem_num // 4
        col_num = elem_num % 4
        color_num = int(el[1:])
        elem_color = self._COLORS[color_num]
        x_left = col_num * self._CELL_SIZE
        y_top = row_num * self._CELL_SIZE
        self._canvas.create_rectangle(x_left, y_top, x_left + self._CELL_SIZE, y_top + self._CELL_SIZE,
                                  fill = elem_color, tag = el)
        self._canvas.create_text(x_left + 30, y_top + 30, text= el[1:], font=("Arial", 20), tag="t" + el)

    def _init_draw_rectangle(self, elem_num):
        """The function only draws cells after permutation"""
        el = self._elems[elem_num]
        row_num = elem_num // 4
        col_num = elem_num % 4
        color_num = int(el[1:])
        elem_color = self._COLORS[color_num]
        x_left = col_num * self._CELL_SIZE
        y_top = row_num * self._CELL_SIZE
        self._canvas.coords(el, x_left, y_top, x_left + self._CELL_SIZE, y_top + self._CELL_SIZE)
        self._canvas.coords("t" + el, x_left + 30, y_top + 30)

    def _change_elems(self, elem_num1, elem_num2):
        """The function rearranges cells and draws them"""
        self._elems[elem_num1], self._elems[elem_num2] = self._elems[elem_num2], self._elems[elem_num1]
        self._init_draw_rectangle(elem_num1)
        self._init_draw_rectangle(elem_num2)

    def _init_end_game(self):
        """The function checks the game for completion"""
        for elem_num in range(15):
            el = self._elems[elem_num]
            if elem_num + 1 != int(el[1:]):
                return 0
        return 1

    def _init_get_near(self, elem_num):
        """The function determines the list of neighbors(three cases)"""
        near_cells = []
        row_num = elem_num // 4
        col_num = elem_num % 4
        if col_num > 0:
            tmp_num = col_num + row_num * 4 - 1
            near_cells.append(tmp_num)
        if col_num < 3:
            tmp_num = col_num + row_num * 4 + 1
            near_cells.append(tmp_num)
        if row_num > 0:
            tmp_num = col_num + (row_num - 1) * 4
            near_cells.append(tmp_num)
        if row_num < 3:
            tmp_num = col_num + (row_num + 1) * 4
            near_cells.append(tmp_num)
        return near_cells

    def _init_prep_elems(self):
        """The function sets the placement of the cells(random)"""
        random.shuffle(self._elems)

    def _init_test_elems(self, event):
        """The function defines a cell,
        if the cells is empty, nothing is executed
        if it is possible, rerranges cells,
        if the game is won, displays a text about the end of game"""
        col_num = event.x // self._CELL_SIZE
        row_num = event.y // self._CELL_SIZE
        elem_num = col_num + row_num * 4
        el = self._elems[elem_num]
        if el == "e0":
            return 1
        near_cells = self._init_get_near(elem_num)
        for tmp_num in near_cells:
            if self._elems[tmp_num] == "e0":
                self._change_elems(elem_num, tmp_num)
                self._game_over = self._init_end_game()
                if self._game_over:
                    b = "GAME OVER"
                    self._canvas.create_text(120, 120, text = b, font = ("Arial", 20), tag ="txt"  )
        return

    def _on_mouse_click(self, event):
        """The function does another function when clicking on the cell with the mouse button """
        self._init_test_elems(event)

    def _init_bind(self):
        """The function handles clicking on the cell with the mouse button"""
        self._canvas.bind("<Button-1>", self._on_mouse_click)

    def _init_start_game(self, event):
        """The function arranges and creates cells at start of game"""
        self._init_prep_elems()
        for elem_num in range(len(self._elems)):
            self._init_canvas_rectangle(elem_num)

    def _init_bind_2_(self):
        """The function handles keystroke on the keyboard(at start of game)"""
        self._canvas.bind("<KeyPress>", self._init_start_game)
        self._canvas.focus_set()

    def show(self):
        self._root.mainloop()
