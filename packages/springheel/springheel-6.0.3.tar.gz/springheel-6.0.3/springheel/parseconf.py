#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Configuration Parser
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

"""Parse configuration files."""

import configparser, os

def comicCParse(conf):
    """
    Parse a configuration file.

    Parameters
    ----------
    conf : str
        The path to the configuration file.
    Returns
    -------
    comic_config : dict
        The comic's configuration file formatted as a dictionary.
    """
    cc = configparser.ConfigParser()
    cc.read(conf,encoding="utf-8")
    cc.sections()

    category = cc.get("ComicConfig","category")
    author = cc.get("ComicConfig","author")
    email = cc.get("ComicConfig","email")
    header = cc.get("ComicConfig","header")
    banner = cc.get("ComicConfig","banner")
    language = cc.get("ComicConfig","language")
    mode = cc.get("ComicConfig","mode")
    status = cc.get("ComicConfig","status")
    chapters = cc.get("ComicConfig","chapters")
    desc = cc.get("ComicConfig","desc")
    chars = cc.get("ComicConfig","chars")
    clicense = cc.get("ComicConfig","license")

    comic_config = {"category":category, "author":author,
                    "email":email, "header":header, "banner":banner,
                    "language":language, "mode":mode, "status":status,
                    "chapters":chapters, "desc":desc,"license":clicense,
                    "chars":chars}
    try:
        clicense_uri = cc.get("ComicConfig","license_uri")
        comic_config["license_uri"] = clicense_uri
    except configparser.NoOptionError:
        pass
    try:
        category_theme = cc.get("ComicConfig","category_theme")
        comic_config["category_theme"] = category_theme
    except configparser.NoOptionError:
        pass
    return(comic_config)
