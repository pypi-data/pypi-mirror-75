#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
# Springheel - Social media icons
########
# Copyright 2017 garrick. Some rights reserved.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Show icons and links to social media sites."""

from springheel.__init__ import *

def getButtons(site, translated_strings):
    """
    Show social media icons on the site as desired.

    Parameters
    ----------
    site : Site
        The site for which icons are being generated.
    translated_strings : dict
        The translation file contents for this site.

    Returns
    -------
    social_links : list
        Dictionaries with metadata about other sites.
    icons : str
        HTML img elements that hyperlink to other sites.
    """

    twitter_handle = site.config.twitter_handle
    tumblr_handle = site.config.tumblr_handle
    patreon_handle = site.config.patreon_handle

    pump_url = site.config.pump_url
    diaspora_url = site.config.diaspora_url
    liberapay_handle = site.config.liberapay_handle
    mastodon_url = site.config.mastodon_url

    rss_url = "feed.xml"
    jsonfeed_url = "feed.json"

    social_links = []

    rss_link = {"url": rss_url, "site": "",
                "title": translated_strings["rss_s"], "image": "rss.png"}
    social_links.append(rss_link)
    jf_link = {"url": jsonfeed_url, "site": "",
                "title": translated_strings["jsonfeed_name"], "image": "jsonfeed.png"}
    social_links.append(jf_link)

    if site.config.social_icons != "False":
        if twitter_handle != "False":
            twitter_url = "https://twitter.com/" + twitter_handle
            twitter = {"url": twitter_url, "site": "twitter",
                       "title": "Twitter", "image": "twitter.png"}
            social_links.append(twitter)
        if tumblr_handle != "False":
            tumblr_url = "https://" + tumblr_handle + ".tumblr.com"
            tumblr = {"url": tumblr_url, "site": "tumblr",
                      "title": "tumblr.", "image": "tumblr.png"}
            social_links.append(tumblr)
        if patreon_handle != "False":
            patreon_url = "https://www.patreon.com/" + patreon_handle
            patreon = {"url": patreon_url, "site": "Patreon",
                       "title": "Patreon", "image": "patreon.png"}
            social_links.append(patreon)
        if liberapay_handle != "False":
            liberapay_url = "https://liberapay.com/" + liberapay_handle
            liberapay = {"url": liberapay_url, "site": "Liberapay",
                         "title": "Liberapay", "image": "liberapay.png"}
            social_links.append(liberapay)
        if pump_url != "False":
            # An additional, identi.ca-specific icon has also been provided.
            # To use it, simply move or rename the existing pump.png (just in case) and rename identica.png to pump.png.
            pump = {"url": pump_url, "site": "pump",
                    "title": "Pump.io", "image": "pump.png"}
            social_links.append(pump)
        if diaspora_url != "False":
            diaspora = {"url": diaspora_url, "site": "diaspora",
                        "title": "diaspora*", "image": "diaspora.png"}
            social_links.append(diaspora)
        if mastodon_url != "False":
            mastodon = {"url": mastodon_url, "site": "mastodon",
                        "title": "Mastodon", "image": "mastodon.png"}
            social_links.append(mastodon)

    social_icons = []
    for i in social_links:
        icon = springheel.__init__.wrapImage(i["url"], i["title"], i["image"])
        social_icons.append(icon)

    icons = " ".join(social_icons)

    return(social_links, icons)
