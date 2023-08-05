#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Transcript Parsing
########
##  Copyright 2017 garrick. Some rights reserved.
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.

##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU Lesser General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Parse transcript files."""

import os, html

def readTranscript(file_name):
    """
    Retrieve the contents of the transcript file.

    Parameters
    ----------
    file_name : str
        The path to the transcript file.
    Returns
    -------
    text_to_read : list
        Lines from the transcript file.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            text_to_read = f.read()
        if text_to_read != "":
            return(text_to_read)
        else:
            return("No transcript file found.")
    except IOError:
        return("No transcript file found.")

def makeTranscript(file_name):
    """
    Create a format transcript from a transcript file.

    Parameters
    ----------
    file_name : str
        The path to the transcript file.
    Returns
    -------
    second_pass : str
        The HTML-formatted transcript.
    """
    raw_transcript = readTranscript(file_name)

    if raw_transcript == "No transcript file found.":
        return(raw_transcript)

    sep = "\n"

    ## separate the individual lines
    sep_transcript = raw_transcript.split(sep)

    ## For navigation within the list. A bit kludgey.
    curr_loc = 0

    ## Initializing a variable to hold the HTML transcript.
    first_pass = []

    for i in sep_transcript:
        ## Actions are offset by parentheses.
        if i[0:1] == "(":
            escaped = html.escape(i)
            action_list = ["""<p class="action">""",escaped,"</p>"]
            action_string = "".join(action_list)
            first_pass.append(action_string)
        ## Actual dialogues are indented by 2 spaces. They're part of the same line as names.
        elif i[0:2] == "  ":
            line_stripped = html.escape(i[2:])
            line_list = ["""<span class="linedia">""",line_stripped,"</span></p>"]
            line_string = "".join(line_list)
            first_pass.append(line_string)
        ## Blank lines are just there for ease of formatting and can be ignored for the final product.
        elif i == "":
            pass
        ## Anything else is probably a character name.
        else:
            charname_list = ["""<p class="line"><span class="charname">""",html.escape(i),"</span>:"]
            charname_string = "".join(charname_list)
            first_pass.append(charname_string)
        curr_loc += 1

    sep = "\n"
    second_pass = sep.join(first_pass)
    return(second_pass)
