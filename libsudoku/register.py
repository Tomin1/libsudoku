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
from types import FunctionType

class Register:
    """libsudoku module register"""
    _parsers = {}
    _solvers = {}
    _printers = {}
    
    @classmethod
    def parser(cls, parser:FunctionType=None, name:str=None) -> FunctionType:
        """Decorator: Registers a parser function"""
        if name is None:
            cls._parsers[parser.__name__] = parser
        else:
            def register(parser):
                cls._parsers[name] = parser
                return parser
            return register
        return parser
    
    @classmethod
    def solver(cls, solver:FunctionType=None, name:str=None) -> FunctionType:
        """Decorator: Registers a solver function"""
        if name is None:
            cls._solvers[solver.__name__] = solver
        else:
            def register(solver):
                cls._solvers[name] = solver
                return solver
            return register
        return solver
    
    @classmethod
    def printer(cls, printer:FunctionType=None, name:str=None) -> FunctionType:
        """Decorator: Registers a printer function"""
        if name is None:
            cls._printers[printer.__name__] = printer
        else:
            def register(printer):
                cls._printers[name] = printer
                return printer
            return register
        return printer
    
    @classmethod
    def get_parser(cls, name:str) -> "FunctionType|None":
        """Returns a parser function that fits the name or None"""
        from .parsers import convert_to_native_sudoku
        parser = cls._parsers.get(name)
        if parser is None:
            return None
        def _parser(*args, **kwargs):
            return convert_to_native_sudoku(parser(*args, **kwargs))
        return _parser
    
    @classmethod
    def get_solver(cls, name:str) -> "FunctionType|None":
        """Returns a solver function that fits the name or None"""
        return cls._solvers.get(name)
    
    @classmethod
    def get_printer(cls, name:str) -> "FunctionType|None":
        """Returns a printer function that fits the name or None"""
        return cls._printers.get(name)
    
    @classmethod
    def get_parsers(cls) -> "(str, ...)":
        """Returns a tuple of parser function names"""
        return list(cls._parsers.keys())
    
    @classmethod
    def get_solvers(cls) -> "(str, ...)":
        """Returns a tuple of solver function names"""
        return list(cls._solvers.keys())
    
    @classmethod
    def get_printers(cls) -> "(str, ...)":
        """Returns a tuple of printer function names"""
        return list(cls._printers.keys())

def discover():
    """Tries to find all parsers, solvers and printers in libsudoku"""
    from . import parsers, solvers, printers
