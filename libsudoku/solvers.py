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
from copy import deepcopy
from .register import Register
from .sudoku import NATIVE_NUMBERS

class SolvingError(Exception):
    """Exception for solving errors"""
    
    def __init__(self, *args, sudoku=None, map_=None, solver=None):
        self.sudoku = sudoku
        self.map = map_
        self.solver = solver
        super().__init__(*args)

class Map:
    def __init__(self, sudoku:'.sudoku.NativeSudoku'):
        self.sudoku = sudoku
        
        self.row_maps = array('I')
        for row in range(9):
            self.row_maps.append(0)
            for value, col in sudoku.iterate_row(row):
                self.row_maps[row] |= value
        
        self.col_maps = array('I')
        for col in range(9):
            self.col_maps.append(0)
            for value, row in sudoku.iterate_col(col):
                self.col_maps[col] |= value
        
        self.box_maps = [ [], [], [] ]
        for y in range(3):
            for x in range(3):
                self.box_maps[y].append(0)
                for value, row, col in sudoku.iterate_box(y, x):
                    self.box_maps[y][x] |= value
    
    def get_values(self, row:int, col:int) -> int:
        """Returns all possible values for a cell"""
        value = 0b1000000000
        value |= self.row_maps[row]
        value |= self.col_maps[col]
        value |= self.box_maps[row//3][col//3]
        return ~value & 0b111111111
    
    def get_value_map(self) -> [array, array, array]:
        """Returns a map of possible values"""
        map_ = [ array('I') for i in range(9) ]
        for row in range(9):
            for col in range(9):
                value = self.sudoku.get_cell(row, col)
                if value == 0:
                    map_[row].append(self.get_values(row, col))
                    continue
                map_[row].append(value)
        return map_
    
    def is_done(self) -> bool:
        """Returns whether the sudoku this map represents is done"""
        for map_ in self.row_maps:
            if not map_ == 0b111111111:
                return False
        for map_ in self.col_maps:
            if not map_ == 0b111111111:
                return False
        for maps in self.box_maps:
            for map_ in maps:
                if not map_ == 0b111111111:
                    return False
        return True
    
    def update(self, row:int, col:int, value:int):
        """Updates all maps by given values"""
        self.row_maps[row] |= value
        self.col_maps[col] |= value
        self.box_maps[row//3][col//3] |= value

@Register.solver(name='dummy')
def dummy_solver(sudoku:".sudoku.NativeSudoku") -> ".sudoku.NativeSudoku":
    """Solver that creates a map but doesn't solve anything"""
    Map(sudoku)
    return sudoku

@Register.solver(name='simple')
def simple_solver(sudoku:".sudoku.NativeSudoku") -> ".sudoku.NativeSudoku":
    """Very primitive solver"""
    if not sudoku.is_valid():
        raise SolvingError("Broken sudoku, didn't start solving", sudoku=sudoku)
    map_ = Map(sudoku)
    while True:
        if check_lines_boxes(sudoku, map_):
            continue
        elif check_all_cells(sudoku, map_):
            continue
        elif not map_.is_done():
            raise SolvingError(
                "Can't solve", sudoku=sudoku, map_=map_, solver=simple_solver
            )
        else:
            break
    if not sudoku.is_valid():
        raise SolvingError(
            "Broken sudoku, checked after solving", sudoku=sudoku, map_=map_
        )
    return sudoku

@Register.solver(name='split')
def splitting_solver(
        sudoku:".sudoku.NativeSudoku"
        ) -> "[.sudoku.NativeSudoku, ....]":
    """Solver that uses split to complete all sudokus"""
    if not sudoku.is_valid():
        raise SolvingError("Broken sudoku, didn't start solving", sudoku=sudoku)
    sudokus_and_maps = [(sudoku, Map(sudoku))]
    ready = []
    while True:
        try:
            sudoku, map_ = sudokus_and_maps.pop()
        except IndexError: # The list is empty
            break
        try:
            if check_lines_boxes(sudoku, map_):
                sudokus_and_maps.append((sudoku, map_))
                continue
            elif check_all_cells(sudoku, map_):
                sudokus_and_maps.append((sudoku, map_))
                continue
        except SolvingError:
            continue
        if map_.is_done():
            if sudoku.is_valid():
                ready.append(sudoku)
        else:
            sudokus_and_maps.extend(split(sudoku, map_))
    if not ready:
        raise SolvingError( # FIXME: exited?
            "Solver exited without solving sudoku", sudoku=sudoku, map_=map_
        )
    return ready

def split(
        sudoku:".sudoku.NativeSudoku", 
        map_:"Map"
        ) -> "[(.sudoku.NativeSudoku, Map), ...]":
    """Splits a sudoku into multiple sudokus"""
    for value, row, col in sudoku.iterate_cells():
        if value != 0:
            continue
        values = map_.get_values(row, col)
        sudokus_and_maps = []
        for number in NATIVE_NUMBERS:
            if number & values:
                new_sudoku = deepcopy(sudoku)
                new_map = deepcopy(map_)
                new_sudoku.set_cell(row, col, number)
                new_map.update(row, col, number)
                sudokus_and_maps.append((new_sudoku, new_map))
        return sudokus_and_maps
    raise SolvingError("Couldn't split", sudoku=sudoku, map_=map_)

def test_value_and_update(
        value:int, 
        row:int, 
        col:int, 
        sudoku:".sudoku.NativeSudoku", 
        map_:"Map"
        ) -> bool:
    """Tests a value and updates sudoku and map if needed"""
    if value == 0:
        return False
    if value == (value & -value):
        sudoku.set_cell(row, col, value)
        map_.update(row, col, value)
        return True
    return False

def check_all_cells(sudoku:".sudoku.NativeSudoku", map_:"Map") -> bool:
    """Checks all cells if there is only one allowed value"""
    changed = False
    for value, row, col in sudoku.iterate_cells():
        if value == 0:
            values = map_.get_values(row, col)
            if values == 0:
                raise SolvingError("Broken map", sudoku=sudoku, map_=map_)
            changed |= test_value_and_update(values, row, col, sudoku, map_)
    return changed

def check_lines_boxes(sudoku:".sudoku.NativeSudoku", map_:"Map") -> bool:
    """Checks all rows, cols and boxes if there is one place for a value"""
    changed = False
    for row in range(9):
        row_map = map_.row_maps[row]
        for value in NATIVE_NUMBERS:
            if not row_map & value:
                saved_col = None
                positions = 0
                for cell_val, col in sudoku.iterate_row(row):
                    if cell_val == 0 and value & map_.get_values(row, col):
                        positions += 1
                        saved_col = col
                if positions == 1:
                    changed |= test_value_and_update(
                        value, row, saved_col, sudoku, map_
                    )
    for col in range(9):
        col_map = map_.col_maps[col]
        for value in NATIVE_NUMBERS:
            if not col_map & value:
                saved_row = None
                positions = 0
                for cell_val, row in sudoku.iterate_col(col):
                    if cell_val == 0 and value & map_.get_values(row, col):
                        positions += 1
                        saved_row = row
                if positions == 1:
                    changed |= test_value_and_update(
                        value, saved_row, col, sudoku, map_
                    )
    for y in range(3):
        for x in range(3):
            box_map = map_.box_maps[y][x]
            for value in NATIVE_NUMBERS:
                if not box_map & value:
                    saved_col = None
                    saved_row = None
                    positions = 0
                    for cell_val, row, col in sudoku.iterate_box(y, x):
                        if cell_val == 0 and value & map_.get_values(row, col):
                            positions += 1
                            saved_col = col
                            saved_row = row
                    if positions == 1:
                        changed |= test_value_and_update(
                            value, saved_row, saved_col, sudoku, map_
                        )
    return changed
