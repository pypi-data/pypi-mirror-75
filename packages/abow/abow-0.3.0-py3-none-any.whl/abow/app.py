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

import re
import urllib.parse
import builtins
import math
import bottle
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

from . import alerts
from . import backend
from . import config
from . import l10n
from . import render
from . import tags

# instanciate the bottle application
app = bottle.Bottle()


def init():
    '''Initialisation of the application
    '''
    # globally setup the deferred gettext
    builtins.__dict__['__'] = l10n.deferred_gettext

    config.init(app.config)
    l10n.init()
    bottle.TEMPLATE_PATH.insert(0, config.get('abow.template_path'))

    if bottle.DEBUG:
        alerts.add('info', __('Application started in debug mode.'))


# setup the app
init()


def _is_modified():
    '''Manage the Last-Modified and If-Modified-Since headers

    Avoid recomputing and resending a page if already cached by the browser
    '''
    # make sure the browser don't use stall data
    bottle.response.set_header('Cache-Control', 'no-cache')

    # no caching when debugging
    if bottle.DEBUG:
        return True

    last_modified = backend.get_mtime()
    ims = bottle.request.environ.get('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = bottle.parse_date(ims.split(";")[0].strip())
    if ims is not None and ims >= math.floor(last_modified):
        return False

    last_modified = bottle.http_date(last_modified)
    bottle.response.set_header('Last-Modified', last_modified)

    return True


def get_url(routename, **kwargs):
    '''Local version of get_url to manage static resources hosted outside
    of the app
    '''
    if routename == 'static':
        static_url = config.get('abow.static_url')
        if static_url:
            return urllib.parse.urljoin(static_url + '/', kwargs['filepath'])
    return app.get_url(routename, **kwargs)


def init_tpl_response(action='', title=''):
    '''Create a dictionary with the minimal info needed to render a template
    '''
    return {
        'get_url': app.get_url,
        'alerts': alerts,
        'help_page': config.get('abow.help_page'),
        'lang': l10n.get_lang(),
        'action': action,
        'title': title,
        }


@app.get('/static/<filepath:path>', name='static')
def get_static(filepath):
    '''Serve the static resources
    '''
    return bottle.static_file(filepath, root=config.get('abow.static_path'))


@app.get('/', name='root')
def redirect_to_index():
    '''Redirect to the index page, the main page of the wiki
    '''
    welcome_page = config.get('abow.welcome_page')
    return bottle.redirect('view/' + welcome_page, code=302)


@app.get('/view/<pagename>', name='view')
@bottle.view('view')
def view_page(pagename):
    '''Display a page of the wiki
    '''
    if not _is_modified():
        return bottle.HTTPResponse(status=304)

    data = init_tpl_response('view', pagename)
    data['pagename'] = pagename
    data['tags'] = tags.get_tags(pagename)
    data.update(render.render(backend.get_content(pagename)))

    return data


@app.get('/edit/<pagename>', name='edit')
@bottle.view('edit')
def edit_page(pagename):
    '''Edit a page of the wiki
    '''
    if not _is_modified():
        return bottle.HTTPResponse(status=304)

    data = init_tpl_response('edit', _('Edit {}').format(pagename))
    data.update({
        'pagename': pagename,
        'tags': '; '.join(tags.get_tags(pagename)),
        'all_tags': tags.get_all_tags(),
        'content': backend.get_content(pagename),
        })
    return data


@app.get('/tag/<tag>')
@app.get('/search/pages', name='search')
@bottle.view('list_pages')
def list_pages(tag=None):
    '''Display the list of pages in the wiki
    optionally filtered by tag or text search
    '''
    if not _is_modified():
        return bottle.HTTPResponse(status=304)

    data = init_tpl_response('list_pages')
    text = bottle.request.query.getunicode('text')
    if tag:
        data['title'] = _('List of pages tagged {}').format(tag)
        data['pages_list'] = tags.search(tag)
    elif text:
        data['title'] = _('List of pages containing {}').format(text)
        data['pages_list'] = backend.search_pages(text)
        if '/' not in text:
            data['page_exists'] = text in backend.get_pages_list()
            data['pagename'] = text
    else:
        data['title'] = _('List of pages')
        data['pages_list'] = backend.get_pages_list()

    return data


@app.get('/about', name='about')
@bottle.view('about')
def about(tag=None):
    '''Display the about page
    '''
    if not _is_modified():
        return bottle.HTTPResponse(status=304)

    data = init_tpl_response('about', _('About'))
    try:
        data['version'] = _('Version {}').format(metadata.version(__package__))
    except metadata.PackageNotFoundError:
        data['version'] = _('Developement version')
    data['config'] = app.config
    return data


@app.error(403)
@app.error(404)
@app.error(405)
@app.error(500)
@bottle.view('error')
def error(err):
    '''Display the various http errors with the wiki style
    '''
    data = init_tpl_response('error', _('Error {}').format(err.status_code))
    data['err_body'] = err.body
    return data


@app.post('/edit/<pagename>')
def save_page(pagename):
    '''Save the page from the edit form
    '''
    content = bottle.request.forms.getunicode('content')
    new_pagename = bottle.request.forms.getunicode('new_pagename')
    page_tags = bottle.request.forms.getunicode('tags')

    if not new_pagename or re.search(r'[/|]', new_pagename):
        bottle.abort(403, _('Page name cannot be blank and cannot contain \'/\' or \'|\''))

    if new_pagename != pagename and new_pagename in backend.get_pages_list():
        bottle.abort(403, _('A page named {} already exists').format(new_pagename))

    tags.set_tags(new_pagename, page_tags)
    backend.set_content(new_pagename, content)
    if new_pagename != pagename:
        backend.delete(pagename)

    return bottle.redirect('../view/' + urllib.parse.quote(new_pagename))


@app.put('/preview')
def preview():
    '''Render the passed-in text and return the html fragment generated
    '''
    content_type = bottle.request.content_type
    if 'charset=' in content_type:
        encoding = content_type.split('charset=')[-1].split(';')[0].strip()
    else:
        encoding = 'utf8'

    content = bottle.request.body.read()
    content = content.decode(encoding)
    return render.render(content)
