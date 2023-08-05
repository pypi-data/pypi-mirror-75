#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Extra Page Generation
########
##  Copyright 2019 garrick. Some rights reserved.
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

"""Generate extras pages."""

import json, os, shutil

class EXpage:
    """
    An extras page.

    Parameters
    ----------
    headings : list
        The page's navigational headings.
    content : str
        The generated HTML for the extras page.
    """
    def __init__(self):
        """Constructor for the EXpage class."""
        self.headings = []

def gen_extra(i_path, o_path, extras_j, translated_strings):
    """
    Generate an extras page.

    Parameters
    ----------
    i_path : str
        Path to the input folder.
    o_path : str
        Path to the output folder.
    extras_j : str
        Path to the Extra.json file.
    translated_strings : dict
        The translation file contents for this site.
    Returns
    -------
    extras : EXpage
        The completed extras page.
    j : dict
        Raw JSON of the extras page.
    """
    with open(extras_j,"r") as f:
      f_raw = f.read()
    j = json.loads(f_raw)
    extras = EXpage()
    extra_elements = []
    for cat in sorted(j.keys()):
        extras.headings.append(cat)
        subhead = "<h2>{cat}</h2>".format(cat=cat)
        extra_elements.append(subhead)
        for el in j[cat]:
            title = "<h3>{title}</h3>".format(title=el["title"])
            if el["type"] == "image":
                images = []
                for image in el["files"]:
                    images.append('<img src="{image}" alt="{title}" />'.format(title=el["title"], image=image))
                    shutil.copy(os.path.join(i_path,image),os.path.join(o_path,image))
                images = "".join(images)
                el_template = """<figure>{images}<figcaption>{image_s}{desc}</figcaption></figure>""".format(images=images, image_s=translated_strings["image_s"], desc=el["desc"])
            else:
                fils = []
                for fil in el["files"]:
                    fils.append("""<li><a href="{path}">{link}</a></li>""".format(path=fil["path"],link=fil["link"]))
                    shutil.copy(os.path.join(i_path,fil["path"]),os.path.join(o_path,fil["path"]))
                fils = "".join(fils)
                el_template = "<p>{desc}</p><ul>{fils}</ul>".format(desc=el["desc"],fils=fils)
            elem = "\n".join([title,el_template])
            extra_elements.append(elem)
    extra_combined = "\n".join(extra_elements)
    extras.content = extra_combined
    return(extras,j)
