#!/usr/bin/env python3
# 
# Sudoku solver. Frontend for libsudoku
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

import argparse
from libsudoku.register import Register, discover
from libsudoku.parsers import ParsingError
from libsudoku.solvers import SolvingError

def parse_arguments(*args) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sudoku solver")
    parser.add_argument(
        '-v', '--verbose', '--verbosity', 
        action='store_true', 
        default=False, 
        dest='verbosity', 
        help="Print verbose output"
    )
    parser.add_argument(
        '-x', '--raise-exceptions', 
        action='store_true', 
        default=False, 
        dest='exceptions', 
        help="Raise Python exceptions"
    )
    parser.add_argument(
        '-r', '--parser', 
        choices=Register.get_parsers(), 
        default='list', 
        help="Parser to use (default: %(default)s)"
    )
    parser.add_argument(
        '-e', '--separator',
        help='Separator to be used when parsing sudoku'
    )
    parser.add_argument(
        '-s', '--solver', 
        nargs=1, 
        default='simple', 
        choices=Register.get_solvers(), 
        help="Solver to use (default: %(default)s)"
    )
    parser.add_argument(
        '-p', '--print', 
        choices=Register.get_printers(), 
        default='none', 
        dest='printer', 
        help="Printing style (default: %(default)s)"
    )

    parser.add_argument(
        '-f', '--file', 
        action='append', 
        dest='files', 
        metavar='FILE', 
        type=argparse.FileType(), 
        help='File containing a sudoku. Use - to read from stdin'
    )
    parser.add_argument(
        '-i', '--input', 
        action='append', 
        dest='sudokus', 
        metavar='SUDOKU', 
        help="Give sudoku as an argument"
    )
    parser.add_argument(
        '-o', '--output', 
        default='-', 
        type=argparse.FileType('w'), 
        help="Output file. Use - to output to stdout. (default: %(default)s)"
    )
    parser.add_argument(
        '-1', 
        action='store_true', 
        dest='single', 
        help="Solve and print only one solution"
    )
    if args:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()
    if isinstance(args.solver, list): # A little fix
        args.solver = args.solver[0]
    return args

class UIError(Exception):
    pass

def parse(
        sudoku:str, 
        parser_name:str, 
        args:"Namespace"
        ) -> "sudoku.NativeSudoku":
    """Calls correct parser for sudoku string and returns result"""
    parser = Register.get_parser(parser_name)
    if parser is None:
        raise UIError("Invalid parser name {}".format(parser_name))
    try:
        return parser(sudoku)
    except ParsingError as error:
        if args.verbosity:
            print("Parser returned error '{}' with value '{}'".format(
                error, error.value
            ))
        else:
            print("Parser returned error '{}'".format(error))
        if args.exceptions:
            raise

def solve(
        sudoku:"sudoku.NativeSudoku", 
        solver_name:str, 
        args:"Namespace"
        ) -> "sudoku.NativeSudoku|[sudoku.NativeSudoku, ...]":
    """Solves NativeSudoku with solver determined by solver"""
    solver = Register.get_solver(solver_name)
    if solver is None:
        raise UIError("Invalid solver name {}".format(solver_name))
    try:
        return solver(sudoku)
    except SolvingError as error:
        print("Solver returned error '{}'".format(error))
        if args.verbosity:
            print("Incomplete sudoku: ", end="")
            Register.get_printer('list')(error.sudoku)
        if args.exceptions:
            raise

def output(
        sudoku:"sudoku.NativeSudoku", 
        printer_name:str, 
        separator:str, 
        output:"io.BufferWriter", 
        args:"Namespace"
        ):
    """Outputs the sudoku as printer wants it"""
    printer = Register.get_printer(printer_name)
    if printer is None:
        raise UIError("Invalid printer name {}".format(printer_name))
    printer(sudoku)

def process(string:str, args:"Namespace"):
    """Processes string by arguments"""
    sudoku = parse(string, args.parser, args)
    if sudoku:
        if args.verbosity:
            print("Parsed sudoku")
        sudoku = solve(sudoku, args.solver, args)
    if sudoku:
        if args.verbosity:
            print("Solved sudoku")
        if isinstance(sudoku, list):
            i = 1
            for sudoku_ in sudoku:
                print("Solution {}:".format(i))
                output(sudoku_, args.printer, args.separator, args.output, args)
                i += 1
        else:
            output(sudoku_, args.printer, args.separator, args.output, args)

def main(*args):
    args = parse_arguments(*args)
    discover()
    if not args.files and not args.sudokus:
        raise NotImplementedError("Called without --file or --input")
    else:
        if args.files:
            for file_ in args.files:
                if args.verbosity:
                    print("Processing file: {}".format(file_.name))
                sudoku = file_.read()
                if sudoku.endswith("\n"):
                    sudoku = sudoku[:-1]
                process(sudoku, args)
        if args.sudokus:
            for string in args.sudokus:
                if args.verbosity:
                    print("Processing argument: {}".format(string))
                process(string, args)

if __name__ == "__main__":
    main()
