#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Metadata Parsing
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

"""Parse metadata files."""

import springheel.parseconf
from slugify import slugify
import html

def readMeta(file_name):
    """
    Retrieve a metadata file.

    Parameters
    ----------
    file_name : str
        The path to the metadata file.
    Returns
    -------
    text_to_read : list
        Lines from the metadata file.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            text_to_read = f.read().splitlines()
    except IOError:
        print("An I/O error has occurred.")
        return(False)
    except UnboundLocalError:
        print("An Unbound Local Error has occurred. I'm probably looking for a page that doesn't exist.")
        return(False)
    return(text_to_read)

def getMetaCom(meta_raw, translated_strings):
    """
    Separate the metadata from formatting info and commentary.

    Parameters
    ----------
    meta_raw : list
        Lines from the metadata file.
    translated_strings : dict
        The translation file contents for this site.
    Returns
    -------
    meta_nl : list
        Metadata lines with key: value pairs.
    comments : list
        HTML-escaped creator commentary lines.
    """
    meta_nl = []
    comments = []
    for i in meta_raw:
        if i == "---\n" or i == "---":
            pass
        else:
            if i[0:2] == "  ":
                meta_nl.append(i.strip())
            else:
                comments.append(html.escape(i))
    if comments == []:
        comments = [translated_strings["no_comment"]]
    return(meta_nl, comments)

def dictizeMeta(m, file_name):
    """
    Convert the plain metadata into a dictionary.

    Parameters
    ----------
    m : list
        A list of lines with colon-separated metadata.
    Returns
    -------
    meta : dict
        The dictionary-fied metadata.
    """
    meta = []
    for i in m:
        s = i.split(": ", 1)
        try:
            d = {s[0]:s[1]}
        except IndexError:
            print("Error: No value set for {s} in {file_name}. Remaining generation may fail.".format(s=s[0], file_name=file_name))
        meta.append(d)
    result = {}
    for d in meta:
        result.update(d)
    meta = result
    return(meta)

def parseMetadata(file_name, translated_strings):
    """
    Short description.

    Parameters
    ----------
    file_name : str
        The path to the metadata file.
    translated_strings : dict
        The translation file contents for this site.
    Returns
    -------
    meta : dict
        A dictionary of strip metadata.
    commentary : str
        Creator commentary formatted as HTML paragraphs.
    slugs : list
        URL-safe slugs for the strip title and category.
    """

    ## Read the metadata from the file.
    meta_raw = readMeta(file_name)
    ## Get the metadata proper and the commentary.
    m, c = getMetaCom(meta_raw, translated_strings)
    ## Convert the metadata list to a dictionary.
    meta = dictizeMeta(m, file_name)

    ## Create slugs.
    series_slug = slugify(meta["category"], lowercase=True, max_length=200)
    title_slug = slugify(meta["title"], lowercase=True, max_length=200)
    slugs = [title_slug, series_slug]

    ## Format commentary lines.
    commentary = []
    for line in c:
        comm = ["<p>",line,"</p>"]
        comm = "".join(comm)
        commentary.append(comm)
    commentary = "".join(commentary)
    return(meta, commentary, slugs)


