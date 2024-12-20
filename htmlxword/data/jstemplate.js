/*
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
 */
var lastCell = -1;
solLst = JSON.parse(atob(solution));
function check() {
    for(let i = 0; i < solLst.length; i++) {
        word = solLst[i];
        wordLen = word[1];
        startRow = word[2]; // not 0 based
        startCol = word[3];

        if(word[4] == "down") {
            for (let j = 0; j < wordLen; j++) {
                row = (startRow + j);
                selector = "input[row=\"" + row + "\"][column=\"" + startCol + "\"]";
                inputField = document.querySelector(selector);
                if (inputField.value.toUpperCase() != word[0][j]) {
                    document.getElementById("checkOverlayText").textContent = "Something isn't right, try again."
                    document.getElementById("checkOverlay").style.display = "block";
                    return;
                }
            }
        }
        else {
            for (let j = 0; j < wordLen; j++) {
                column = (startCol + j);
                selector = "input[row=\"" + startRow + "\"][column=\"" + column + "\"]";
                inputField = document.querySelector(selector);
                if (inputField.value.toUpperCase() != word[0][j]) {
                    document.getElementById("checkOverlayText").textContent = "Something isn't right, try again."
                    document.getElementById("checkOverlay").style.display = "block";
                    return;
                }
            }
        }
    }
    // If we make it this far then it didn't fail.
    document.getElementById("checkOverlayText").textContent = "\u{1F389} You got it! You're awesome. \u{1F38A}";;
    document.getElementById("checkOverlayText").className = "overlayTextWin";
    document.getElementById("checkOverlay").style.display = "block";
}

function moveToCell(index) {
    var inputFields = document.querySelectorAll('input.hintHighlight');
    if ( inputFields.length == 0 ) {
        guessMove(index);
    }
    else {
        moveToHighlighted(index, inputFields);
    }
}

function moveToHighlighted(index, highlightedFields) {
    var inputFields = document.querySelectorAll('input');
    for ( var i = 0; i < highlightedFields.length; ++i) {
        if ( inputFields[index] == highlightedFields[i] ) {
            if (i + 1 < highlightedFields.length) {
                highlightedFields[i+1].focus();
                return;
            }
        }
    }
}

// This attemps to guess where the next character is.
function guessMove(index) {
    var inputFields = document.querySelectorAll('input');
    var thisCell = index;
    var newIndex = thisCell + 1;
    console.log(thisCell);
    console.log(lastCell);

    // No clue as to which way we are going, go across.
    if (lastCell == -1) {
        newIndex = thisCell + 1;
        if (inputFields[newIndex].attributes["class"].value == "block") {
            // Only go to this case if it will work, otherwise the selection will
            //  jump awkwardly.
            if (inputFields[thisCell + dimCol].attributes["class"].value != "block") {
                newIndex = thisCell + dimCol;
            }
        }
    }

    // If the last cell was one back, assume we are going across.
    else if (lastCell == thisCell - 1) {
        newIndex = thisCell + 1;
        if (inputFields[newIndex].attributes["class"].value == "block") {
            // Only go to this case if it will work, otherwise the selection will
            //  jump awkwardly.
            if (inputFields[thisCell + dimCol].attributes["class"].value != "block") {
                newIndex = thisCell + dimCol;
            }
        }
    }
    else if (lastCell == thisCell - dimCol) { // If the last cell is above, assume we are going down.
        newIndex = thisCell + dimCol;
        if (inputFields[newIndex].attributes["class"].value == "block") {
            newIndex = thisCell + 1;
        }
    }
    // Loop until we find a valid input cell. If selection is valid there will be
    //  no iterations.
    while(inputFields[newIndex].attributes["class"].value == "block") {
        newIndex += 1;
        if (newIndex > inputFields.length) {
            newIndex = 0;
        }
    }
    lastCell = thisCell;
    inputFields[newIndex].focus();
}

var inputFieldList = document.querySelectorAll('input');
// Add event listener to each input field
inputFieldList.forEach(function(input, index) {
    input.addEventListener('input', function() {
        moveToCell(index);
    });
    // User clicks to change input.
    input.addEventListener('mousedown', function(event) {
        lastCell = -1;
    });
    // User presses tab to change input
        input.addEventListener('keydown', function(event) {
        if (event.key === 'Tab' && event.shiftKey) {
            event.preventDefault(); // Prevent the default tab behavior
            lastCell = -1;
            var index = 0;
            for ( let i = 0; i < inputFieldList.length ; ++i) {
                if (inputFieldList[i].getAttribute("row") == document.activeElement.getAttribute("row") && inputFieldList[i].getAttribute("column") == document.activeElement.getAttribute("column")) {
                    index = i;
                    break;
                }
            }
            var newIndex = -1;
            for ( let i = highlightedSelection.length; i >= 0; --i) {
                if (highlightedSelection[i] < index) {
                    newIndex = highlightedSelection[i];
                    break;
                }
            }
            if (newIndex == -1) { // Not found
                if (highlightedHintIndex == 0) {
                    hintList[hintList.length-1].click();
                }
                else {
                    hintList[highlightedHintIndex-1].click();
                }
                // hintList.click() will update highlightedSelection.
                newIndex = highlightedSelection[highlightedSelection.length-1];
            }
            inputFieldList[newIndex].focus();
        }
        else if (event.key === 'Tab') {
            event.preventDefault(); // Prevent the default tab behavior
            lastCell = -1;
            var index = 0;
            for ( let i = 0; i < inputFieldList.length ; ++i) {
                if (inputFieldList[i].getAttribute("row") == document.activeElement.getAttribute("row") && inputFieldList[i].getAttribute("column") == document.activeElement.getAttribute("column")) {
                    index = i;
                    break;
                }
            }
            var newIndex = -1;
            for ( let i = 0; i < highlightedSelection.length; ++i) {
                if (highlightedSelection[i] > index) {
                    newIndex = highlightedSelection[i];
                    break;
                }
            }
            if (newIndex == -1) { // Not found
                if (highlightedHintIndex == hintList.length-1) {
                    hintList[0].click();
                }
                else {
                    hintList[highlightedHintIndex+1].click();
                }
                // hintList.click() will update highlightedSelection.
                newIndex = highlightedSelection[0];
            }
            inputFieldList[newIndex].focus();
        }
    });
    // When focused on a cell, select all existing text.
    input.addEventListener('focus', function(event) {
        this.select();
    });
});

function setClueDivMaxHeight() {
    height = document.getElementById("crosswordTable").offsetHeight;
    document.getElementById("rightDiv").style.maxHeight = height;
}
setClueDivMaxHeight();

var hintList = document.querySelectorAll('li.hint');

function removeHintHighlight(event) {

    hintList.forEach(hint => {
        if (!event.target.closest(".hint")) {
            hint.classList.remove(".hintHighlight");
        }
    });
}

document.addEventListener("click", function(event) {
    hintList.forEach(hint => {
        // If the item clicked on is not of the class hint, then
        //  something that isn't a hint has been clicked and so
        //  the hintHighlight class should be removed.
        if (!event.target.closest('.hint') && !event.target.closest('.character')) { 
            hint.classList.remove("hintHighlight");
            deHighlight();
        }
    }); 
});

function hintListHighlightListeners() {
    // Highlight for hint strings
    hintList.forEach((hint, index) => {
        hint.addEventListener('click', function(event) {
                hintList.forEach( li => {
                if( li !== hint) {
                    li.classList.remove("hintHighlight")
                }
            });
            hint.classList.add("hintHighlight");
            highlightRange(hint.getAttribute("direction"), hint.getAttribute("row"), hint.getAttribute("column"), hint.getAttribute("length"), index);
        });
    });
}
hintListHighlightListeners();

// This is that first box which has the super script indicating the start of a word.
function firstLetterHighlightListeners() {
    var firstLetterInputs = document.querySelectorAll("div.input-container");
    firstLetterInputs.forEach( input => {
        input.addEventListener("click", function(event) {
            var superscriptHtml = input.getElementsByClassName("superscript-number");
            var superscript = NaN;
            if (superscriptHtml.length > 0) {
                superscript = Number(superscriptHtml[0].innerHTML);
            }
            var hints = document.querySelectorAll("li.hint");
            for (var i = 0; i < hints.length; ++i) {
                if (hints[i].getAttribute("clueNumber") == superscript && ! hints[i].classList.contains("hintHighlight")) {
                    // use the click event of the hint to highlight things.
                    var clickEvent = new MouseEvent("click", {
                        bubbles: true,
                        cancelable: true,
                        view: window
                        });
                    hints[i].dispatchEvent(clickEvent);
                    return; // Exit the loop.
                }
            }
        });
    });
}
firstLetterHighlightListeners();

var highlightedSelection = [];
var inputFieldList = document.querySelectorAll('input');
var highlightedHintIndex = 0;
function highlightRange(direction, row, col, len, index) {
    highlightedHintIndex = index;
    var startIndex = (Number(row) * Number(dimCol)) + Number(col);
    var wordLength = Number(len);
    deHighlight();
    if (direction == "down") {
        for(var i = 0; i < wordLength; ++i) {
            index = startIndex + (dimCol * i);
            highlightedSelection.push(index);
            inputFieldList[index].classList.add("hintHighlight");
        }
    }
    else {
        for(var i = 0; i < wordLength; ++i) {
            index = startIndex + i;
            highlightedSelection.push(index);
            inputFieldList[index].classList.add("hintHighlight");
        }
    }
    highlightedSelection;
    inputFieldList[startIndex].focus();
    inputFieldList[startIndex].select();
}

function deHighlight() {
    highlightedSelection = [];
    var inputFieldList = document.querySelectorAll('input');
    for(var i = 0; i < inputFieldList.length; ++i) {
        inputFieldList[i].classList.remove("hintHighlight");
    }
}

function noneDisplay(elementId) {
    document.getElementById(elementId).style.display = "none";
}

function setDisplay(elementId, display="block") {
    document.getElementById(elementId).style.display = display;
}