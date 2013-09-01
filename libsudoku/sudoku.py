#!/usr/bin/env python3
# 
# Part of libsudoku library
# Copyright (c) 2013, Tomi Leppänen
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from array import array
import math

class NativeSudoku:
    """Native sudoku"""
    def __init__(self, arrays:[array, ...]):
        """Constructor, accepts a list of arrays as an argument"""
        self._sudoku = arrays
    
    def __eq__(self, obj:"NativeSudoku") -> bool:
        if not isinstance(obj, NativeSudoku):
            return False
        return self._sudoku == obj._sudoku
    
    @property
    def filled(self):
        for value, *ignore in self.iterate_cells():
            if value == 0:
                return False
        return True
    
    @property
    def readyness(self):
        numbers = 0
        for value, *ignore in self.iterate_cells():
            if value != 0:
                numbers += 1
        return numbers / 81
    
    def get_box(self, y:int, x:int) -> [array, array, array]:
        """Returns values of the box"""
        box = []
        for row in range(y*3, y*3+3):
            box.append(array('I', self._sudoku[row][x*3 : x*3+3]))
        return box
    
    def get_box_y_x_for_position(self, row:int, col:int) -> (int, int):
        """Returns box row and col for given row and col
        
        For example:
        >>> sudoku.get_box_y_x_for_position(0, 5)
        (0, 1)
        >>> sudoku.get_box_y_x_for_position(3, 3)
        (1, 1)
        >>> sudoku.get_box_y_x_for_position(7, 2)
        (2, 0)
        
        That can be used with get_box and iterate_box:
        >>> position = sudoku.get_box_y_x_for_position(3, 6)
        >>> box = sudoku.get_box(*position)
        """
        return (row//3, col//3)
    
    def get_cell(self, row:int, col:int) -> int:
        """Returns cell value"""
        return self._sudoku[row][col]
    
    def get_col(self, col:int) -> array:
        """Returns values of a column"""
        column = array('I')
        for row in self._sudoku:
            column.append(row[col])
        return column
    
    def get_row(self, row:int) -> array:
        """Returns values of a row"""
        return self._sudoku[row]
    
    def is_valid(self) -> bool:
        """Tests whether the sudoku is valid"""
        col_maps = [ 0 for i in range(9) ]
        box_maps = [ [ 0 for j in range(9) ] for i in range(3) ]
        for row in range(9):
            row_map = 0
            for col in range(9):
                value = self._sudoku[row][col]
                if value & row_map:
                    return False
                row_map |= value
                if value & col_maps[col]:
                    return False
                col_maps[col] |= value
                if value & box_maps[row//3-1][col//3-1]:
                    return False
                box_maps[row//3-1][col//3-1] |= value
        return True
    
    def iterate_box(self, y:int, x:int) -> "generator: (int, int, int)":
        """Generator, iterates given box as tuples (value, row, col)"""
        for row in range(y*3, y*3+3):
            for col in range(x*3, x*3+3):
                yield (self._sudoku[row][col], row, col)
        return
    
    def iterate_cells(self) -> "generator: (int, int, int)":
        """Generator, iterates cells as tuples (value, row, col)"""
        for row in range(9):
            for col in range(9):
                yield (self._sudoku[row][col], row, col)
        return
    
    def iterate_col(self, col:int) -> "generator: (int, int)":
        """Generator, iterates given column as tuples (value, row)"""
        for row in range(9):
            yield (self._sudoku[row][col], row)
        return
    
    def iterate_row(self, row:int) -> "generator: (int, int)":
        """Generator, iterates given row as tuples (value, col)"""
        for col in range(9):
            yield (self._sudoku[row][col], col)
        return
    
    def set_cell(self, row:int, col:int, value:int):
        """Sets cell value"""
        self._sudoku[row][col] = value

NATIVE_NUMBERS = [
    0b000000000, 
    0b000000001, 
    0b000000010, 
    0b000000100, 
    0b000001000, 
    0b000010000, 
    0b000100000, 
    0b001000000, 
    0b010000000, 
    0b100000000
]
