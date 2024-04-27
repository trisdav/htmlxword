"""
    "htmlxword" creates a crossword in html/javascript form a text file.
    Copyright (C) 2024  Tristan Davis (tridav95@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from . import staticgen
from genxword.control import Genxword
import argparse
def main():
    parser = argparse.ArgumentParser(description='html & JS crossword generator.', prog='staticgen')
    parser.add_argument('infile', help='Name of word list file.')
    parser.add_argument('-o', '--output', dest='output', default='test', help="What the output file should be named.")
    parser.add_argument('-t', '--title', dest='title', default='', help="Add a title to the crossword page.")
    parser.add_argument('-y', '--config-yaml', dest='yaml', default='', help="Path to a custom yaml config file.")
    parser.add_argument('-c', '--css-template', dest='css', default='', help="Path to a custom css file.")
    parser.add_argument('-j', '--javascript', dest='js', default='', help="Path to a custom javascript file.")
    parser.add_argument('-m', '--html-tempalte', dest='html', default='', help="Path to a custom html template file.")
    args = parser.parse_args()
    gen = Genxword(auto=True, mixmode=False)
    with open(args.infile) as infile:
        gen.wlist(infile)
    gen.grid_size()
    calc = staticgen.gengrid(gen)

    staticgen.staticSite(args.output, gen, calc, args.title, args.html, args.css, args.js, args.yaml)