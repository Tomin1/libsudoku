#!/usr/bin/env python3
# 
# Copyright (c) 2013, Tomi Leppänen
from libsudoku import *
from libsudoku.sudoku import NATIVE_NUMBERS
from array import array
import doctest, unittest

CORRECT_INCOMPLETE = [
    [5,3,0, 0,7,0, 0,0,0], 
    [6,0,0, 1,9,5, 0,0,0], 
    [0,9,8, 0,0,0, 0,6,0], 
    
    [8,0,0, 0,6,0, 0,0,3], 
    [4,0,0, 8,0,3, 0,0,1], 
    [7,0,0, 0,2,0, 0,0,6], 
    
    [0,6,0, 0,0,0, 2,8,0], 
    [0,0,0, 4,1,9, 0,0,5], 
    [0,0,0, 0,8,0, 0,7,9]
]

CORRECT_INCOMPLETE_NATIVE = sudoku.NativeSudoku([
    array('I', ( 16,  4,  0,   0, 64,  0,   0,  0,  0)),  
    array('I', ( 32,  0,  0,   1,256, 16,   0,  0,  0)),  
    array('I', (  0,256,128,   0,  0,  0,   0, 32,  0)),  
    
    array('I', (128,  0,  0,   0, 32,  0,   0,  0,  4)),  
    array('I', (  8,  0,  0, 128,  0,  4,   0,  0,  1)),  
    array('I', ( 64,  0,  0,   0,  2,  0,   0,  0, 32)),  
    
    array('I', (  0, 32,  0,   0,  0,  0,   2,128,  0)),  
    array('I', (  0,  0,  0,   8,  1,256,   0,  0, 16)),  
    array('I', (  0,  0,  0,   0,128,  0,   0, 64,256)), 
])

class TestParsers(unittest.TestCase):
    def setUp(self):
        self.correct = CORRECT_INCOMPLETE
        self.correct_native = CORRECT_INCOMPLETE_NATIVE
        self.native_numbers = NATIVE_NUMBERS
    
    def test_comma_separated(self):
        result = parsers.comma_separated('5,3,0,0,7,0,0,0,0,6,0,0,1,9,5,0,0,'+
            '0,0,9,8,0,0,0,0,6,0,8,0,0,0,6,0,0,0,3,4,0,0,8,0,3,0,0,1,7,0,0,0,'+
            '2,0,0,0,6,0,6,0,0,0,0,2,8,0,0,0,0,4,1,9,0,0,5,0,0,0,0,8,0,0,7,9'
        )
        self.assertEqual(self.correct, result)
    
    def test_table(self):
        result = parsers.table(
'''5,3,0,0,7,0,0,0,0
6,0,0,1,9,5,0,0,0
0,9,8,0,0,0,0,6,0
8,0,0,0,6,0,0,0,3
4,0,0,8,0,3,0,0,1
7,0,0,0,2,0,0,0,6
0,6,0,0,0,0,2,8,0
0,0,0,4,1,9,0,0,5
0,0,0,0,8,0,0,7,9'''
)
        self.assertEqual(self.correct, result)
    
    def test_convert_to_native_number(self):
        for number in range(10):
            self.assertEqual(
                self.native_numbers[number], 
                parsers.convert_to_native_number(number)
            )

    def test_convert_to_native_sudoku(self):
        self.assertEqual(
            self.correct_native, 
            parsers.convert_to_native_sudoku(self.correct)
        )

class TestNativeSudoku(unittest.TestCase):
    def setUp(self):
        self.sudoku = CORRECT_INCOMPLETE_NATIVE
    
    def test_equality(self):
        self.assertEqual(self.sudoku, sudoku.NativeSudoku([
            array('I', ( 16,  4,  0,   0, 64,  0,   0,  0,  0)),  
            array('I', ( 32,  0,  0,   1,256, 16,   0,  0,  0)),  
            array('I', (  0,256,128,   0,  0,  0,   0, 32,  0)),  
            
            array('I', (128,  0,  0,   0, 32,  0,   0,  0,  4)),  
            array('I', (  8,  0,  0, 128,  0,  4,   0,  0,  1)),  
            array('I', ( 64,  0,  0,   0,  2,  0,   0,  0, 32)),  
            
            array('I', (  0, 32,  0,   0,  0,  0,   2,128,  0)),  
            array('I', (  0,  0,  0,   8,  1,256,   0,  0, 16)),  
            array('I', (  0,  0,  0,   0,128,  0,   0, 64,256)), 
        ]))
        self.assertNotEqual(self.sudoku, sudoku.NativeSudoku([
            array('I', ( 16,  8,  0,   0, 64,  0,   0,  0,  0)),  
            array('I', ( 32,  0,  0,   1,256, 16,   0,  0,  0)),  
            array('I', (  0,256,128,   0,  0,  0,   0, 32,  0)),  
            
            array('I', (128,  0,  0,   0, 32,  0,   0,  0,  4)),  
            array('I', (  8,  0,  0, 128,  0,  4,   0,  0,  1)),  
            array('I', ( 64,  0,  0,   0,  2,  0,   0,  0, 32)),  
            
            array('I', (  0, 32,  0,   0,  0,  0,   2,128,  0)),  
            array('I', (  0,  0,  0,   8,  1, 32,   0,  0, 16)),  
            array('I', (  0,  0,  0,   0,128,  0,   0, 64,256)), 
        ]))
    
    def test_get_row(self):
        self.assertEqual(
            array('I', (32, 0, 0, 1, 256, 16, 0, 0, 0)),  
            self.sudoku.get_row(1)
        )
    
    def test_get_col(self):
        self.assertEqual(
            array('I', (0, 1, 0, 0, 128, 0, 0, 8, 0)), 
            self.sudoku.get_col(3)
        )
    
    def test_get_box(self):
        self.assertEqual(
            [ 
                array('I', (  0,   0,   0)), 
                array('I', (  0,   0,   0)), 
                array('I', (  0,  32,   0)) 
            ], self.sudoku.get_box(0, 2)
        )
    
    def test_get_cell(self):
        self.assertEqual(32, self.sudoku.get_cell(1, 0))
        self.assertEqual(256, self.sudoku.get_cell(7, 5))
    
    def test_iterating_cells(self):
        values = (
            16, 4,  0, 0, 64, 0, 0, 0, 0,  
            32, 0,  0,   1, 256, 16, 0, 0, 0,  
            0, 256, 128, 0, 0, 0, 0, 32,  0,  
            128, 0, 0, 0, 32,  0,  0,  0,  4,  
            8, 0, 0, 128, 0, 4, 0, 0, 1,  
            64, 0, 0, 0, 2, 0, 0, 0, 32,  
            0, 32, 0, 0, 0, 0, 2, 128, 0,  
            0, 0, 0, 8, 1, 256, 0, 0, 16,  
            0, 0, 0, 0, 128, 0, 0, 64, 256 
        )
        generator = self.sudoku.iterate_cells()
        for value in values:
            val, row, col = next(generator)
            self.assertEqual(value, val)

    def test_iterating_row(self):
        values = (128, 0, 0, 0, 32, 0, 0, 0, 4)
        generator = self.sudoku.iterate_row(3)
        for col in range(9):
            value, ignore = next(generator)
            self.assertEqual(values[col], value)
        
    def test_iterating_col(self):
        values = (0, 0, 128, 0, 0, 0, 0, 0, 0)
        generator = self.sudoku.iterate_col(2)
        for row in range(9):
            value, ignore = next(generator)
            self.assertEqual(values[row], value)
    
    def test_iterating_box(self):
        values = ((128, 0, 0), (8, 0, 0), (64, 0, 0))
        generator = self.sudoku.iterate_box(1, 0)
        for y in range(3):
            for x in range(3):
                value, *ignore = next(generator)
                self.assertEqual(values[y][x], value)
    
    def test_checking(self):
        self.assertEqual(True, self.sudoku.is_valid())
        self.assertEqual(False, sudoku.NativeSudoku([
            array('I', ( 16,  4,  0,   0, 64,  0,   0,  0,  0)),  
            array('I', ( 32,  0,  0,   1,256, 16,   0,  0,  0)),  
            array('I', (  0,256,128,   0,  0,  0,   0, 32,256)),  
            
            array('I', (128,  0,  0,   0, 32,  0,   0,  0,  4)),  
            array('I', (  8,  0,  0, 128,  0,  4,   0,  0,  1)),  
            array('I', ( 64,  0,  0,   0,  2,  0,   0,  0, 32)),  
            
            array('I', (  0, 32,  0,   0,  0,  0,   2,128,  0)),  
            array('I', (  0,  0,  0,   8,  1,256,   0,  0, 16)),  
            array('I', (  0,  0,  0,   0,128,  0,   0, 64, 16)), 
            ]).is_valid()
        )

class TestSolving(unittest.TestCase):
    def setUp(self):
        self.test_sudoku = CORRECT_INCOMPLETE_NATIVE
        self.answer = sudoku.NativeSudoku([
            array('I', ( 16,   4,   8,  32,  64, 128, 256,   1,   2)),
            array('I', ( 32,  64,   2,   1, 256,  16,   4,   8, 128)),
            array('I', (  1, 256, 128,   4,   8,   2,  16,  32,  64)),
            array('I', (128,  16, 256,  64,  32,   1,   8,   2,   4)),
            array('I', (  8,   2,  32, 128,  16,   4,  64, 256,   1)),
            array('I', ( 64,   1,   4, 256,   2,   8, 128,  16,  32)),
            array('I', (256,  32,   1,  16,   4,  64,   2, 128,   8)),
            array('I', (  2, 128,  64,   8,   1, 256,  32,   4,  16)),
            array('I', (  4,   8,  16,   2, 128,  32,   1,  64, 256))
        ])
        self.map = solvers.Map(self.test_sudoku)
    
    def test_map_get_values(self):
        self.assertEqual(0b101010000, self.map.get_values(4, 6))
        self.assertEqual(0b000011000, self.map.get_values(3, 4))
    
    def test_simple_solver(self):
        sudoku = solvers.simple_solver(self.test_sudoku)
        self.assertEqual(self.answer, sudoku)

def load_tests(loader, tests, ignored):
    """Loads doctests"""
    for module in (parsers, printers, sudoku, solvers):
        tests.addTests(
            doctest.DocTestSuite(module, extraglobs={
                    'sudoku':CORRECT_INCOMPLETE_NATIVE,
                    'map_':solvers.Map(CORRECT_INCOMPLETE_NATIVE)
                }
            )
        )
    tests.addTests(doctest.DocTestSuite(parsers))
    return tests

if __name__ == "__main__":
    unittest.main()
