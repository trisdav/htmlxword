# htmlxword
## htmlxword is
A python library that can create a interactive crossword, from an input text file, on a static page using html and javascript.

## htmlxword usage
* Basic usage:
```bash
htmlxword inputfile.txt -o myCrossword.html -t "Crossword Title"
```
* Example input file:
```
Noun Person, place, or thing.
adverb A word or phrase that modifies or qualifies an adjective.
adjective A word or phrase describing an attribute.
paragraph A section of a piece of writing.
chapter A section marker in a book.
```
* Arguments

| short | long | description |
| ----------- | ----------- | ----------- |
| -o | --output | What the output file should be named. |
| -t | --title | Add a title to the crossword page. |
| -y | --config-yaml | Path to a custom yaml config file. |
| -c | --css-template | Path to a custom css file. |
| -j | --javascript | Path to a custom javascript file. |
| -m | --html-tempalte | Path to a custom html template file. |
|      | --print-config | Print the contents of the default config.yaml. |
|      | --print-css | Print the contents of the default csstemplate.css. |
|      | --print-javascript | Print the contents of the default jstemplate.js. |
|      | --print-html | Print the contnets of the default html_xword_template.html. |

## htmlxword depends on
The python library genxword, which creates crosswords and various formats. This uses genxword to create a layout for the crossword, and then builds a crossword in html and javascript. Genxword has several dependenices, I would refer to that project to determine the dependencies.

## Configurability
The heart of configurability of this project is in html_xword_template.html.
Inside that file there are strings like {JS}, {CLUE} which define where to insert
generated code segments. Other things can be configred in config.yaml I strongly
advise viewing the template files for figuring out how to configure the outputs.
* jstemplate.js, {JS}
* csstemplate.css, {CSS}

### config.yaml
* superScript - Defines the html of the superscript in the first block signifying the start of a word.
* letterBlock - Defines html of the crossword blocks that accepts inputs.
* blankBlock - Defines html of the crossword blocks that is an empty cell.
* crossWordRowHtml - Defines html of a crow in the crossword.
* clueHtml - Defines html of the clue text.
* clueListDown - Defines the list which holds the Down clues.
* clueListAcross - Defines the list whcih holds the Across clues.
* clueListItem - Defines an item in the clue list.



