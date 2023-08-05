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

from collections import OrderedDict
import locale
import re

from . import backend


# attribute name for the tags
_ATTR = 'tags'


def get_tags(pagename):
    '''Return the list of tags of a page
    '''
    return backend.get_attr(pagename, _ATTR, [])


def set_tags(pagename, tags):
    '''Set the tags of a page
    '''
    if isinstance(tags, str):
        # convert to list by spliting on ; and ,
        tags = [t.strip() for t in re.split('[;,]', tags)]
    if not isinstance(tags, list):
        raise TypeError('tags must be a string or a list')

    # remove empty tags and duplicates but keep order
    tags = list(OrderedDict.fromkeys(filter(None, tags)))

    if get_tags(pagename) or tags:
        backend.set_attr(pagename, _ATTR, tags)


def search(tag):
    '''Search pages matching a tag and return a list

    Note: the list is sorted
    '''
    tagged_pages = []
    all_pages = backend.get_pages_list()

    for page in all_pages:
        tags = get_tags(page)
        if tag in tags:
            tagged_pages.append(page)

    return tagged_pages


def get_all_tags():
    '''Return the list of the tags of all pages

    Note: the list is sorted
    '''
    tags = set()
    pages = backend.get_pages_list()

    for page in pages:
        tags.update(get_tags(page))

    return sorted(tags, key=locale.strxfrm)
