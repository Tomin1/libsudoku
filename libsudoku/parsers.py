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
from .register import Register
from .sudoku import NativeSudoku

class ParsingError(Exception):
    """Exception for parsing errors"""
    def __init__(self, *args, value=None):
        self.value = value
        super().__init__(*args)

@Register.parser(name='list')
def comma_separated(value:str, separator:str=",") -> "sudoku as list":
    """Parser for comma separated form"""
    numbers = value.split(separator)
    if len(numbers) != 81:
        raise ParsingError("Invalid input string", value=value)
    sudoku = []
    for i in range(0, 81, 9):
        sudoku.append(cleanup(numbers[i:i+9]))
    return sudoku

@Register.parser
def table(value:str, separator:str=",") -> "sudoku as list":
    """Parser for table form"""
    lines = value.split("\n")
    if len(lines) != 9:
        raise ParsingError("Invalid input string", value=value)
    sudoku = []
    for line in lines:
        numbers = line.split(separator)
        if len(numbers) != 9:
            raise ParsingError("Invalid input string", value=value)
        sudoku.append(cleanup(numbers))
    return sudoku

@Register.parser(name='ignore')
def ignoring_parser(value:str, *ignore) -> "sudoku as list":
    """Expects one character per cell, values other than [1-9] are empty"""
    chars = list(value)
    chars = cleanup(chars)
    sudoku = []
    try:
        for r in range(9):
            sudoku.append([])
            base = r*9
            for c in range(9):
                try:
                    sudoku[r].append(int(chars[base + c]))
                except ValueError:
                    sudoku[r].append(0)
    except IndexError:
        raise ParsingError("Not enough input")
    return sudoku

@Register.parser
def table_ignore(value:str, *ignore) -> "sudoku as list":
    """Expects one character per cell, values other than [1-9] are empty"""
    sudoku = "".join(value.split("\n"))
    return ignoring_parser(sudoku)

def cleanup(values:list) -> "cleaned list":
    """Cleans up sudokus in parsers

    Replaces empty values (0, '' and None) with 0s.
    """
    try:
        for i in range(0, len(values)):
            value = values[i]
            if value in (0, '', None):
                values[i] = 0
            else:
                values[i] = int(value)
    except ValueError:
        raise ParsingError("Invalid number while cleaning sudoku", value=value)
    return values

def convert_to_native_sudoku(sudoku:list) -> "native sudoku":
    """Converts cleaned sudokus to native ones"""
    native = []
    for line in sudoku:
        native_line = array('I')
        for number in line:
            native_line.append(convert_to_native_number(number))
        native.append(native_line)
    return NativeSudoku(native)

def convert_to_native_number(value:int) -> "native_number":
    """Converts integers to native numbers
    
    For example:
    >>> convert_to_native_number(0)
    0
    >>> convert_to_native_number(1)
    1
    >>> convert_to_native_number(4)
    8
    >>> convert_to_native_number(9)
    256
    """
    if value in (0, 1):
        return value
    return 1 << value-1
