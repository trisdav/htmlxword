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
#!/bin/python3
from genxword.control import Genxword
from genxword.calculate import Crossword
from genxword.calculate import Exportfiles
import base64
import json
import yaml
import os
base_dir = os.path.abspath(os.path.dirname(__file__))

def cluesAsLists(efs, configStruct):
    # Create clue section
    acrossClues = ""
    downClues = ""
    # Create a list of the clues
    for clue in efs.wordlist:
        word, clue_text, row, col, vertical, num = clue[:6]
        # Assume direction is across until seen otherwise.
        direction = "across"
        if (vertical == 1):
            direction = "down"

        clueReplace = {}
        clueReplace["CLUE_NUMBER"] = num
        clueReplace["CLUE_TEXT"] = clue_text
        clueReplace["DIRECTION"] = direction
        clueReplace["LENGTH"] = len(word)
        clueReplace["ROW"] = row
        clueReplace["COLUMN"] = col
        if vertical:
            downClues += configStruct["clueListItem"].format(**clueReplace)
        else:
            acrossClues += configStruct["clueListItem"].format(**clueReplace)
    
    clues = configStruct["clueListDown"].format(downClues) + configStruct["clueListAcross"].format(acrossClues)
    return clues

def genFromFile(input):
    gen = Genxword(auto=True, mixmode=False)
    with open(input) as infile:
        gen.wlist(infile)
    gen.grid_size()
    return gen

def genFromList(input):
    gen = Genxword(auto=True, mixmode=False)
    gen.wlist(input, len(input))
    gen.grid_size()
    return gen

def getGen(input):
    gen = None
    if isinstance(input, list):
        gen = genFromList(input)
    elif isinstance(input, str):
        gen = genFromFile(input)
    return gen

def loadTemplate(defaultTemplate, customTemplate):
    templatePath = defaultTemplate
    templateString = ""
    if (customTemplate != ""):
        templatePath = customTemplate

    with open(templatePath) as templateStream:
        templateString = templateStream.read()
    return templateString

def getCrosswordGrid(efs, configStruct, calc):
    rowIdx = 0
    crosswordGrid = ""
    for row in calc.grid:
        newRow = ""
        # Create cells
        colIdx=0
        for col in row:
            if (col == "-"):
                newRow += configStruct["blankBlock"].format(**{"ROW":rowIdx,"COLUMN":colIdx})
            else:
                # Look for where to place the word number
                firstWord = False
                wordNumber = 0
                for word in efs.wordlist:
                    if(word[2] == rowIdx and word[3] == colIdx):
                        firstWord = True
                        wordNumber = word[5]
                        break
                rc = {"ROW":str(rowIdx), "COLUMN":str(colIdx), "SUPER_SCRIPT":""}
                if firstWord:
                    rc["SUPER_SCRIPT"] = configStruct["superScript"].format(**{"REPLACE":str(wordNumber)})
                newRow += configStruct["letterBlock"].format(**rc)
            colIdx += 1
        rowIdx += 1
        crosswordGrid += "\n" + configStruct["crossWordRowHtml"].format(**{"ROW_CONTENT":newRow})
    return crosswordGrid

def formatWordList(efs):
    # Modify word list to be :
    # [ WORD, len(word), row(start), col(start), direction, clue number ]
    newWordList = efs.wordlist
    for i in range(0, len(newWordList)):
        if newWordList[i][4] == 1:
            newWordList[i][4] = "down"
        else:
            newWordList[i][4] = "across"
        newWordList[i][1] = len(newWordList[i][0])
    return newWordList

def base64List(newWordList):
    # Encode it as json, then encode it as base64.
    return str(base64.b64encode(bytes(json.dumps(newWordList), 'ascii'))).lstrip("b")

def staticSite(name, input, title="", customHtml="", customCss="", customJs="", customYaml=""):
    gen = getGen(input)
    calc = Crossword(gen.nrow, gen.ncol, '-', gen.wordlist)
    print(calc.compute_crossword())
    # Default template paths.
    htmlPath = os.path.join(base_dir, "data", "html_xword_template.html")
    cssPath = os.path.join(base_dir, "data", 'csstemplate.css')
    jsPath = os.path.join(base_dir, "data", 'jstemplate.js')
    yamlPath = os.path.join(base_dir, "data", 'config.yaml')

    htmlFormat = ""
    htmlValues = {"CROSSWORD":"", "CLUES":"", "SOLUTIONBASE64":"", "CSS":"", "JS":"", "TITLE":title}
    configStruct = {}
    
    htmlFormat = loadTemplate(htmlPath, customHtml)
    htmlValues["CSS"] = loadTemplate(cssPath, customCss)
    htmlValues["JS"] = loadTemplate(jsPath, customJs)
    configStruct = yaml.safe_load(loadTemplate(yamlPath, customYaml))

    efs = Exportfiles(gen.nrow, gen.ncol, calc.best_grid, calc.best_wordlist)
    efs.order_number_words()
    efs.wordlist

    # Create list of clues.
    htmlValues["CLUES"] += cluesAsLists(efs, configStruct)
    # Create the crossword grid.
    htmlValues["CROSSWORD"] = getCrosswordGrid(efs, configStruct, calc)
    # Format the word list for the html page.
    newWordList = formatWordList(efs)
    # Base64 the word list to prevent peeking.
    htmlValues["SOLUTIONBASE64"] = base64List(newWordList)
    # Set the column dimension.
    htmlValues["COLUMNDIMENSION"] = gen.ncol
    # Build the whole html
    htmlFormat = htmlFormat.format(**htmlValues)
    with open(name, 'w') as html_file:
        html_file.write(htmlFormat)

if __name__ == "__main__":
    # This is a test script.
    words = [
        'Happy',
        'Mystery',
        'Secretive',
        'Idealistic',
        'Bubbly',
        'Sad',
        'Luck',
        'Indescribable',
        'Strong',
        'Airy'
    ]

    staticSite("test.html", words, "test title")
