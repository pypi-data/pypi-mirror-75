#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Comic Navigation Block Generation
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

"""Generate comic navigation."""

import springheel.parseconf, springheel.parsemeta
from springheel.__init__ import logMsg

class Arrow:
    """
    A navigation element to go to another page.

    Attributes
    ----------
    relation : str
        The relationship between the target page and the current one.
        Will be first, prev, next, or last.
    page : str
        The page number for the target page.
    """
    def __init__(self, relation, page):
        """
        The constructor for the Arrow class.

        Parameters
        ----------
        relation : str
            The relationship between the target page and the current
            one. Will be first, prev, next, or last.
        page : str
            The page number for the target page.
        """
        self.relation = relation
        self.page = page

def navGen(navdirection, zero_padding, scrollto, page_int, first_page, last_page, first, final, series_slug, site_style, translated_strings):
    """
    Generate navigation boxes and link rel navigation.

    Parameters
    ----------
    navdirection : str
        Site reading direction. One of ltr or rtl.
    zero_padding : int
        The number of digits to page numbers are padded.
    scrollto : str
        The anchor to scroll to on the target page. Will likely be
        empty, #comictitle, #topbox, or #comic.
    page_int : int
        The page number represented as an integer.
    first_page : int
        The number of the first page. Will likely be 1.
    last_page : int
        The number of the latest/final page.
    first : bool
        Whether or not the current page is the first one.
    final : bool
        Whether or not the current page is the final one.
    series_slug : str
        URL-safe slug for the comic category.
    site_style : str
        The theme whose arrows will be used.
    translated_strings : dict
        The translation file contents for this site.
    Returns
    -------
    nav : str
        The generated navigation box.
    linkrels : str
        The generated link rel information.
    """
    strips = range(0,(last_page+1))
    if page_int not in strips:
        logmesg = """Building failed! Navigation could not be built because {page_int} is an invalid page number. The .meta value "page" may have been set to something incorrect, or the scan may have failed to detect a comic. Please double-check.""".format(page_int=page_int)
        print(logmesg)
        logMsg(logmesg,".")

    if page_int == last_page:
        final = True
    elif page_int == first_page:
        first = True
    if zero_padding == False:
        first_page = str(first_page)
        last_page = str(last_page)
    else:
        first_page = "{page:0{zero_padding}}".format(page=first_page,zero_padding=zero_padding)
        last_page = "{page:0{zero_padding}}".format(page=last_page,zero_padding=zero_padding)

    first_s = translated_strings["first_s"]
    prev_s = translated_strings["prev_s"]
    next_s = translated_strings["next_s"]
    last_s = translated_strings["last_s"]
    home_s = translated_strings["home_s"]

    firsts_s = translated_strings["firsts_s"]
    prevs_s = translated_strings["prevs_s"]
    nexts_s = translated_strings["nexts_s"]
    lasts_s = translated_strings["lasts_s"]

    navl = [' <ul class="cominavbox">']
    linkl = ['<link rel="alternate" type="application/rss+xml" title="RSS" href="feed.xml">']

    image_template = """<li><a href="{series_slug}_{page}.html{scrollto}"><img src="arrows/{site_style}_{relation}.png" alt="{image_long_string}" /><br/>{image_short_string}</a></li>"""
    linkrel_template = """<link rel="{relation}" href="{series_slug}_{page}.html" title="{page_string}">"""

    navl = ['<ul class="cominavbox" id="{boxlocation}">']
    linkl = ['<link rel="alternate" type="application/rss+xml" title="{rss_s}" href="feed.xml">'.format(rss_s=translated_strings["rss_s"]),
    '<link rel="alternate" type="application/json" title="{jsonfeed_name}" href="feed.json">'.format(jsonfeed_name=translated_strings["jsonfeed_name"])]
    relations = []
    if not first:
        fd = {"rel":"first","page":first_page}
        relations.append(fd)
        if zero_padding == False:
            prev_page = str(page_int-1)
        else:
            prev_page = "{page:0{zero_padding}}".format(page=(page_int-1),zero_padding=zero_padding)
        pd = {"rel":"prev","page":prev_page}
        relations.append(pd)
    if not final:
        if zero_padding == False:
            next_page = str(page_int+1)
        else:
            next_page = "{page:0{zero_padding}}".format(page=(page_int+1),zero_padding=zero_padding)
        nd = {"rel":"next","page":next_page}
        relations.append(nd)
        ld = {"rel":"last","page":last_page}
        relations.append(ld)
    if navdirection == "rtl":
        image_strings = [{"rel":"first","long":last_s,"short":lasts_s}, {"rel":"prev","long":next_s,"short":nexts_s}, {"rel":"next","long":prev_s,"short":prevs_s},
        {"rel":"last","long":first_s,"short":firsts_s},]
    else:
        image_strings = [{"rel":"first","long":first_s,"short":firsts_s}, {"rel":"prev","long":prev_s,"short":prevs_s}, {"rel":"next","long":next_s,"short":nexts_s},
        {"rel":"last","long":last_s,"short":lasts_s},]
    for rel in relations:
        arr = Arrow(relation=rel["rel"], page=rel["page"])
        arr.strings = [item for item in image_strings if item["rel"] == arr.relation][0]
        arr.long = arr.strings["long"]
        arr.short = arr.strings["short"]
        img = image_template.format(series_slug=series_slug,
                                   page=arr.page,
                                   scrollto=scrollto,
                                   site_style=site_style,
                                   relation=arr.relation,
                                   image_long_string=arr.long,
                                   image_short_string=arr.short)
        navl.append(img)
        linkrel = linkrel_template.format(relation=arr.relation,
                                     series_slug=series_slug,
                                     page=arr.page,
                                     page_string=arr.long)
        linkl.append(linkrel)

    navl.append("</ul>")
    nav = """\n""".join(navl)

    linkrels = """\n""".join(linkl)

    return(nav,linkrels)
