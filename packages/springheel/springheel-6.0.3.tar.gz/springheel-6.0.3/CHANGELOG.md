# Springheel Changelog

## 6.0.3
+ Fixed a bug that kept headers and banners from copying to output under some circumstances.

## 6.0.2
+ Removing some accidental JSON debug output from building. ^_^;;

## 6.0.1
+ Replaced awesome-slugify with [python-slugify](https://pypi.org/project/python-slugify/), as the former is no longer actively developed.
+ Minor updates to JSON Feed generation to comply with version 1.1 of the spec.

## 6.0.0 "Ukyou"
+ Added new themes "fluff", "crystal", and "elemental" (which is configurable, like "seasonal").
+ Added progress bars for time-consuming parts of site generation, like finding images and creating tag index pages. This feature adds [tdqm](https://pypi.org/project/tqdm/) as a dependency.
+ Added rudimentary [JSON Feed](https://jsonfeed.org/) support. I hacked this together myself based on existing JSON endpoint bits; it validates, but should be considered experimental.
+ Added feature to generate tables of contents on archive pages if the comic has chapters.
+ Improvements to the "book", "fairy", "gothic", and "city" themes.
+ Optimized some graphics slightly. There should be little or no visual difference.
+ Cut some unneeded mixin imports from the theme SCSS files.
+ Fixed an error in the default conf.ini -- `scrollto` was mistakenly listed as `skipto` and so did not work.
+ Fixed several bugs in non-chaptered comic archives.
+ Changed the recommended alternate value of `scrollto` from "comic" to "topbox" so that above-strip navigation can still be accessed. "comic" is still accepted as a valid value for `scrollto`.
+ Added `scrollto` to archive links as well.
+ Allow disabling `scrollto` by setting it to `False`.
+ Added classes and I.D.s to some elements that did not have them.
+ Added social button for Mastodon.
+ RSS feed generation bugfixes: less hacky output selection and comment creation, and strips with a more recent date will appear closer to the top of the XML file.
+ Cleaned up social media icon code and markup a bit.
+ Removed trailing spaces that were accidentally inserted after speaker identifiers in transcripts.
+ Many improvements to the HOWTO.md tutorial file.
+ Adding page URL as an argument to `format()` when generating pages. If you want to add something like a "share" button to your page templates (per the "Extending Springheel Sites" section of HOWTO.md), you can use `{url}` in place of a static permalink. Springheel will now replace that with the page's URL.
+ The default alt text that appears when `alt` is unset is now more informative.
+ Page numbering now sensibly allows for page number 0. (It previously started from 1.) This allows for cover pages and the like without creating confusing constructions like "Page #2 'Page 1'".
+ If they exist, some non-strip assets (e.g. stylesheets, site graphics, navigation arrows) are no longer rewritten when building, to avoid them being copied and re-copied over and over. Delete `output/assets` and `output/arrows` if you do want to overwrite these files.

## 5.2.4
+ Alt text for comic pages is now a translated string.
+ Extra images now have alt text, allowing screen readers on some platforms to announce their captions properly.

## 5.2.3
+ Finally accepted that my paltry attempt to support favicons was in error. Users who want to add favicons should edit their site's local templates (the old/bad favicon code has been replaced with a comment indicating where to insert the output from a dedicated favicon generator) and manually copy the appropriate files into `output`.
+ Fixed a couple of minor HTML errors in templates (mostly extra whitespace and single-quoted elements) and the processing of same.

## 5.2.2
+ Improved metadata parsing a bit.
+ Added missing docstrings.
+ Fixed some quirks in page-footer copyright statements.
+ Cleaned up some unused functions.
+ Updated HOWTO.md

## 5.2.1
+ Removed the `langcodes` dependency. Multi-language site linking should work the same as before, if not better.
+ Added display of the original language code as a fallback if Springheel doesn't know the proper name for a language during multi-language site linking.

## 5.2.0 "Bossun"
+ Made it possible to insert links to your Springheel site in other languages in the site footer, using the new `multilang` config option. Notably, this adds `langcodes` as a dependency (to display the language names correctly).
+ Added functionality to generate a JSON file (`output/site.json`) with detailed information about the site, including URL endpoints. This should theoretically make it easier to extend Springheel sites with other programs.
+ Fixed an error in social icon spacing. (Re-init any existing site templates.)
+ Updated HOWTO.md

## 5.1.0 "Senku"
+ Added a configuration option for skip links and comic navigation to scroll directly to the comic image, instead of to the page title.
+ Fixed an error that was preventing sites' local `strings.json` files from being used.
+ Completely rewrote comic navigation.
+ Started work on a Spanish translation. It's incomplete and likely weird in many places; I don't actually speak Spanish. (The translation is based entirely on poking around on Spanish webcomic sites to see how they render the common terms, double-checking with several dictionaries.)
+ Started a French translation in the same way, although I'm even less sure of this one's accuracy.
+ Removed references to GitHub from `setup.py` and templates in protest of their contract with ICE.

## 5.0.3
+ Fixed a major bug where comics on multi-comic sites were added to the wrong chapters.
+ Corrected the error message that appears if "status" is unset.

## 5.0.2
+ Fixed a bug where tag page results weren't being sorted correctly.
+ Archive page titles for single-comic sites are now translatable.
+ Fixed an error where colons couldn't be used in some metadata fields.
+ Removed the long-unnecessary language prompt when running `springheel-init`.
+ Lots of improvements to all themes. (Make sure to re-run `springheel-init` to update your stylesheets)

## 5.0.1
+ Started escaping most things that will appear as HTML.

## 5.0.0 "Azumane"
+ Added proper tagging system.
+ Added option for zero-padding page numbers.
+ Cleared out some unused stuff from archive and navigation generation + the default conf.ini
+ Fixed some issues with image renaming.
+ Fixed error where chaptered works sometimes appeared twice on archive pages.
+ Started naming major/minor versions ~~after hot anime dudes~~

## 4.1.0
+ Springheel now generates XML site maps of comic sites.
+ Cleaned up logging a bit.

## 4.0.0
+ Added new themes "revolution", "fairy", "sysadmin", and "might".
+ Separated traits from descriptions on character pages.
+ Fixed major error where a multi-comic site wouldn't generate if some comics had a characters file and some didn't.
+ Fixed bug where slugs were not URL-safe.
+ Fixed bug where the archive page's main heading wasn't getting translated.
+ Fixed bug where extras pages used a comic's title and banner, instead of the sitewide ones.
+ Slight improvements to "seasonal" and "showtime" themes.

## 3.0.3
+ Fixed a very stupid copy+paste error that caused public domain comics to be described as published from a U.R.L. (instead of their respective country).

## 3.0.2
+ Did a better job fixing the character bug from the previous version.
+ Fixed an error where non-transcribed comics wouldn't generate on Windows.
+ Fiddled with the markdown in HOWTO.md because it was displaying strangely in some programs.

## 3.0.1
+ Fixed a bug where archives weren't generating correctly for non-chaptered comics.
+ Fixed a bug where the ordering of character attributes changed randomly every time the page was regenerated.
+ Updated some information in the default conf.ini file.

## 3.0.0
+ Added extras page functionality
+ Added new theme "showtime"
+ Corrected <title> elements for character pages
+ Improved logging

## 2.0.0
+ Condensed template files into one
+ Improved accessibility
+ Updated translations

## 1.0.2
+ Fixed a bug where archives couldn't be generated for multi-comic sites.

## 1.0.1
+ Fixed the parts of the readme that said arrow was a dependency (it isn't).
+ Fixed a bug where .sass-cache was getting installed as if it were a theme.

## 1.0.0

+ Streamlined config files.
+ Tidied up all stylesheets and templates.
+ Added some more translation strings.
+ Refactored a whole lot of code and made it neater.
+ Fixed miscellaneous bugs.
+ Added new themes "rock" and "western".
+ Added better arrows for some themes.
