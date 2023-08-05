# A Bottle of Wiki — personal wiki
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2020  Benoît Monin <benoit.monin@gmx.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import markdown

from markdown.extensions.abbr import AbbrExtension
from markdown.extensions.admonition import AdmonitionExtension
from markdown.extensions.attr_list import AttrListExtension
from markdown.extensions.def_list import DefListExtension
from markdown.extensions.footnotes import FootnoteExtension
from markdown.extensions.md_in_html import MarkdownInHtmlExtension
from markdown.extensions.sane_lists import SaneListExtension
from markdown.extensions.toc import TocExtension

from pymdownx.betterem import BetterEmExtension
from pymdownx.caret import InsertSupExtension
from pymdownx.escapeall import EscapeAllExtension
from pymdownx.highlight import HighlightExtension
from pymdownx.keys import KeysExtension
from pymdownx.mark import MarkExtension
from pymdownx.superfences import SuperFencesCodeExtension
from pymdownx.tabbed import TabbedExtension
from pymdownx.tasklist import TasklistExtension
from pymdownx.tilde import DeleteSubExtension

from .mdx_tables import TableExtension
from .mdx_wikilinks import WikiLinkExtension


# markdown renderer
_md = None


def init():
    '''Initialize the renderer if needed
    '''
    global _md

    if _md is None:
        _md = markdown.Markdown(
            output_format='html5',
            extensions=[
                AbbrExtension(),
                AdmonitionExtension(),
                AttrListExtension(),
                DefListExtension(),
                FootnoteExtension(BACKLINK_TITLE=_('Jump back to reference %d')),
                MarkdownInHtmlExtension(),
                SaneListExtension(),
                TocExtension(marker='',
                             permalink='#',
                             permalink_class='permalink',
                             permalink_title='',
                             toc_depth=5,
                             baselevel=2),

                BetterEmExtension(),
                InsertSupExtension(),
                EscapeAllExtension(hardbreak=True, nbsp=True),
                HighlightExtension(linenums_style='pymdownx-inline'),
                KeysExtension(),
                MarkExtension(),
                SuperFencesCodeExtension(),
                TabbedExtension(),
                TasklistExtension(custom_checkbox=True),
                DeleteSubExtension(),

                WikiLinkExtension(),
                TableExtension(),
                ],
            )


def render(text):
    '''Render some text to html

    Return a tuple containing the rendered html and the table of content
    '''
    init()
    _md.reset()
    html = _md.convert(text)
    return {
        'html': html,
        'toc': _md.toc,
        }
