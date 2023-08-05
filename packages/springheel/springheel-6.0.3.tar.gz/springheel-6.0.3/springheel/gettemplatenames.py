#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Get templates
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
## along with this program. If not, see <http://www.gnu.org/

"""Get filenames for site templates."""

import os

def getTemplateNames():
    """Make filenames for site templates."""
    base = "base-template"
    characters = "characters-template"
    archive = "archive-template"
    index = "index-template"
    extra = "extras-template"
    strings = "strings.json"

    patterns=[base,characters,archive,index,extra]

    extension = "html"

    root="templates"

    fulls=[]

    for pattern in patterns:
        file=".".join([pattern,extension])
        full=os.path.join(root,file)
        fulls.append(full)

    ## Get strings.json path and add it too
    strings_p = os.path.join(root,strings)
    fulls.append(strings_p)
    templates=tuple(fulls)

    return(templates)
