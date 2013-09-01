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
from .register import Register

@Register.printer(name='table')
def print_as_table(sudoku:'.sudoku.NativeSudoku'):
    """Prints the sudoku as a table"""
    previous_row = 0
    for value, row, col in sudoku.iterate_cells():
        if row != previous_row:
            print()
            previous_row = row
            if row in (3, 6):
                for i in range(2):
                    print("\u2500"*3, end="")
                    print("\u253C", end="")
                print("\u2500"*3)
        if col in (3, 6):
            print("\u2502", end="")
        if value != 0:
            print(convert_to_character(value), end="")
        else:
            print(" ", end="")
    print()

@Register.printer(name='list')
def print_as_list(sudoku:'.sudoku.NativeSudoku'):
    """Prints the sudoku as a list"""
    for value, row, col in sudoku.iterate_cells():
        if value == 0:
            value = ""
        if row == 8 and col == 8:
            print(convert_to_character(value), end="")
        else:
            print(convert_to_character(value), end=",")
    print()

@Register.printer(name='none')
def dummy_printer(*args, **kwargs):
    pass

def convert_to_character(value:int) -> str:
    """Converts native number presentation to character (string)
    
    For example:
    >>> convert_to_character(0)
    '0'
    >>> convert_to_character(1)
    '1'
    >>> convert_to_character(0b000100000)
    '6'
    """
    if value in (0, 1):
        return str(value)
    loops = 0
    while(value):
        value = value >> 1
        loops += 1
    return str(loops)
