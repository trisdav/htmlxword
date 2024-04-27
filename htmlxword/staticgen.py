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

def staticSite(name, gen, calc, title="", customHtml="", customCss="", customJs="", customYaml=""):
    htmlFormat = ""
    htmlValues = {"CROSSWORD":"", "CLUES":"", "SOLUTIONBASE64":"", "CSS":"", "JS":"", "TITLE":title}
    configStruct = {}
    
    # Set up custom inputs.
    htmlTemplatePath = os.path.join(base_dir, "data", "html_xword_template.html")
    if(customHtml != ""):
        htmlTemplatePath = customHtml

    cssPath = os.path.join(base_dir, "data", 'csstemplate.css')
    if(customCss != ""):
        cssPath = customCss

    jsPath = os.path.join(base_dir, "data", 'jstemplate.js')
    if(customJs != ""):
        jsPath = customJs

    yamlPath = os.path.join(base_dir, "data", 'config.yaml')
    if(customYaml != ""):
        yamlPath = customYaml

    with open(htmlTemplatePath) as htmlTemplateFile:
        htmlFormat = htmlTemplateFile.read()
    with open(cssPath) as cssTemplateFile:
        htmlValues["CSS"] = cssTemplateFile.read()
    with open(jsPath) as jsTemplateFile:
        htmlValues["JS"] = jsTemplateFile.read()
    with open(yamlPath) as configFile:
        configStruct = yaml.safe_load(configFile)

    efs = Exportfiles(gen.nrow, gen.ncol, calc.best_grid, calc.best_wordlist)
    efs.order_number_words()
    efs.wordlist

    htmlValues["CLUES"] += cluesAsLists(efs, configStruct)

    # Create the rows
    solution = [['#' if col == '-' else col for col in row] for row in calc.grid]
    rowIdx=0
    for row in solution:
        newRow = ""
        # Create cells
        colIdx=0
        for col in row:
            if (col == "#"):
                newRow += configStruct["blankBlock"].format(**{"ROW":rowIdx,"COLUMN":colIdx})
            else:
                # Look for where to place the word number
                firstWord=False
                wordNumber=0
                for word in efs.wordlist:
                    if(word[2] == rowIdx and word[3] == colIdx):
                        firstWord=True
                        wordNumber=word[5]
                        break
                rc = {"ROW":str(rowIdx), "COLUMN":str(colIdx), "SUPER_SCRIPT":""}
                if firstWord:
                    rc["SUPER_SCRIPT"] = configStruct["superScript"].format(**{"REPLACE":str(wordNumber)})
                newRow += configStruct["letterBlock"].format(**rc)
            colIdx+=1
        rowIdx+=1
        htmlValues["CROSSWORD"] += "\n" + configStruct["crossWordRowHtml"].format(**{"ROW_CONTENT":newRow})

    # Modify word list to be :
    # [ WORD, len(word), row(start), col(start), direction, clue number ]
    newWordList = efs.wordlist
    for i in range(0, len(newWordList)):
        if newWordList[i][4] == 1:
            newWordList[i][4] = "down"
        else:
            newWordList[i][4] = "across"
        newWordList[i][1] = len(newWordList[i][0])
    # Encode it as json, then encode it has base64 to prevent peeking.
    htmlValues["SOLUTIONBASE64"] = str(base64.b64encode(bytes(json.dumps(newWordList), 'ascii'))).lstrip("b")
    # Set the column dimension.
    htmlValues["COLUMNDIMENSION"] = gen.ncol
    # Build the whole html
    htmlFormat = htmlFormat.format(**htmlValues)
    with open(name, 'w') as html_file:
        html_file.write(htmlFormat)


def gengrid(gen):
    i = 0
    while 1:
        calc = Crossword(gen.nrow, gen.ncol, '-', gen.wordlist)
        print(calc.compute_crossword())
        if float(len(calc.best_wordlist))/len(gen.wordlist) < 0.9 and i < 5:
            gen.nrow += 2; gen.ncol += 2
            i += 1
        else:
            break
    return calc

if __name__ == "__main__":
    # This is a test script.
    gen = Genxword(auto=True, mixmode=False)
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
    gen.wlist(words, 10)
    gen.grid_size()
    calc = gengrid(gen)

    staticSite("test.html", gen, calc, "test title")
