'''
WikiLinks Extension for Python-Markdown
======================================

Converts [[WikiLinks]] and [[label|wikilinks]] to relative links.

Derived from <https://Python-Markdown.github.io/extensions/wikilinks>

Original code Copyright [Waylan Limberg](http://achinghead.com/).

All changes Copyright The Python Markdown Project

License: [BSD](https://opensource.org/licenses/bsd-license.php)

'''

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree
import urllib.parse
from . import backend

# action keyword in wikilinks
_ACTION_KW = 'action:'


def build_url(target):
    """ Build a url from the wiki target. """
    if target.startswith(_ACTION_KW):
        target = target[len(_ACTION_KW):]
        if not target:
            return None
        return '../' + urllib.parse.quote(target, safe='/#?=')

    # anchor link in the current page, return the anchor
    if target.startswith('#'):
        return urllib.parse.quote(target, safe='#')

    # default action is to view the page
    return '../view/' + urllib.parse.quote(target, safe='#')


def is_dangling(target):
    '''Return True if the wiki page is missing
    '''
    # assume action link are ok
    if target.startswith(_ACTION_KW):
        return False

    pagename = target.split('#')[0]
    if not pagename or pagename in backend.get_pages_list():
        return False

    return True


class WikiLinkExtension(Extension):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        self.md = md

        # append to end of inline patterns
        WIKILINK_RE = r'\[\[\s*((?P<label>[^][]+)\s*\|\s*)?(?P<target>[^][|]+?)\s*\]\]'
        wikilinkPattern = WikiLinksInlineProcessor(WIKILINK_RE)
        wikilinkPattern.md = md
        md.inlinePatterns.register(wikilinkPattern, 'wikilink', 75)


class WikiLinksInlineProcessor(InlineProcessor):
    def __init__(self, pattern):
        super().__init__(pattern)

    def handleMatch(self, m, data):
        mdict = m.groupdict()
        target = mdict['target']
        label = mdict['label'] or target
        url = build_url(target)
        if url:
            a = etree.Element('a')
            a.text = label
            a.set('href', url)
            link_class = ['wikilink']
            if is_dangling(target):
                link_class.append('text-danger')
            a.set('class', ' '.join(link_class))
        else:
            a = ''
        return a, m.start(0), m.end(0)


def makeExtension(**kwargs):  # pragma: no cover
    return WikiLinkExtension(**kwargs)
