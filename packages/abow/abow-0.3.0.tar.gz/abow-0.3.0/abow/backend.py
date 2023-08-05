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

import os
import errno
import json
import locale
import time

from . import alerts
from . import config

# page content file extension
_CONTENT_EXT = '.md'

# page attributes file extension
_ATTR_EXT = '.json'

# pages attributes dictionary
# the key is the pagename, the value is a dictionary of attributes
_pages_attrs = {}


# time reference for the backend modification time
# use the application start time
_ref_mtime = time.time()


def _build_path(pagename='', ext=''):
    '''Return the path of a page
    '''
    return os.path.join(config.get('abow.backend_path'), pagename + ext)


def get_content(pagename):
    '''Return the content of a page or an empty string if the page is missing
    '''
    fp = _build_path(pagename, _CONTENT_EXT)
    try:
        with open(fp, 'r', encoding='utf8') as f:
            return f.read()
    except OSError as err:
        if err.errno != errno.ENOENT:
            alerts.add('warning',
                       __('Failed to read the content of page {}: {}.').format(
                           pagename, err.strerror))
        return ''


def set_content(pagename, content):
    '''Save the content of a page, create it if needed
    If the content is an empty string, delete the page
    '''
    fp = _build_path(pagename, _CONTENT_EXT)
    if content == '':
        delete(pagename)
    else:
        try:
            with open(fp, 'w', encoding='utf8') as f:
                f.write(content.replace('\r', ''))
        except OSError as err:
            alerts.add('danger',
                       __('Failed to save the content of page {}: {}.').format(
                           pagename, err.strerror))


def delete(pagename):
    '''Remove a page from storage and the attributes dict

    Raises OSError if the page cannot be deleted
    '''
    try:
        os.unlink(_build_path(pagename, _CONTENT_EXT))
    except OSError as err:
        if err.errno != errno.ENOENT:
            alerts.add('warning',
                       __('Failed to delete the content of page {}: {}.').format(
                           pagename, err.strerror))
    try:
        os.unlink(_build_path(pagename, _ATTR_EXT))
    except OSError as err:
        if err.errno != errno.ENOENT:
            alerts.add('warning',
                       __('Failed to delete the attributes of page {}: {}.').format(
                           pagename, err.strerror))
    try:
        del _pages_attrs[pagename]
    except KeyError:
        pass


def _load_attrs(pagename):
    '''Load the page attributes from file if needed
    '''
    if pagename not in _pages_attrs:
        fp = _build_path(pagename, _ATTR_EXT)
        try:
            with open(fp, 'r', encoding='utf8') as f:
                _pages_attrs[pagename] = json.load(f)
        except OSError as err:
            if err.errno != errno.ENOENT:
                alerts.add('warning',
                           __('Failed to load the attributes of page {}: {}.').format(
                               pagename, err.strerror))
            _pages_attrs[pagename] = {}


def get_attr(pagename, attr, default=None):
    '''Return one attribute of a page if found, or the default value
    '''
    _load_attrs(pagename)
    attrs = _pages_attrs.get(pagename, {})
    return attrs.get(attr, default)


def set_attr(pagename, attr, value):
    '''Set one attribute of a page
    '''
    _load_attrs(pagename)

    attrs = _pages_attrs.get(pagename, {})
    attrs[attr] = value
    _pages_attrs[pagename] = attrs

    fp = _build_path(pagename, _ATTR_EXT)
    try:
        with open(fp, 'w', encoding='utf8') as f:
            json.dump(_pages_attrs[pagename], f)
    except OSError as err:
        alerts.add('danger',
                   __('Failed to save the attributes of page {}: {}.').format(
                       pagename, err.strerror))


def _list_files():
    '''Return the list of files in the backend

    Note: the list is not sorted
    '''
    # empty pagename and extension gives the containing folder
    top = _build_path()
    try:
        _, _, filenames = next(os.walk(top))
    except StopIteration:
        filenames = []
    return filenames


def get_pages_list():
    '''Return the list of pages

    Note: the list is sorted
    '''
    # empty pagename and extension gives the containing folder
    filenames = _list_files()
    pages = [os.path.splitext(f)[0] for f in filenames if f.endswith(_CONTENT_EXT)]
    return sorted(pages, key=locale.strxfrm)


def get_mtime(pagename=None):
    '''Return the page modification time of a page or the whole backend

    Note: the mtime is the unix epoch as an integer
    '''
    mtime = [_ref_mtime]

    if pagename and os.path.exists(_build_path(pagename, _CONTENT_EXT)):
        paths = [
            _build_path(pagename, _ATTR_EXT),
            _build_path(pagename, _CONTENT_EXT),
            ]
    else:
        paths = [_build_path(f) for f in _list_files()]

    for fp in paths:
        try:
            mtime.append(int(os.path.getmtime(fp)))
        except OSError:
            pass

    return max(mtime)


def search_pages(text):
    '''search pages containing some text

    Note: the list is sorted
    '''
    matching_pages = []
    all_pages = get_pages_list()
    text = text.casefold()

    for page in all_pages:
        content = get_content(page).casefold()
        if text in content:
            matching_pages.append(page)

    return matching_pages
