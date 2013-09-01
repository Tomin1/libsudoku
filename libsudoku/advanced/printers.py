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

from ..sudoku import NATIVE_NUMBERS
from ..printers import convert_to_character

def generate_html_debug_page(
        sudoku:'..sudoku.NativeSudoku', 
        map_:'..solvers.Map'=None,
        solver:'function'=None, 
        ) -> str:
    """Prints a HTML page for debugging"""
    html = """<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>Sudoku debug information</title>
    <meta name="generator" content="libsudoku" />
    <style type="text/css">
    #sudoku, .values { border-collapse: collapse }
    #sudoku * { 
        margin: 0;
        padding: 0;
        position: relative; 
    }
    #sudoku > tr, #sudoku > tbody > tr { height: 4em; }
    #sudoku > tr > td, #sudoku > tbody > tr > td {
        border: 2px solid black;
        height: 3em;
        width: 3em;
    }
    #sudoku .row_2 { border-bottom: 5px solid black; }
    #sudoku .row_5 { border-bottom: 5px solid black; }
    #sudoku .col_2 { border-right: 5px solid black; }
    #sudoku .col_5 { border-right: 5px solid black; }
    .number { 
        font-size: xx-large;
        text-align: center;
        z-index: 100;
    }
    .values { 
        color: grey;
        height: 100%;
        left: 0;
        position: absolute !important;
        top: 0;
        width: 100%;
    }
    .values td { 
        font-size: small;
        height: 33%;
        text-align: center;
        width: 33%;
    }
    .values td.border-left { border-left: 1px solid lightgrey; }
    .values td.border-right { border-right: 1px solid lightgrey; }
    .values td.border-top { border-top: 1px solid lightgrey; }
    .values td.border-bottom { border-bottom: 1px solid lightgrey; }
    </style>
</head>
<body>
    <table id="sudoku">
"""
    previous_row = None
    for value, row, col in sudoku.iterate_cells():
        if row != previous_row:
            if previous_row is not None:
                html += "    "*2
                html += "</tr>\n"
            html += "    "*2
            html += "<tr class=\"row_"
            html += str(row)
            html += "\">\n"
            previous_row = row
        html += "    "*3
        html += "<td class=\"col_"
        html += str(col)
        html += "\">\n"
        if value != 0:
            html += "    "*4
            html += "<div class=\"number\">"
            html += convert_to_character(value)
            html += "</div>\n"
        elif map_:
            html += "    "*4
            html += "<table class=\"values\">\n"
            values = map_.get_values(row, col)
            for r in range(3):
                html += "    "*5
                html += "<tr>\n"
                for c in range(3):
                    borders = ""
                    if c > 0: borders += " border-left"
                    if c < 2: borders += " border-right"
                    if r > 0: borders += " border-top"
                    if r < 2: borders += " border-bottom"
                    html += "    "*6
                    html += "<td class=\""
                    html += borders[1:]
                    html += "\">"
                    number = NATIVE_NUMBERS[r*3 + c + 1]
                    if number & values:
                        html += convert_to_character(number)
                    html += "</td>\n"
                html += "    "*5
                html += "</tr>\n"
            html += "    "*4
            html += "</table>\n"
        html += "    "*3
        html += "</td>\n"
    html += "    </table>\n"
    html += "    <p id=\"completed\"> Status: "
    if sudoku.is_valid:
        if sudoku.filled:
            html += "Completed" 
        else: 
            html += "Incomplete"
    else:
        html += "Failed"
    html += "</p>\n"
    html += "    <p id=\"percentage\">Filled: "
    html += str(round(sudoku.readyness * 100, 2))
    html += " %</p>\n"
    html += "    <p id=\"solver\">Solver: "
    html += solver.__name__ if solver else "N/A"
    html += "</p>\n"
    html += "</body>"
    return html
