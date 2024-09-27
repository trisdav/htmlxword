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
from . import htmlxword
import os
def staticSite(name, input, title="", customHtml="", customCss="", customJs="", customYaml="", json=False):
    xword = htmlxword.htmlxword()
    if (customHtml):
        xword.setHtmlPath(customHtml)
    if (customCss):
        xword.setCssPath(customCss)
    if (customJs):
        xword.setJsPath(customJs)
    if (customYaml):
        xword.setYamlPath(customYaml)
    if (json):
        input = xword.parseJson(input)
    xword.createStaticPage(name, input, title)


if __name__ == "__main__":
    # This is a test script.
    words = [
        'Happy Joy',
        'Mystery Riddle',
        'Secretive Hush',
        'Idealistic Optimistic',
        'Bubbly Soap',
        'Sad Cry',
        'Luck Draw',
        'Indescribable Confusing',
        'Strong Manly',
        'Airy Fluffy, light'
    ]

    staticSite("test.html", words, "test title")
