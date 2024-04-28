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
import os
base_dir = os.path.abspath(os.path.dirname(__file__))

def printConfigs(printConfig, printCss, printJs, printHtml):
    if printConfig:
        yamlPath = os.path.join(base_dir, "data", 'config.yaml')
        with open(yamlPath, "r") as config:
            print(config.read())
        return
    if printCss:
        cssPath = os.path.join(base_dir, "data", 'csstemplate.css')
        with open(cssPath, "r") as config:
            print(config.read())
        return
    if printJs:
        jsPath = os.path.join(base_dir, "data", 'jstemplate.js')
        with open(jsPath, "r") as config:
            print(config.read())
        return
    if printHtml:
        htmlTemplatePath = os.path.join(base_dir, "data", "html_xword_template.html")
        with open(htmlTemplatePath, "r") as config:
            print(config.read())
        return

def main():
    parser = argparse.ArgumentParser(description='html & JS crossword generator.', prog='staticgen')
    parser.add_argument('infile', nargs="?", help='Name of word list file.')
    parser.add_argument('-o', '--output', dest='output', default='test', help="What the output file should be named.")
    parser.add_argument('-t', '--title', dest='title', default='', help="Add a title to the crossword page.")
    parser.add_argument('-y', '--config-yaml', dest='yaml', default='', help="Path to a custom yaml config file.")
    parser.add_argument('-c', '--css-template', dest='css', default='', help="Path to a custom css file.")
    parser.add_argument('-j', '--javascript', dest='js', default='', help="Path to a custom javascript file.")
    parser.add_argument('-m', '--html-tempalte', dest='html', default='', help="Path to a custom html template file.")
    parser.add_argument('--print-config', dest="printConfig", action="store_true", help="Print the contents of the default config.yaml.")
    parser.add_argument('--print-css', dest="printCss", action="store_true" , help="Print the contents of the default csstemplate.css.")
    parser.add_argument('--print-javascript', dest="printJs", action="store_true", help="Print the contents of the default jstemplate.js.")
    parser.add_argument('--print-html', dest="printHtml", action="store_true", help="Print the contnets of the default html_xword_template.html.")
    args = parser.parse_args()

    if args.infile:
        staticgen.staticSite(args.output, args.infile, args.title, args.html, args.css, args.js, args.yaml)
    elif (args.printConfig or args.printCss or args.printJs or args.printHtml):
        printConfigs(args.printConfig, args.printCss, args.printJs, args.printHtml)
    else:
        parser.error("Invalid inputs.")