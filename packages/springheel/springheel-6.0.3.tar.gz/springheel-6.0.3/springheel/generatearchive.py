#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Comic Archive Page Generation
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

"""Generate links for archive pages."""

import springheel.parseconf, os

def getLinks(i, scrollto, translated_strings):
    """Generate hyperlinks for the archive page.

    Takes a Strip object and links it according to the archive link
    format for the current language from strings.json.

    Parameters
    ----------
    i : Strip
        The Strip whose link is to be formatted.
    scrollto : str
        The anchor to scroll to on the target page. Will likely be
        empty, #comictitle, #topbox, or #comic.
    translated_strings: dict
        The translation file contents for this site.
    Returns
    -------
    archive_link : str
        The formatted link to the page.
    """
    archive_l = translated_strings["archive_l_s"].format(title=i.title,page=i.page)
    link_format = """<li><a href="{html_filename}{scrollto}">{archive_l}</a></li>"""
    archive_link = link_format.format(html_filename=i.html_filename,
                                      scrollto=scrollto,
                                      archive_l=archive_l)
    return(archive_link)

def generateChapArchList(archive, chapter, chapter_title, chapter_slug, translated_strings, l):
    """Generates an ordered list of pages in a chapter."""
    sep = "\n"
    link_list = sep.join(archive)

    chapter_s = translated_strings["chapter_s"].format(chapter=chapter,chapter_title=chapter_title)

    sect = """<h{l} id="{slug}">{chapter_s}</h{l}>
<ol class="chapterarch">
{link_list}
</ol>"""

    arch_list = sect.format(slug=chapter_slug,
                            chapter_s=chapter_s,
                            link_list=link_list,
                            l=l)
    return(arch_list)

def generateSeriesArchives(category,status,archive):
    """Generates an ordered list of pages sorted by date."""
    sep = "\n"
    link_list = sep.join(archive)
    sect = """<section class="archive">
<h2>{category}</h2>
<p class="status">{status}</p>
<ol class="datearch">
{link_list}
</ol>
</section>"""

    arch_section = sect.format(category=category,
                               status=status,
                               link_list=link_list)
    return(arch_section)
