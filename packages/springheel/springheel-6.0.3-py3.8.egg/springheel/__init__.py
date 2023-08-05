#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##  Copyright 2017-2020 garrick. Some rights reserved.
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.

##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Springheel -- a static site generator for webcomics."""

name = "springheel"
author = "gargargarrick"
__version__ = '6.0.3'

import springheel.genchars
import springheel.generatearchive
import springheel.generatenav
import springheel.genmultipleindex
import springheel.gentrans
import springheel.genrss
import springheel.gentopnav
import springheel.gettemplatenames
import springheel.parsemeta
import springheel.parsetranscript
import springheel.springheelinit
import springheel.genextra
import springheel.socialbuttons
import springheel.genmultilang
import springheel.genjsonfeed

import shutil
import configparser, os, datetime, sys
from operator import itemgetter
from slugify import slugify
import html, json
from tqdm import tqdm

class Site:
    """
    A Springheel comic site.

    Attributes
    ----------
    comics : list
        A List of comic series/categories.
    sitemap : list
        Dicts of HTML filenames and last-modified times for all pages.
    jsonpoints : dict
        Information about the site in JSON format.
    config : Config
        Sitewide configuration settings.
    license : str
        The license of the overall site.
    copyright_statement : str
        A copyright statement for the site.
    """
    def __init__(self):
        """The constructor for the Site class."""
        self.comics = []
        self.sitemap = []

class Config(object):
    """A ConfigParser object for site preferences."""
    def __init__(self,*file_names):
        """
        The constructor for the Config class.

        Parameters
        ----------
        file_names : str
            (opt.) Filename of the configuration file.
        """
        parser = configparser.ConfigParser()
        parser.optionxform = str
        found = parser.read(file_names,encoding="utf-8")
        if not found:
            raise ValueError("No cfg file")
        for name in ["Config"]:
            self.__dict__.update(parser.items(name))
class Tag:
    """
    A tag that classifies comic strips.

    Attributes
    ----------
    name : str
        The name of the tag.
    escaped : str
        An HTML-safe version of name (no &, <, or >).
    slug : str
        name slugified for URLs.
    strips : list
        Strips to which the tag applies.
    rurl : str
        HTML filename for the tag.
    link : str
        Hyperlink to the tag index URL.
    """
    def __init__(self,name):
        """
        The constructor for Tag.

        Parameters
        ----------
        name : str
            The name of the tag.
        """
        self.name = name
        self.escaped = html.escape(name)
        self.slug = slugify_url(name)
        self.strips = []
class Strip:
    """
    An individual comic page.

    Attributes
    ----------
    imagef : str
        Filename of the strip image.
    metaf : str
        Filename of the strip's metadata file.
    transf : str
        Filename of the strip's transcript file.
    tags : list
        (opt.) A list of Tags used by the strip.
    metadata : dict
        The strip's metadata.
    commentary : str
        The strip's creator commentary.
    slugs : list
        Title and series slugs.
    title_slug : str
        URL-safe slug for the strip's title.
    series_slug : str
        URL-safe slug for the strip's category.
    category : str
        The strip's category.
    page : str
        The strip's page number (directly from the meta file).
    page_int : int
        The strip's page number converted to an integer.
    transcript_c : str
        Contents of the strip's transcript file.
    conf_c : str
        Contents of the strip's config file.
    author : str
        The strip's author.
    author_email : str
        The strip's author's email address (for RSS feeds).
    mode : str
        Debug parameter that currently does nothing.
    height : str
        The height of the strip image in pixels.
    width : str
        The width of the strip image in pixels.
    date : datetime.datetime
        The upload date of the strip.
    date_s : str
        date formatted according to ISO 8601 (YYYY-MM-dd).
    year : int
        The year in which the strip was published.
    license : str
        The copyright status of the strip.
    title : str
        The title of the strip.
    img : str
        The path to the strip image.
    alt_text : str
        (opt.) Extra text that displays below the strip. Despite the
        name, is not really used as alt text. A more accessible
        version of the title text some comics have.
    chapter : int/bool
        The chapter number if a strip is part of a chapter. False if
        it is not.
    h1_title : str
        The title used as a top-level heading for the strip.
    header_title : str
        The string used as an HTML <title> element.
    copyright_statement : str
        The copyright information used in the footer of the page.
    archive_link : str
        The text that will link to the strip on the Archives page.
    """
    def __init__(self,imagef,metaf,transf):
        """
        The constructor for Strip.

        Parameters
        ----------
        imagef : str
            Filename of the strip image.
        metaf : str
            Filename of the strip's metadata file.
        transf : str
            Filename of the strip's transcript file.
        """
        self.imagef = imagef
        self.metaf = metaf
        self.transf = transf
        self.tags = []
class Comic:
    """
    A comic series or story.

    Attributes
    ----------
    category : str
        The name of the comic.
    category_escaped : str
        HTML-safe category (no &, <, or >).
    last_page : int
        The latest page of the comic.
    first_page : int
        The first page of the comic.
    author : str
        The comic's creator.
    email : str
        The comic creator's email address, for RSS feeds.
    header : str
        Filename for the page header of the comic.
    banner : str
        The comic's banner that appears on the index page.
    language : str
        The comic's language.
    mode : str
        Debug parameter that currently does nothing.
    status : str
        Whether the comic is still updating or not.
    chapters : bool
        True if the comic is chaptered, False if not.
    chapters_file : str
        (opt.) If chapters is True, path to the chapter file.
    desc : str
        A description of the comic for the index.
    category_theme : str
        (opt.) Theme used by the comic.
    chars_file : str
        (opt.) Filename of the character file.
    chapters_dicts : list
        (opt.) Dicts with chapter numbers and titles.
    chapters_list : list
        (opt.) List of Chapters in the comic.
    slug : str
        category slugified for URLs.
    statuss : str
        status but wrapped in <strong> tags.
    license : str
        The comic's license.
    copyright_statement : str
        A copyright statement for the comic.
    pbp : list
        all Strips in the comic, sorted by page number.
    pbd : list
        all Strips in the comic, sorted by date.
    fbp_link : list
        HTML filename of the first strip by page number.
    lbp_link : list
        HTML filename of the last strip by page number.
    fbd_link : list
        HTML filename of the first strip by date.
    lbd_link : list
        HTML filename of the last strip by date.
    """
    def __init__(self, category):
        """
        The constructor for the Comic class.

        Parameters
        ----------
        category : str
            The name of the comic.
        """
        self.category = category
        self.category_escaped = html.escape(category)
    class Chapter:
        """
        A set of related Strips.

        Attributes
        ----------
        chap_number : int
            The number of the chapter.
        chap_title : str
            The title of the chapter.
        chap_title_escaped : str
            HTML-safe chap_title (no &, <, or >).
        pages : list
            All Strips in the chapter.
        """
        def __init__(self,chap_number,chap_title):
            """
            Constructor for the Chapter class.

            Parameters
            ----------
            chap_number : int
                The number of the chapter.
            chap_title : str
                The title of the chapter.
            """
            self.chap_number = chap_number
            self.chap_title = chap_title
            self.chap_title_escaped = html.escape(chap_title)
            self.pages = []
    class Archives:
        """
        A list of links to Strips, which may or may not be divided into
        Chapters.

        Attributes
        ----------
        category : str
            The number of the chapter.
        chap_title : str
            The title of the chapter.
        chap_title_escaped : str
            HTML-safe chap_title (no &, <, or >).
        pages : list
            All Strips in the chapter.
        """

        def __init__(self, arg):
            """Constructor for the Archives class."""
            super(Archives, self).__init__()
            self.arg = arg


def logMsg(message,path):
    """Save info about the generation process to a file."""
    logfile = os.path.join(path, "springheel.log")
    now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
    message = "".join(["\n", now, " -- ", message])
    with open(logfile,"a+",encoding="utf-8") as lf:
        lf.write(message)

def wrapImage(link,title,image):
    """Enclose an image in a hyperlink."""
    line = """<a href="{link}"><img src="socialbuttons/{image}" alt="{title}" /></a>""".format(link=link,image=image,title=title)
    return(line)

def copyTheme(site_theme_path,new_site_theme_path):
    """Copy theme assets to the output folder."""
    files = os.listdir(site_theme_path)

    for i in files:
        source_path = os.path.join(site_theme_path, i)
        new_path = os.path.join(new_site_theme_path, i)
        if os.path.exists(new_path) == False:
            try:
                shutil.copy(source_path,new_site_theme_path)
            except IsADirectoryError:
                pass
        else:
            logmesg = "{i} already exists in the output. To overwrite, remove the existing file from output.".format(i=i)
            logMsg(logmesg, ".")

    logmesg = "Copied assets to {new_site_theme_path}".format(new_site_theme_path=new_site_theme_path)
    logMsg(logmesg,".")

def copyButtons(site, old_buttons_path, socialbuttons_path, translated_strings):
    """Copy buttons to the output folder."""
    files = os.listdir(old_buttons_path)

    logmesg = "Social icons: {icons}".format(icons=site.config.social_icons)
    logMsg(logmesg,".")
    social_links = socialbuttons.getButtons(site, translated_strings)[0]

    for item in files:
        for d in social_links:
            if item == d["image"]:
                source_path = os.path.join(old_buttons_path, item)
                shutil.copy(source_path,socialbuttons_path)
            elif item == "rss.png":
                source_path = os.path.join(old_buttons_path, item)
                shutil.copy(source_path,socialbuttons_path)

    if site.config.social_icons == "True":
        logmesg = "Copied social buttons to {socialbuttons_path}".format(socialbuttons_path=socialbuttons_path)
    else:
        logmesg = "Copied RSS feed button to {socialbuttons_path}".format(socialbuttons_path=socialbuttons_path)
    logMsg(logmesg,".")

def copyArrows(site,old_arrows_path,new_arrows_path):
    """Copy navigation arrows to the output folder."""
    theme = site.config.site_style
    arrtemplate = "{theme}_{dir}.png"
    needed_dirs = ["first", "prev", "next", "last"]
    needed_arrows = [arrtemplate.format(theme=theme, dir=item) for item in needed_dirs]

    for arrow in needed_arrows:
        old_arrow_path = os.path.join(old_arrows_path, arrow)
        new_arrow_path = os.path.join(new_arrows_path, arrow)
        if os.path.exists(old_arrow_path):
            if not os.path.exists(new_arrow_path):
                shutil.copy(old_arrow_path, new_arrows_path)
                logmesg = "{arrow} copied.".format(arrow=arrow)
                logMsg(logmesg,".")
        else:
            logmesg = "{old_arrow_path} not found in the currently-set style {theme}.".format(old_arrow_path=old_arrow_path, theme=theme)
            logMsg(logmesg,".")
            return(False)

    return()

def copyHeader(old_header_path,new_header_path):
    """Copy the site header image to the output folder."""
    shutil.copy(old_header_path,new_header_path)
    logmesg = "Site header copied."
    logMsg(logmesg,".")

def copyBanner(old_banner_path,new_banner_path,banner):
    """Copy an index banner to the output folder."""
    shutil.copy(old_banner_path,new_banner_path)
    logmesg = "Banner {banner} copied.".format(banner=banner)
    logMsg(logmesg,".")

def copyMultiThemes(themes,c_path,o_path,assets_path):
    """Concatenate themes into one stylesheet in the output folder."""
    theme_path = os.path.join(c_path, "themes")
    new_theme_path = os.path.join(o_path, assets_path)
    theme_ds = []

    for theme in themes:
        t_path = os.path.join(c_path, "themes", theme)
        files = os.listdir(t_path)
        sheet = os.path.join(t_path, "style.css")
        with open(sheet,"r",encoding="utf-8") as f:
            sheet_contents = f.read()

        theme_ds.append({"theme":theme,"o_path":t_path,"files":files,"sheet":sheet,"sheet_contents":sheet_contents})

    style = []
    knownfiles = []

    for d in theme_ds:
        sc = d["sheet_contents"]
        style.append(sc)
        for i in d["files"]:
            source_dir = d["o_path"]
            source_path = os.path.join(source_dir, i)
            new_path = os.path.join(new_theme_path, i)
            if os.path.exists(new_path) == False and i not in knownfiles:
                try:
                    shutil.copy(source_path,new_theme_path)
                except IsADirectoryError:
                    pass
                knownfiles.append(i)
                logmesg = "{source_path} copied to {new_theme_path}".format(source_path=source_path,new_theme_path=new_theme_path)
                logMsg(logmesg,".")
            else:
                if i not in knownfiles:
                    logmesg = "{i} already exists in the output. To overwrite, remove the existing file from output.".format(i=i)
                    logMsg(logmesg, ".")
                    knownfiles.append(i)

    cstyle = "".join(style)
    new_style_path = os.path.join(new_theme_path, "style.css")
    with open(new_style_path,"w+") as fout:
        fout.write(cstyle)
    logmesg = "Concatenated stylesheet written."
    logMsg(logmesg,".")

    return()

def copyMultiArrows(themes,c_path,o_path,assets_path):
    """Copy multiple themes' navigation arrows to the output folder."""
    for theme in themes:
        arrtemplate = "{theme}_{dir}.png"
        needed_dirs = ["first", "prev", "next", "last"]
        needed_arrows = [arrtemplate.format(theme=theme, dir=item) for item in needed_dirs]

        old_arrows_path = os.path.join(c_path, "arrows")
        new_arrows_path = os.path.join(o_path, "arrows")

        for arrow in needed_arrows:
            old_arrow_path = os.path.join(old_arrows_path, arrow)
            new_arrow_path = os.path.join(new_arrows_path, arrow)
            if os.path.exists(old_arrow_path):
                if not os.path.exists(new_arrow_path):
                    shutil.copy(old_arrow_path, new_arrows_path)
                    logmesg = "{arrow} copied.".format(arrow=arrow)
                    logMsg(logmesg,".")
            else:
                logmesg = "{old_arrow_path} not found in the currently-set style {theme}.".format(old_arrow_path=old_arrow_path, theme=theme)
                logMsg(logmesg,".")
                return(False)

    return()

def getTags(meta,all_tags):
    """Process a strip's tags.

    Retrieve a strip's used tags, add new ones to the list of all
    known tags, and create a line that indicates the strip's tags with
    hyperlinks to those tags' indices.
    """
    tags_raw = meta["tags"]
    tags_sep = tags_raw.split(", ")
    this_strips_tags = []
    this_strips_wraps = []
    for tag in tags_sep:
        tago = Tag(name=tag)
        tago.rurl = "tag-{tag_slug}.html".format(tag_slug=tago.slug)
        wrapped = """<a href="tag-{tag_slug}.html">{tag}</a>""".format(tag_slug=tago.slug,tag=tago.escaped)
        tago.link = wrapped
        if tag not in (n.name for n in all_tags):
            all_tags.append(tago)
        this_strips_tags.append(tago)
        this_strips_wraps.append(wrapped)
    tagline = ", ".join(this_strips_wraps)
    return(tagline,this_strips_tags)

def getComics():
    """Find comic strips in the input folder."""

    original_path = os.getcwd()

    path = os.path.join(original_path, "input")
    os.chdir(path)

    files = os.listdir()

    ## Get a list of images that have the proper meta files.

    images = []
    image_extensions = [".png", ".gif", ".jpg", ".jpeg", ".svg", ".webp"]

    for i in files:
        ext = os.path.splitext(i)[1]
        if ext in image_extensions:
            images.append(i)

    comics = []
    logmesg = "Finding images..."
    print(logmesg)
    logMsg(logmesg, original_path)
    for i in tqdm(images):
        noext = os.path.splitext(i)[0]
        transcr = noext+".transcript"
        meta = noext+".meta"
        if transcr in files and meta in files:
            logmesg = "Metadata and transcript found for {image}.".format(image=i)
            logMsg(logmesg,original_path)
            comic = Strip(imagef=i,transf=transcr,metaf=meta)
            comics.append(comic)
        elif meta in files and transcr not in files:
            logmesg = "Metadata found, but no transcript for {image}. Please create {transcr}".format(image=i,transcr=transcr)
            logMsg(logmesg,original_path)
            comic = Strip(imagef=i,transf="no_transcript.transcript",metaf=meta)
            comics.append(comic)
        elif transcr in files and meta not in files:
            logmesg = "Transcript found, but no metadata for {image}. I can't build the page without metadata. Please create {meta}".format(image=i,meta=meta)
            logMsg(logmesg,original_path)
            return(False)
        else:
            logmesg = "{image} doesn't seem to be a comic, as it is missing a transcript and metadata.".format(image=i)
            logMsg(logmesg,original_path)

    if comics == []:
        logmesg = "The comics list is empty. Please add some comics and then try to build again."
        logMsg(logmesg,".")
        return(False)

    os.chdir(original_path)

    return(comics)

def getChapters(chapter_file):
    """Get numbers and titles from a chapter file."""
    with open(chapter_file,"r",encoding="utf-8") as f:
        chapter_raws = f.readlines()
    chapters = []
    for line in chapter_raws:
        if line != "":
            split_line = line.split(" = ",1)
            d = {"num":int(split_line[0]), "title":split_line[1]}
            chapters.append(d)
    return(chapters)

def wrapWithTag(s,tag):
    """Wrap a string in an HTML tag."""
    wrapped = "<{tag}>{s}</{tag}>".format(tag=tag,s=s)
    return(wrapped)

def wrapWithComment(s,comment):
    """Wrap a string in an HTML comment."""
    wrapped = "<!--{comment}-->{s}<!--END {comment}-->".format(comment=comment, s=s)
    return(wrapped)

def checkExtremes(l):
    """Find the highest and lowest values in a list of integers."""
    highest = max(l)
    lowest = min(l)
    return(highest,lowest)

def makeFilename(series_slug,page):
    """Combine a series slug and page number into an HTML filename."""
    ##pattern: series_slug_page.html
    file_name_components = [series_slug,page]
    file_name = str("_".join(file_name_components)+".html")
    return(file_name)

def slugify_url(txt):
    slugified = slugify(txt, lowercase=True, max_length=200)
    return(slugified)

def build():
    """Generate a Springheel site."""
    site = Site()
    sep = "\n"
    falses = [False,"False"]
    config = Config("conf.ini")
    site.config = config
    image_rename_pattern = site.config.image_rename_pattern
    starttime = datetime.datetime.now().timestamp()
    site.jsonpoints = {"generated_on": starttime, **config.__dict__,
                   "archive_page": "".join([site.config.base_url, "archive.html"]), "categories": []}

    ## Initialize log to avoid confusion
    logfile = os.path.join(".", "springheel.log")
    with open(logfile,"w+") as lf:
        lf.write("== Springheel Build Log ==")
    c_path, o_path, pages_path, assets_path, arrows_path, socialbuttons_path = springheelinit.makeOutput()
    i_path = os.path.join(c_path, "input")

    try:
        zero_padding = site.config.zero_padding
    except AttributeError:
        zero_padding = "False"
        logmesg = "There is no config value for zero_padding. Please update your conf.ini."
        logMsg(logmesg,".")
    if zero_padding == "False":
        zero_padding = False
    else:
        zero_padding = int(zero_padding)
    try:
        scrollto = site.config.scrollto
        if scrollto == "False":
            scrollto = ""
    except AttributeError:
        scrollto = ""
        logmesg = "There is no config value for scrollto. Please update your conf.ini."
        logMsg(logmesg,".")
    if scrollto != "":
        scrollto = "#"+scrollto
    try:
        multilang = site.config.multilang
    except AttributeError:
        multilang = False

    ## Get some config variables

    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheel.springheelinit.makeOutput()

    site_theme_path = os.path.join(c_path, "themes", site.config.site_style)
    new_site_theme_path = os.path.join(o_path, assets_path)

    old_buttons_path = os.path.join(c_path, "socialbuttons")

    old_arrows_path = os.path.join(c_path, "arrows")
    new_arrows_path = os.path.join(o_path, "arrows")

    old_header_path = os.path.join(c_path, "input", site.config.banner_filename)
    new_header_path = os.path.join(o_path, site.config.banner_filename)

    html_filenames = []
    ## Get a list of dictionaries that map image files to metadata
    comics_base = getComics()

    ## Get template paths
    base_t,chars_t,archive_t,index_t,extra_t,strings_path = gettemplatenames.getTemplateNames()

    ## Select the right template for the specific site type we have
    all_page_ints = []
    if site.config.site_type == "single":
        single = True
    else:
        single = False

    if single == True:
        index_t = index_t+".single"
        archive_t = archive_t+".single"
    else:
        index_t = index_t+".multi"
        archive_t = archive_t+".multi"

    ## Get translation strings, too.
    translated_strings = gentrans.generateTranslations(site.config.language, strings_path)
    language_names = translated_strings["language_names"]
    logmesg = "Loading translation strings for {lang}...".format(lang=site.config.language)
    logMsg(logmesg, ".")

    ## Copy assets from the Springheel installation directory.

    copyTheme(site_theme_path, new_site_theme_path)
    copyButtons(site, old_buttons_path, socialbuttons_path, translated_strings)
    copyArrows(site, old_arrows_path, new_arrows_path)
    copyHeader(old_header_path, new_header_path)

    #### Get basic info first.
    for i in comics_base:
        file_name = os.path.join(i_path, i.metaf)
        meta, commentary, slugs = parsemeta.parseMetadata(file_name, translated_strings)
        ## Page number
        page = meta["page"]
        page_int = int(page)
        i.metadata = meta
        i.commentary = commentary
        i.slugs = slugs
        i.title_slug = slugs[0]
        i.series_slug = slugs[1]
        i.category = i.metadata["category"]
        i.page = page
        i.page_int = page_int
        all_page_ints.append(page_int)

    if single == True:
        last_page,first_page = checkExtremes(all_page_ints)
        cat = comics_base[0].category
        cats_raw = [cat]
        cats_w_pages = [{'category':cat, 'first_page': first_page, 'last_page': last_page}]
    else:
        cats_raw = []
        cats_w_pages = []
        for i in comics_base:
            if i.category not in cats_raw:
                cat = i.category
                cats_raw.append(cat)
        for cat in cats_raw:
            cat_pages = []
            for page in comics_base:
                if page.category == cat:
                    cat_pages.append(page.page_int)
            last_page,first_page = checkExtremes(cat_pages)
            cat_w_pages = {"category":cat,"last_page":last_page,
                           "first_page":first_page}
            cats_w_pages.append(cat_w_pages)

    comics = []
    configs = []
    ccomics = []

    for cat in cats_w_pages:
        c = Comic(cat["category"])
        c.last_page = cat["last_page"]
        c.first_page = cat["first_page"]
        ccomics.append(c)
        if not [item for item in site.jsonpoints["categories"] if item["category"] == cat["category"]]:
            site.jsonpoints["categories"].append(cat)

    ## Get other pages.
    characters_page = site.config.characters_page
    extras_page = site.config.extras_page
    store_page = site.config.store_page

    if characters_page == "True":
        characters_page = True
    else:
        characters_page = False
    site.jsonpoints["characters_page"] = characters_page

    if extras_page == "True":
        extras_page = True
    else:
        extras_page = False
    site.jsonpoints["extras_page"] = extras_page

    if store_page == "False":
        store_page = False
    site.jsonpoints["store_page"] = store_page

    ## why did I already use "top_nav" smh
    site_nav_raw = gentopnav.genTopNav(characters_page,
                                       extras_page,
                                       store_page,
                                       translated_strings)
    top_site_nav = sep.join(site_nav_raw)

    cpages = []
    themes = [site.config.site_style]
    chapters_list = []
    all_tags = []
    years = []

    logmesg = "Processing comic pages..."
    print(logmesg)
    logMsg(logmesg, ".")
    for i in tqdm(comics_base):
        file_name = i.imagef
        meta = i.metadata
        commentary = i.commentary
        slugs = i.slugs

        transcript_file = os.path.join(
            i_path,
            i.transf)
        transcript = parsetranscript.makeTranscript(
            transcript_file)
        if transcript == "No transcript file found.":
            no_trans_p = wrapWithTag(translated_strings["no_transcript"],"p")
            transcript = no_trans_p
        conf_file = os.path.join(
            i_path,
            meta["conf"])
        conf = springheel.parseconf.comicCParse(conf_file)

        i.transcript_c = transcript
        i.conf_c = conf
        category = conf["category"]

        try:
            category_theme = conf["category_theme"]
            themes.append(category_theme)
        except KeyError:
            category_theme = False

        match = [item for item in ccomics if item.category == category][0]

        if conf not in configs:
            configs.append(conf)
            match.author = conf["author"]
            match.email = conf["email"]
            match.header = conf["header"]
            match.banner = conf["banner"]
            match.language = conf["language"]
            match.mode = conf["mode"]
            match.status = conf["status"]
            match.chapters = conf["chapters"]
            if match.chapters not in falses:
                match.chapters = True
                match.chapters_file = os.path.join(i_path, conf["chapters"])
            else:
                match.chapters = False
            match.desc = html.escape(conf["desc"])
            if category_theme:
                match.category_theme = category_theme
        else:
            logmesg = "{category} config already found...".format(category=category)
            logMsg(logmesg,".")

        old_banner_path = os.path.join(c_path, "input", match.banner)
        new_banner_path = os.path.join(o_path, match.banner)
        if os.path.exists(new_banner_path) == False:
            copyBanner(old_banner_path,new_banner_path, match.banner)

        lang = conf["language"]
        page = i.page
        page_int = i.page_int

        author=html.escape(conf["author"])
        author_email=conf["email"]
        mode = conf["mode"]
        banner = conf["banner"]
        header = conf["header"]
        if characters_page == True:
            chars_file = conf["chars"]
            match.chars_file = chars_file
        else:
            match.chars_file = None

        if match.chapters not in falses:
            site.jsonpoints.setdefault("chapter_info", [])
            chapters_dicts = getChapters(match.chapters_file)
            match.chapters_dicts = chapters_dicts
            if match.chapters_dicts not in site.jsonpoints["chapter_info"]:
                site.jsonpoints["chapter_info"].append(match.chapters_dicts)
            if hasattr(match,"chapters_list") == False:
                match.chapters_list = []
            for chapter in chapters_dicts:
                ## Check if chapter exists already
                chap_check = [item for item in match.chapters_list if item.chap_number == chapter["num"]]
                if len(chap_check) == 0:
                    chap = match.Chapter(chapter["num"],chapter["title"])
                    match.chapters_list.append(chap)
        else:
            logMsg("{match} has a chapter setting of {chapter}.".format(match=match.category,chapter=match.chapters), ".")
            match.chapters_list = []

        title = html.escape(meta["title"])
        series_slug = i.series_slug
        title_slug = i.title_slug
        match.slug = series_slug
        date = datetime.datetime.strptime(meta["date"],"%Y-%m-%d")
        year = date.year
        if year not in years:
            years.append(year)
        if "height" in meta.keys():
            height = meta["height"]
        if "width" in meta.keys():
            width = meta["width"]
        if "alt" in meta.keys():
            alt_text = html.escape(meta["alt"])
        else:
            alt_text = False

        ## Make hte license
        clicense = conf["license"]

        if hasattr(site, "license") == False :
            ### Init publicdomain
            publicdomain = False
            if conf["license_uri"]:
                license_uri = conf["license_uri"]
                if clicense.lower() == "public domain" or "publicdomain" in license_uri:
                    publicdomain = True
                    ## Creative Commons Public Domain Waiver
                    ccpdw = translated_strings["ccpdw"]
                    site_license_s = ccpdw.format(
                        site_url=site.config.base_url,
                        author=author,
                        site_title=site.config.site_title,
                        author_country=site.config.country)
                elif "creativecommons.org/licenses/by" in license_uri:
                    cc = translated_strings["cc"]
                    site_license_s = cc.format(
                        license_uri=license_uri,
                        clicense=clicense,
                        author=author,
                        category=site.config.site_title,
                        base_url=site.config.base_url)
            else:
                site_license_s = clicense
            site.license = site_license_s
        if hasattr(match, "license") == False:
            ### Init publicdomain
            publicdomain = False
            if conf["license_uri"]:
                license_uri = conf["license_uri"]
                if clicense.lower() == "public domain" or "publicdomain" in license_uri:
                    publicdomain = True
                    ## Creative Commons Public Domain Waiver
                    ccpdw = translated_strings["ccpdw"]
                    license_s = ccpdw.format(
                        site_url=site.config.base_url,
                        author=i.author,
                        site_title=i.category,
                        author_country=site.config.country)
                elif "creativecommons.org/licenses/by" in license_uri:
                    cc = translated_strings["cc"]
                    license_s = cc.format(
                        license_uri=license_uri,
                        clicense=clicense,
                        author=author,
                        category=i.category,
                        base_url=site.config.base_url)
            else:
                license_s = clicense
            match.license = license_s
        else:
            license_s = match.license
        i.license = license_s

        if publicdomain == False:
            i.copyright_statement = "<p>&copy; {year} {author}. {clicense}</p>".format(
                year=year,
                author=author,
                clicense=i.license)
        else:
            i.copyright_statement = wrapWithTag(
                license_s,
                "p")

        img_path=i.imagef
        if "chapter" in meta.keys():
            chapter = meta["chapter"]
        else:
            chapter = False

        if single == False:
            matching_cat = [item for item in cats_w_pages if item["category"] == meta["category"]][0]
            last_page = matching_cat["last_page"]
            first_page = matching_cat["first_page"]

        if page_int == last_page:
            final = True
        else:
            final = False
        if page_int == first_page:
            first = True
        else:
            first = False

        i.author = author
        i.author_email=author_email
        i.mode = mode
        i.page_int = int(page)
        if height:
            i.height = height
        if width:
            i.width = width

        i.series_slug = series_slug
        i.date = date
        i.date_s = datetime.datetime.strftime(date,"%Y-%m-%d")
        i.year = year
        i.title = title
        if chapter != "False":
            i.chapter = chapter
        else:
            i.chapter = False
        if alt_text == False:
            atitle = i.title
            if i.chapter:
                chap_check = [item for item in match.chapters_list if item.chap_number == int(i.chapter)][0]
                chapter_title = chap_check.chap_title_escaped.strip()
                alt_formatted = translated_strings["alt_chapter_s"].format(category=i.category, chapter=i.chapter, chapter_title=chapter_title, page=i.page, title=i.title)
            else:
                alt_formatted = translated_strings["alt_nochapter_s"].format(category=i.category, page=i.page, title=i.title)
            alt_text = alt_formatted
            i.alt_text = alt_text
        else:
            i.alt_text = alt_text

        if category_theme:
            navblock,linkrels = generatenav.navGen(
                site.config.navdirection,
                zero_padding,
                scrollto,
                page_int,
                first_page,
                last_page,
                first,
                final,
                series_slug,
                category_theme,
                translated_strings)
        else:
            navblock,linkrels = generatenav.navGen(
                site.config.navdirection,
                zero_padding,
                scrollto,
                page_int,
                first_page,
                last_page,
                first,
                final,
                series_slug,
                site.config.site_style,
                translated_strings)

        top_nav = wrapWithComment(navblock.format(boxlocation="topbox"),"TOP NAVIGATION")
        bottom_nav = wrapWithComment(navblock.format(boxlocation="botbox"),"BOTTOM NAVIGATION")

        h1_title = translated_strings["h1_s"].format(category=html.escape(meta["category"]),  page=meta["page"], title=html.escape(meta["title"]))
        header_title = h1_title
        i.h1_title = h1_title
        i.header_title = header_title

        stat_s = translated_strings["statline_s"].format(author=meta["author"],
            date=meta["date"])

        stat_line = """<p class="statline">{stat_s}""".format(stat_s=stat_s)

        tags_in_keys = "tags" in meta.keys()
        if tags_in_keys == True and meta["tags"] != "":
            tagsline,these_tags = getTags(meta,all_tags)
            i.tags = these_tags
            for tag in i.tags:
                tag_match = [item for item in all_tags if item.name == tag.name][0]
                tag_match.strips.append(i)
                tag_match.strips.sort(key=lambda x: (x.category, x.page_int))
            tline = " &mdash; {tags_s}: {tags} &mdash; ".format(
               tags_s=translated_strings["tags_s"],
               tags=tagsline)
            stat_line = stat_line+tline
        site.jsonpoints.setdefault("tags",[])
        for tag in all_tags:
            if not [item for item in site.jsonpoints["tags"] if item["name"] == tag.name]:
                site.jsonpoints["tags"].append({"name":tag.name,"url":"".join([site.config.base_url, tag.rurl])})

        transcript_block = ['<div role="region" id="transcript" aria-label="Transcript"><h2>{transcript_s}</h2>'.format(transcript_s =
            translated_strings["transcript_s"])]

        transcript_block.append(transcript)
        transcript_block.append("</div>")

        tb = "\n".join(transcript_block)

        statuses = [translated_strings["inprogress_s"], translated_strings["complete_s"], translated_strings["hiatus_s"], "Status Not Found - Please add one of 'in-progress', 'complete', or 'hiatus' to this comic's .conf file!"]

        if match.status == "in-progress":
            status = statuses[0]
        elif match.status == "complete":
            status = statuses[1]
        elif match.status == "hiatus":
            status = statuses[2]
        else:
            status = statuses[3]

        match.statuss = wrapWithTag(status, "strong")

        ###########################################################################
        # Generate the actual page!
        ###########################################################################

        if zero_padding != False:
            page_padded = "{page:0{zero_padding}}".format(page=page_int,zero_padding=zero_padding)
            next_page = "{page:0{zero_padding}}".format(page=(page_int+1),zero_padding=zero_padding)
        else:
            page_padded = page
            next_page=str(page_int+1)

        html_filename = makeFilename(
            series_slug,
            page_padded)
        html_filenames.append(html_filename)
        out_file = os.path.join(
            o_path,
            html_filename)

        jsoncat = [item for item in site.jsonpoints["categories"] if item["category"] == category][0]
        strips = jsoncat.setdefault("strips",[])
        dictified_strip = {**i.__dict__}
        page_url = "".join([site.config.base_url, html_filename])
        dictified_strip["url"] = page_url
        ## Get rid of the dict elements we don't need
        del dictified_strip["page_int"]
        del dictified_strip["conf_c"]
        del dictified_strip["metadata"]
        dictified_strip["date"] = dictified_strip["date_s"]
        del dictified_strip["date_s"]
        dictified_strip["year"] = str(dictified_strip["year"])
        if hasattr(i,"tags"):
            dictified_strip["tags"] = []
            for tag in i.tags:
                dictified_strip["tags"].append(tag.name)

        template_name = base_t
        template = os.path.join(
            c_path,
            template_name)

        with open(template) as f:
            base_template = f.read()

        statline = stat_line
        icons = "".join(socialbuttons.getButtons(site, translated_strings)[1])
        if multilang is not False:
            other_langs = springheel.genmultilang.genMultiLang(multilang, language_names)
            icons = " ".join([icons, other_langs])

        if category_theme:
            style = category_theme
        else:
            style = site.config.site_style

        if site.config.rename_images == "True":
            renamed_fn = image_rename_pattern.format(
                comic=series_slug,
                page=page_padded,
                chapter=i.chapter,
                height=i.height,
                width=i.width,
                titleslug=title_slug,
                date=i.date_s,
                ext=os.path.splitext(img_path)[1][1:])
            renamed_path = os.path.join(
                pages_path,
                renamed_fn)
        else:
            renamed_fn = img_path
            renamed_path = os.path.join(
                pages_path,
                img_path)
        source_path = os.path.join(
            i_path,
            img_path)
        shutil.copyfile(
            source_path,
            renamed_path)
        i.img = renamed_fn
        dictified_strip["img"] = i.img
        jsoncat["strips"].append(dictified_strip)

        if site.config.rename_images == "True":
            new_meta = image_rename_pattern.format(
                comic=series_slug,
                page=page_padded,
                chapter=i.chapter,
                height=i.height,
                width=i.width,
                titleslug=title_slug,
                date=i.date_s,
                ext="meta")
        else:
            new_meta = i.metaf
        new_meta_path = os.path.join(
            pages_path,
            new_meta)
        old_meta_path = os.path.join(
            i_path,
            i.metaf)
        shutil.copyfile(
            old_meta_path,
            new_meta_path)

        if site.config.rename_images == "True":
            new_transcr = image_rename_pattern.format(
                comic=series_slug,
                page=page_padded,
                chapter=i.chapter,
                height=i.height,
                width=i.width,
                titleslug=title_slug,
                date=i.date_s,
                ext="transcript")
        else:
            new_transcr = transcript_file
        if os.path.basename(transcript_file) != "no_transcript.transcript":
            new_transcr_path = os.path.join(pages_path, new_transcr)
            old_transcr_path = os.path.join(i_path, transcript_file)
            shutil.copyfile(old_transcr_path,new_transcr_path)

        if scrollto == "":
            skiplink = "#comic"
        else:
            skiplink = scrollto
        n_string = base_template.format(
            lang=lang,
            site_style=style,
            header_title=header_title,
            linkrels=linkrels,
            banner=banner,
            category=html.escape(category),
            top_site_nav=top_site_nav,
            h1_title = h1_title,
            alt_text = alt_text,
            top_nav = top_nav,
            next_page=next_page,
            img_path="pages/"+renamed_fn,
            page_alt = translated_strings["page_alt_s"].format(page=page),
            bottom_nav = bottom_nav,
            commentary = commentary,
            statline = statline,
            metadatafile = "pages/"+new_meta,
            tb=tb,
            year=year,
            author=author,
            icons=icons,
            home_s=translated_strings["home_s"],
            archive_s=translated_strings["archive_s"],
            caption_s=translated_strings["caption_s"],
            metadata_s=translated_strings["meta_s"],
            copyright_statement=i.copyright_statement,
            stylesheet_name_s=translated_strings["stylesheet_name_s"],
            skiplink=skiplink,
            skip_s=translated_strings["skip_s"],
            scrollto=scrollto,
            page_s=translated_strings["page_s"],
            meta_s=translated_strings["meta_s"],
            generator_s=translated_strings["generator_s"],
            goarchive_s=translated_strings["goarchive_s"],
            url=page_url)

        logmesg = "Writing {html_fn}...".format(html_fn=html_filename)
        logMsg(logmesg,".")
        with open(out_file,"w+",encoding="utf-8") as fout:
            fout.write(n_string)
        logmesg = "{html_fn} written.".format(html_fn=html_filename)
        logMsg(logmesg,".")
        modified_time = datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),"%Y-%m-%dT%H:%M:%S.%fZ")
        sitemap_loc = {"loc": page_url, "lastmod": modified_time}
        site.sitemap.append(sitemap_loc)

        ###########################################################################

        i.clicense = clicense
        i.file_name = renamed_fn
        i.html_filename = html_filename
        i.lang = lang
        i.meta_fn = new_meta
        i.o_meta_fn = i.metaf
        i.o_transcr_fn = i.transf
        i.page_int = page_int
        i.title_slug = title_slug
        i.transcr_fn = new_transcr
        if match.chapters not in falses:
            i.chapter = chapter

    ## Sitewide copyright statement
    if not hasattr(site, "copyright_statement"):
        if publicdomain == False:
            last_year, first_year = checkExtremes(years)
            if first_year == last_year:
                year = first_year
            else:
                year = "{fy}&ndash;{ly}".format(fy=first_year, ly=last_year)
            copyright_statement = "<p>&copy; {year} {author}. {clicense}</p>".format(
                year=year,
                author=author,
                clicense=site_license_s)
        else:
            copyright_statement = wrapWithTag(
                license_s,
                "p")
        site.copyright_statement = copyright_statement

        banner_path = os.path.join(o_path, banner)

        if os.path.exists(banner_path) == False:
            old_banner_path = os.path.join(i_path, banner)
            shutil.copy(old_banner_path,banner_path)
            logmesg = "Banner {banner} copied.".format(banner=banner)
            logMsg(logmesg,".")
        else:
            pass

    ## If there are multiple series that have separate themes,
    ## time 2 concatenate the stylesheets.

    if category_theme:
        logmesg = "Categories have separate themes. Concatenating stylesheets..."
        logMsg(logmesg,".")
        copyMultiThemes(themes,c_path,o_path,assets_path)
        copyMultiArrows(themes,c_path,o_path,assets_path)

    ## Generate archives
    logmesg = "Generating archives..."
    logMsg(logmesg,".")

    ## Some things are done by page and some things are done by year.

    cpages_by_page = sorted(comics_base, key=lambda x: x.page_int)
    cpages_by_date = sorted(comics_base, key=lambda x: x.date)

    archives_r = []

    ## Get all pages for each series.
    for cat in cats_raw:
        cur_cat = []
        match = [item for item in ccomics if item.category == cat][0]
        for page in cpages_by_page:
            if page.category == cat:
                cur_cat.append(page)
        match.pbp = cur_cat

        cur_cat = []
        for page in cpages_by_date:
            if page.category == cat:
                cur_cat.append(page)
        match.pbd = cur_cat

        allp = len(match.pbd)-1

        match.fbp_link = match.pbp[0].html_filename
        match.lbp_link = match.pbp[allp].html_filename

        match.fbd_link = match.pbd[0].html_filename
        match.lbd_link = match.pbd[allp].html_filename

    sdate_comics = cpages_by_date
    spage_comics = cpages_by_page

    ex_by_page = []
    ex_by_date = []
    for comic in ccomics:
        logmesg = "Category: "+comic.category
        logMsg(logmesg,".")

        first_bypage = comic.fbp_link
        last_bypage = comic.lbp_link

        logmesg = "First/last by page:" + ", ".join([first_bypage, last_bypage])
        logMsg(logmesg,".")

        d = {"category":category,"first_bypage":first_bypage,
             "last_bypage":last_bypage}
        ex_by_page.append(d)

    for comic in ccomics:
        logmesg = "Category: "+comic.category
        logMsg(logmesg,".")

        first_bydate = comic.fbd_link
        last_bydate = comic.lbd_link

        d = {"category":category,"first_bydate":first_bydate,
             "last_bydate":last_bydate}
        ex_by_date.append(d)

    archive_d_secs = []

    logmesg = "Got first and last strips for each series."
    logMsg(logmesg,".")

    logmesg = "Generating archives..."
    print(logmesg)
    logMsg(logmesg,".")
    # Generate table of contents
    ccomic_chapters = [item.chapters for item in ccomics]
    no_chapters = all(item in falses for item in ccomic_chapters)
    if not no_chapters:
        toc_heading = "<h2>{toc_s}</h2>".format(toc_s=translated_strings["toc_s"])
        chapter_toc = ["""<section class="archive" role="directory">""",toc_heading,"""<ol class="chapterarch">"""]
        for comic in ccomics:
            if comic.chapters not in falses:
                for chapter in comic.chapters_list:
                    chapter_heading = translated_strings["category_chapter_s"].format(category=comic.category, chapter=chapter.chap_number, chapter_title=chapter.chap_title)
                    chapter_slug = slugify_url(chapter_heading)
                    escaped_chap_slug = html.escape(chapter_slug)
                    chapter.slug = "id-{slug}".format(slug=escaped_chap_slug)
                    chapter_link = """<li><a href="#{slug}">{title}</a></li>""".format(slug=chapter.slug, title=chapter_heading)
                    chapter_toc.append(chapter_link)
            else:
                logmesg = "Not generating table of contents, because I couldn't find any chapters."
                logMsg(logmesg, ".")
        chapter_toc.append("</ol></section>")
        toc = "".join(chapter_toc)
    else:
        toc = ""
    logmesg = "Table of contents:"
    logMsg(logmesg, ".")
    logMsg(toc, ".")

    for comic in tqdm(ccomics):
        category = comic.category
        status = comic.statuss
        comic_header = comic.header
        desc = comic.desc
        logmesg = "Currently working on {category}.".format(category=category)
        logMsg(logmesg,".")

        ## Get the comic-specific header.
        old_cheader_path = os.path.join(c_path, "input", comic_header)
        new_cheader_path = os.path.join(o_path, comic_header)

        copyHeader(old_cheader_path, new_cheader_path)
        ## This got reset somewhere? Huh
        match = comic

        archive_links_page = []
        archive_links_date = []
        for i in comic.pbp:
            archive_link = generatearchive.getLinks(i, scrollto, translated_strings)
            i.archive_link = archive_link
            if archive_link not in archive_links_page:
                archive_links_page.append(archive_link)
        for i in comic.pbd:
            if not hasattr(i, "archive_link"):
                archive_link = generatearchive.getLinks(i, scrollto, translated_strings)
                i.archive_link = archive_link
            if archive_link not in archive_links_date:
                archive_links_date.append(archive_link)
        if comic.chapters in falses:
            non_chaptered_archives = generatearchive.generateSeriesArchives(
                comic.category_escaped,
                status,
                archive_links_page)
            archives_r.append(non_chaptered_archives)

        if comic.chapters not in falses:
            for page in comic.pbp:
                if hasattr(page,"chapter"):
                    match = [item for item in ccomics if item.category == page.category][0]
                    cho = [item for item in match.chapters_list if item.chap_number == int(page.chapter)][0]
                    cho.pages.append(page)
                else:
                    logmesg = "No chapters found."
                    logMsg(logmesg,".")

        if comic.chapters not in falses:
            chapter_sections = []
            for chapi in match.chapters_list:
                in_this_chapter = []
                for page in chapi.pages:
                    in_this_chapter.append(page.archive_link)
                if single == True:
                    header_level = "2"
                else:
                    header_level = "3"
                archive_list = generatearchive.generateChapArchList(
                    in_this_chapter,
                    chapi.chap_number,
                    chapi.chap_title_escaped,
                    chapi.slug,
                    translated_strings,
                    header_level)
                chapter_sections.append(archive_list)
            chapter_sections_j = sep.join(chapter_sections)
            if single == False:
                chapter_archives_r = sep.join(['<section class="archive">',
                                               '<h2>{category}</h2>',
                                               '<p class="status">{status}</p>',
                                               chapter_sections_j,
                                               "</section>"])
            else:
                chapter_archives_r = sep.join(['<section class="archive">',
                                               '<p class="status">{status}</p>',
                                               chapter_sections_j,
                                               "</section>"])
            chapter_archives = chapter_archives_r.format(
                category=comic.category_escaped,status=comic.statuss)
            archives_r.append(chapter_archives)

    archives = sep.join(archives_r)

    if len(all_tags) > 0:
        tags_sorted = sorted(all_tags, key=lambda x: x.name)
        tag_section_content = ["""<section class="archive">""","<h2>{tags_s}</h2>".format(tags_s=translated_strings["tags_s"]),"""<ul class="tagslist">"""]
        for tag in tags_sorted:
            tag_count = len(tag.strips)
            tag_section_content.append("<li>{link} ({tag_count})</li>".format(link=tag.link,tag_count=tag_count))
        tag_section_content.append("</ul>")
        tag_section_content.append("</section>")
        tag_sectionn = sep.join(tag_section_content)
    else:
        tag_sectionn = ""

    arch_template_name = archive_t
    arch_template = os.path.join(c_path, arch_template_name)

    link_rel_l = ['<link rel="alternate" type="application/rss+xml" title="{rss_s}" href="feed.xml">'.format(rss_s=translated_strings["rss_s"]), '<link rel="alternate" type="application/json" title="{jsonfeed_name}" href="feed.json">'.format(jsonfeed_name=translated_strings["jsonfeed_name"])]
    link_rel = sep.join(link_rel_l)

    out_file = os.path.join(o_path, "archive.html")

    archive_header_title = "{site_title} - {archive_s}".format(site_title=site.config.site_title, archive_s=translated_strings["archive_s"])

    with open(arch_template) as f:
        arch_template = f.read()

        arch_string = arch_template.format(
            lang=lang,
            site_style=site.config.site_style,
            site_title=site.config.site_title,
            header_title=archive_header_title,
            linkrels=link_rel,
            banner=site.config.banner_filename,
            category=category,
            status=status,
            top_site_nav=top_site_nav,
            toc=toc,
            archive_sections=archives,
            tag_section=tag_sectionn,
            year=year,
            author=site.config.site_author,
            copyright_statement=copyright_statement,
            icons=icons,
            home_s=translated_strings["home_s"],
            archive_s=translated_strings["archive_s"],
            stylesheet_name_s=translated_strings["stylesheet_name_s"],
            skip_s=translated_strings["skip_s"],
            page_s=translated_strings["page_s"],
            meta_s=translated_strings["meta_s"],
            generator_s=translated_strings["generator_s"],
            goarchive_s=translated_strings["goarchive_s"],
            url = site.config.base_url+"archive.html")

        logmesg = "Writing {archive}...".format(archive="archive.html")
        logMsg(logmesg,".")
        with open(out_file,"w+",encoding="utf-8") as fout:
            fout.write(arch_string)
        logmesg = "{archive} written.".format(archive="archive.html")
        logMsg(logmesg,".")
        modified_time = datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),"%Y-%m-%dT%H:%M:%S.%fZ")
        sitemap_loc = {"loc":site.config.base_url+"archive.html","lastmod":modified_time}
        site.sitemap.append(sitemap_loc)

    ##Generate feed

    base_url = site.config.base_url

    rssmeta = {
            "author":site.config.site_author,
            "email":site.config.site_author_email,
            "language":site.config.language,
            "link":site.config.base_url,
            "desc":site.config.description,
            "title":site.config.site_title
        }

    rss = genrss.generateFeed(site.config.base_url,rssmeta,comics_base, o_path)

    ## Generate main page

    if single == True:
        template = os.path.join(c_path, index_t)

        out_file = os.path.join(o_path, "index.html")

        logmesg = "First/last by page:" + ", ".join([first_bypage, last_bypage])
        logMsg(logmesg,".")

        with open(template) as f:
            index_template = f.read()

            n_string = index_template.format(
                lang=lang,
                site_style=site.config.site_style,
                header_title=site.config.site_title,
                linkrels=link_rel,
                banner=site.config.banner_filename,
                site_title=site.config.site_title,
                category=category,
                top_site_nav=top_site_nav,
                header=header,
                desc=desc,
                status=status,
                latest=last_bypage,
                first=first_bypage,
                archive="archive.html",
                year=year,
                author=site.config.site_author,
                copyright_statement=copyright_statement,
                icons=icons,
                home_s=translated_strings["home_s"],
                archive_s=translated_strings["archive_s"],
                stylesheet_name_s=translated_strings["stylesheet_name_s"],
                skip_s=translated_strings["skip_s"],
                page_s=translated_strings["page_s"],
                meta_s=translated_strings["meta_s"],
                golatest_s=translated_strings["golatest_s"],
                gofirst_s=translated_strings["gofirst_s"],
                generator_s=translated_strings["generator_s"],
                goarchive_s=translated_strings["goarchive_s"],
                url = site.config.base_url+"index.html")


            logmesg = "Writing {indexh}...".format(indexh="index.html")
            logMsg(logmesg,".")
            with open(out_file,"w+",encoding="utf-8") as fout:
                fout.write(n_string)
            logmesg = "{indexh} written.".format(indexh="index.html")
            logMsg(logmesg,".")
            modified_time = datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),"%Y-%m-%dT%H:%M:%S.%fZ")
            sitemap_loc = {"loc":site.config.base_url+"index.html","lastmod":modified_time}
            site.sitemap.append(sitemap_loc)
    else:
        multi_secs = genmultipleindex.genMultipleIndex(
            ccomics,
            characters_page,
            translated_strings)
        secs = sep.join(multi_secs)

        template = os.path.join(c_path, index_t)

        out_file = os.path.join(o_path, "index.html")

        with open(template) as f:
            index_template = f.read()

            n_string = index_template.format(
                lang=lang,
                site_style=site.config.site_style,
                header_title=site.config.site_title,
                linkrels=link_rel,
                banner=site.config.banner_filename,
                site_title=site.config.site_title,
                category=site.config.site_title,
                top_site_nav=top_site_nav,
                multi_secs=secs,
                year=year,
                author=site.config.site_author,
                copyright_statement=copyright_statement,
                icons=icons,
                home_s=translated_strings["home_s"],
                archive_s=translated_strings["archive_s"],
                stylesheet_name_s=translated_strings["stylesheet_name_s"],
                skip_s=translated_strings["skip_s"],
                page_s=translated_strings["page_s"],
                meta_s=translated_strings["meta_s"],
                generator_s=translated_strings["generator_s"],
                goarchive_s=translated_strings["goarchive_s"],
                url = site.config.base_url+"index.html")


            logmesg = "Writing {indexh}...".format(indexh="index.html")
            logMsg(logmesg,".")
            with open(out_file,"w+",encoding="utf-8") as fout:
                fout.write(n_string)
            logmesg = "{indexh} written.".format(indexh="index.html")
            logMsg(logmesg,".")
            modified_time = datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),"%Y-%m-%dT%H:%M:%S.%fZ")
            sitemap_loc = {"loc":site.config.base_url+"index.html","lastmod":modified_time}
            site.sitemap.append(sitemap_loc)

    ## Generate characters page if necessary.
    if characters_page == True:
        site.jsonpoints["characters_page"] = "".join([site.config.base_url, "characters.html"])

        character_pages = []

        for conf in configs:

            fn = conf["chars"]
            if fn == "None" or fn == "False":
                logmesg = "No character file found for {category}, skipping...".format(category=conf["category"])
                logMsg(logmesg,".")
            else:
                fp = os.path.join(i_path, fn)
                logmesg = "Loading characters file {fn}...".format(fn=fn)
                logMsg(logmesg,".")

                try:
                    with open(fp,"r",encoding="utf-8") as f:
                        raw_text = f.read()
                except UnboundLocalError:
                    logmesg = "An Unbound Local Error has occurred. I'm probably looking for a page that doesn't exist."
                    logMsg(logmesg,".")
                except FileNotFoundError:
                    logmesg = "The characters page couldn't be built because I couldn't find the characters file at {fp}.".format(fp=fp)
                    logMsg(logmesg,".")
                characters_parsed = genchars.parseChars(raw_text)
                chard_i = jsoncat.setdefault("characters",{})
                chard = chard_i.setdefault("items",[])
                for chard_element in characters_parsed[2:]:
                    chard_el_dict = {}
                    for k,v in chard_element:
                        chard_el_dict[k] = v
                    chard.append(chard_el_dict)
                character_elements = genchars.genCharsPage(characters_parsed)

                ##Get character images
                for char in characters_parsed:
                    if type(char) == list:
                        if char[2][1] != "None":
                            img_source_path = os.path.join(i_path, char[2][1])
                            img_out_path = os.path.join(o_path, char[2][1])
                            shutil.copy(img_source_path,img_out_path)

                chars_template_path = os.path.join(c_path, chars_t)

                cat_slug = slugify_url(conf["category"])
                logmesg = "Slugified category name: {cat_slug}".format(cat_slug=cat_slug)
                logMsg(logmesg,".")

                if single == True:
                    out_name = "characters.html"
                else:
                    out_name = "".join([cat_slug, "-", "characters.html"])
                    cpd = {"charpage":out_name,
                           "category":conf["category"]}
                    character_pages.append(cpd)
                jsoncat["characters"]["url"] = "".join([base_url, out_name])

                out_file = os.path.join(o_path, out_name)

                chars_title_line = " - ".join([conf["category"], translated_strings["char_s"]])

                with open(chars_template_path) as f:
                    chars_template = f.read()

                    n_string = chars_template.format(
                        lang=lang,
                        site_style=site.config.site_style,
                        header_title=chars_title_line,
                        linkrels=link_rel,
                        banner=banner,
                        banner_alt=category,
                        title_line=translated_strings["char_s"],
                        top_site_nav=top_site_nav,
                        chars = character_elements,
                        year=year,
                        author=site.config.site_author,
                        copyright_statement=copyright_statement,
                        icons=icons,
                        home_s=translated_strings["home_s"],
                        archive_s=translated_strings["archive_s"],
                        stylesheet_name_s=translated_strings["stylesheet_name_s"],
                        skip_s=translated_strings["skip_s"],
                        page_s=translated_strings["page_s"],
                        meta_s=translated_strings["meta_s"],
                        generator_s=translated_strings["generator_s"],
                        goarchive_s=translated_strings["goarchive_s"],
                        url = site.config.base_url+out_name)


                    logmesg = "Writing {out_name}...".format(out_name=out_name)
                    logMsg(logmesg,".")
                    with open(out_file,"w+",encoding="utf-8") as fout:
                        fout.write(n_string)
                    logmesg = "{out_name} written.".format(out_name=out_name)
                    logMsg(logmesg,".")
                    modified_time = datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),"%Y-%m-%dT%H:%M:%S.%fZ")
                    sitemap_loc = {"loc":site.config.base_url+out_name,"lastmod":modified_time}
                    site.sitemap.append(sitemap_loc)

        if single == False:
            out_name = "characters.html"
            out_file = os.path.join(o_path, out_name)

            chars_title_line = " - ".join([site.config.site_title, translated_strings["char_s"]])

            charpage_elements = ['<div class="allchars">']

            logmesg = "Character pages: {character_pages}".format(character_pages=character_pages)
            logMsg(logmesg,".")
            for chpage in character_pages:
                character_page_line = ['<p><a href="',
                    chpage["charpage"],
                    '">',
                    chpage["category"],
                    "</a></p>"]
                character_page_line = "".join(character_page_line)
                charpage_elements.append(character_page_line)
            charpage_elements.append("</div>")
            charpages = sep.join(charpage_elements)

            with open(chars_template_path) as f:
                chars_template = f.read()

                n_string = chars_template.format(
                    lang=lang,
                    site_style=site.config.site_style,
                    header_title=chars_title_line,
                    linkrels=link_rel,
                    banner=site.config.banner_filename,
                    banner_alt=site.config.site_title,
                    title_line=chars_title_line,
                    top_site_nav=top_site_nav,
                    chars = charpages,
                    year=year,
                    author=site.config.site_author,
                    copyright_statement=copyright_statement,
                    icons=icons,
                    home_s=translated_strings["home_s"],
                    archive_s=translated_strings["archive_s"],
                    stylesheet_name_s=translated_strings["stylesheet_name_s"],
                    skip_s=translated_strings["skip_s"],
                    page_s=translated_strings["page_s"],
                    meta_s=translated_strings["meta_s"],
                    generator_s=translated_strings["generator_s"],
                    goarchive_s=translated_strings["goarchive_s"],
                    url = site.config.base_url+out_name)

                logmesg = "Writing {out_name}...".format(out_name=out_name)
                logMsg(logmesg,".")
                with open(out_file,"w+",encoding="utf-8") as fout:
                    fout.write(n_string)
                logmesg = "{out_name} written.".format(out_name=out_name)
                logMsg(logmesg,".")
                modified_time = datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),"%Y-%m-%dT%H:%M:%S.%fZ")
                sitemap_loc = {"loc":site.config.base_url+out_name,"lastmod":modified_time}
                site.sitemap.append(sitemap_loc)

    ## Generate extras page if necessary.
    if extras_page == True:

        extras_j = os.path.join(i_path, "Extra.json")
        if os.path.exists(extras_j):
            extras,j = genextra.gen_extra(i_path,o_path,extras_j,translated_strings)
            site.jsonpoints["extras"] = j

            extr_title = " - ".join([site.config.site_title, translated_strings["extra_s"]])

            ex_html_filename = "extras.html"
            out_file = os.path.join(
                o_path,
                ex_html_filename)
            site.jsonpoints["extras_page"] = "".join([base_url, ex_html_filename])

            with open(extra_t) as f:
                extra_template = f.read()

            extras_html = extra_template.format(
                lang=lang,
                site_style=site.config.site_style,
                header_title=extr_title,
                h1_title=translated_strings["extra_s"],
                stylesheet_name_s=translated_strings["stylesheet_name_s"],
                home_s=translated_strings["home_s"],
                linkrels=linkrels,
                skip_s=translated_strings["skip_s"],
                banner=site.config.banner_filename,
                category=category,
                top_site_nav=top_site_nav,
                extras=extras.content,
                copyright_statement=copyright_statement,
                generator_s=translated_strings["generator_s"],
                icons=icons,
            )

            with open(out_file,"w",encoding="utf-8") as fout:
                fout.write(extras_html)
            logmesg = "Extras page written to {out_file}.".format(out_file="extras.html")
            logMsg(logmesg,".")
            modified_time = datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),"%Y-%m-%dT%H:%M:%S.%fZ")
            sitemap_loc = {"loc":site.config.base_url+ex_html_filename,"lastmod":modified_time}
            site.sitemap.append(sitemap_loc)
        else:
            logmesg = "Extra pages are supposed to be generated, but Extras.json wasn't found in input/. Make sure it exists and is valid, then try again."
            logMsg(logmesg,".")
    else:
        logmesg = "Not generating extras page..."
        logMsg(logmesg,".")

###############################################################################
    ## Generate tags pages if necessary
    if len(all_tags) > 0:
        logmesg = "Generating tag indices..."
        print(logmesg)
        logMsg(logmesg,".")

        for tag in tqdm(all_tags):
            tags_links_page = ["""<ol class="tagslist">"""]
            tag_outn = "tag-{tag_slug}.html".format(tag_slug=tag.slug)
            tag_outf = os.path.join(o_path, tag_outn)
            tag_h = "{tags_s}: {tag}".format(tags_s=translated_strings["tags_s"],tag=tag.name)
            for strip in tag.strips:
                tag_l = translated_strings["h1_s"].format(category=strip.category,title=strip.title,page=strip.page)
                link_format = """<li><a href="{html_filename}">{tag_l}</a></li>"""
                tag_link = link_format.format(html_filename=strip.html_filename,tag_l=tag_l)
                tags_links_page.append(tag_link)
            tags_links_page.append("</ol>")
            tag_section = sep.join(tags_links_page)

            link_rel_l = ['<link rel="alternate" type="application/rss+xml" title="{rss_s}" href="feed.xml">'.format(rss_s=translated_strings["rss_s"])]
            link_rel = sep.join(link_rel_l)

            tag_template_name = archive_t
            tag_template = os.path.join(c_path, tag_template_name)

            with open(tag_template) as f:
                tag_template = f.read()

            tag_html = tag_template.format(
                lang=lang,
                site_style=site.config.site_style,
                site_title=site.config.site_title,
                header_title=tag_h,
                linkrels=link_rel,
                banner=site.config.banner_filename,
                category=category,
                status=status,
                top_site_nav=top_site_nav,
                toc="",
                archive_sections=tag_section,
                tag_section="",
                year=year,
                author=site.config.site_author,
                copyright_statement=copyright_statement,
                icons=icons,
                home_s=translated_strings["home_s"],
                archive_s=translated_strings["archive_s"],
                stylesheet_name_s=translated_strings["stylesheet_name_s"],
                skip_s=translated_strings["skip_s"],
                page_s=translated_strings["page_s"],
                meta_s=translated_strings["meta_s"],
                generator_s=translated_strings["generator_s"],
                goarchive_s=translated_strings["goarchive_s"],
                url = site.config.base_url+tag_outn)

            with open(tag_outf,"w",encoding="utf-8") as fout:
                fout.write(tag_html)
            logmesg = "Tag page written to {out_file}.".format(out_file=tag_outn)
            logMsg(logmesg,".")
            modified_time = datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),"%Y-%m-%dT%H:%M:%S.%fZ")
            sitemap_loc = {"loc":site.config.base_url+tag_outn,"lastmod":modified_time}
            site.sitemap.append(sitemap_loc)

###############################################################################

    ## Generate sitemap
    sitemap_close = '</urlset>'
    sitemap_sorted = sorted(site.sitemap,key=lambda k:k['loc'])
    ## Move index to the beginning
    for sitepage in sitemap_sorted:
        if sitepage["loc"][-11:] == "/index.html":
            smap_index_ind = sitemap_sorted.index(sitepage)
    sitemap_sorted.insert(0, sitemap_sorted.pop(smap_index_ind))
    formatted_sitemap = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for sitepage in sitemap_sorted:
        smap_entry = "<url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>".format(loc=sitepage["loc"],lastmod=sitepage["lastmod"])
        formatted_sitemap.append(smap_entry)
    formatted_sitemap.append("</urlset>")
    sitemap = "\n".join(formatted_sitemap)
    sitemap_xml_fn = "sitemap.xml"
    sitemap_out = os.path.join(o_path, sitemap_xml_fn)
    with open(sitemap_out,"w",encoding="utf-8") as fout:
        fout.write(sitemap)
    logmesg = "Generated sitemap at {sitemap_fn}.".format(sitemap_fn=sitemap_xml_fn)
    logMsg(logmesg,".")

    ## Generate JSON endpoints file

    json_fn = "site.json"
    jsonpoints_out = os.path.join(o_path, json_fn)
    with open(jsonpoints_out, "w", encoding="utf-8") as fout:
        json.dump(site.jsonpoints, fout)
    logmesg = "Generated JSON endpoints file at {json_fn}.".format(json_fn=json_fn)
    logMsg(logmesg,".")

    ## Generate JSON Feed
    json_feed_contents = springheel.genjsonfeed.genJsonFeed(site.jsonpoints, translated_strings)
    jsonfeed_fn = "feed.json"
    jsonfeed_out = os.path.join(o_path, jsonfeed_fn)
    with open(jsonfeed_out, "w", encoding="utf-8") as fout:
        json.dump(json_feed_contents, fout)
    logmesg = "Generated JSON Feed at {jsonfeed_fn}.".format(jsonfeed_fn=jsonfeed_fn)
    logMsg(logmesg,".")

    logmesg = "Springheel compilation complete! ^_^"
    print(logmesg)
    logMsg(logmesg,".")

def init():
    """Initialize a Springheel project."""
    springheelinit.copyAssets()

def version():
    """Print version information."""
    print("{name} {version} copyright 2017-2020 {author}. Some rights reserved. See LICENSE.".format(name=springheel.name,author=springheel.author,version=springheel.__version__))
    print("Installed to {dir}.".format(dir=sys.modules['springheel'].__path__[0]))
    print("Run springheel-init to create a new site in the current directory, or springheel-build to regenerate the site.")








