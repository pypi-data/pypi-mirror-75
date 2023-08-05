import io
import bottle
import pytest
import abow
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata


pytestmark = pytest.mark.usefixtures('backend_path')


def test_init():
    '''test app initialisation
    '''
    abow.alerts.clear()
    bottle.DEBUG = True
    abow.app.init()
    assert len(abow.alerts.get_list()) == 1
    bottle.DEBUG = False


def test_is_modified(monkeypatch):
    '''test is modified return value
    '''
    # empty backend
    assert abow.app._is_modified() is True

    # debug mode
    bottle.DEBUG = True
    assert abow.app._is_modified() is True
    bottle.DEBUG = False

    # create a page to have an backend mtime
    abow.backend.set_content('page1', 'abc')
    mtime = abow.backend.get_mtime()

    assert abow.app._is_modified() is True
    assert 'Last-Modified' in bottle.response.headers

    # simulate sending if modified since
    monkeypatch.setitem(bottle.request.environ,
                        'HTTP_IF_MODIFIED_SINCE',
                        bottle.http_date(mtime))
    assert abow.app._is_modified() is False

    monkeypatch.setitem(bottle.request.environ,
                        'HTTP_IF_MODIFIED_SINCE',
                        bottle.http_date(mtime - 1))
    assert abow.app._is_modified() is True


def test_get_url(monkeypatch):
    '''test url generation
    '''
    assert abow.app.get_url('root') == '/'
    assert abow.app.get_url('view', pagename='page1') == '/view/page1'

    def mock_cfg(key):
        return None
    monkeypatch.setattr(abow.config, 'get', mock_cfg)
    assert abow.app.get_url('static', filepath='test') == '/static/test'

    def mock_cfg(key):
        return '/outside'
    monkeypatch.setattr(abow.config, 'get', mock_cfg)
    assert abow.app.get_url('static', filepath='test') == '/outside/test'


def test_init_tpl_response():
    '''test the presence of the common keys
    '''
    expected = ['action', 'alerts', 'get_url', 'help_page', 'lang', 'title']
    resp = abow.app.init_tpl_response('abc', 'def')

    assert resp['action'] == 'abc'
    assert resp['title'] == 'def'
    assert len(expected) == len(resp.keys())
    assert sorted(expected) == sorted(resp.keys())


def test_static():
    '''test access to static resources
    '''
    assert abow.app.get_static(filepath='not-found').status_code == 404
    assert abow.app.get_static(filepath='css/abow.css').status_code == 200


def test_redirect_to_index(monkeypatch):
    '''test redirection to the wiki home page
    '''
    def mock_cfg(key):
        return 'welcome'
    monkeypatch.setattr(abow.config, 'get', mock_cfg)

    with pytest.raises(bottle.HTTPResponse) as resp:
        abow.app.redirect_to_index()

    assert resp.value.status_code == 302
    assert 'view/welcome' in resp.value.headers['Location']


def test_view_page():
    '''test the view page
    '''
    pagename = 'abc'
    data = abow.app.view_page.__wrapped__(pagename)
    assert data['pagename'] == pagename
    assert data['title'] == pagename
    assert data['action'] == 'view'
    assert {'tags', 'html', 'toc'}.issubset(set(data.keys()))


def test_edit_page():
    '''test the edit page
    '''
    pagename = 'abc'
    data = abow.app.edit_page.__wrapped__(pagename)
    assert data['pagename'] == pagename
    assert pagename in data['title']
    assert data['action'] == 'edit'
    assert {'tags', 'all_tags', 'content'}.issubset(set(data.keys()))


def test_list_pages(monkeypatch):
    '''test the list pages
    '''
    data = abow.app.list_pages.__wrapped__()
    assert data['action'] == 'list_pages'
    assert 'pages_list' in data.keys()

    monkeypatch.setitem(bottle.request.environ,
                        'bottle.request.query',
                        bottle.FormsDict({'text': 'abc'}))
    data = abow.app.list_pages.__wrapped__()
    assert data['action'] == 'list_pages'
    assert data['pagename'] == 'abc'
    assert {'pages_list', 'page_exists', 'pagename'}.issubset(data.keys())

    monkeypatch.setitem(bottle.request.environ,
                        'bottle.request.query',
                        bottle.FormsDict({'text': 'abc/def'}))
    data = abow.app.list_pages.__wrapped__()
    assert 'pages_list' in data.keys()
    assert {'page_exists', 'pagename'}.isdisjoint(data.keys())

    data = abow.app.list_pages.__wrapped__(tag='a')
    assert data['action'] == 'list_pages'
    assert 'pages_list' in data.keys()


def test_about(monkeypatch):
    '''test the about page
    '''
    data = abow.app.about.__wrapped__()
    assert data['action'] == 'about'
    assert {'version', 'config'}.issubset(set(data.keys()))

    def mock_get(key):
        raise metadata.PackageNotFoundError
    monkeypatch.setattr(metadata, 'version', mock_get)
    data = abow.app.about.__wrapped__()


def test_not_modified(monkeypatch):
    '''test the 304 reply
    '''
    # create a page to have an backend mtime
    abow.backend.set_content('page1', 'abc')
    mtime = abow.backend.get_mtime()

    # simulate sending if modified since
    monkeypatch.setitem(bottle.request.environ,
                        'HTTP_IF_MODIFIED_SINCE',
                        bottle.http_date(mtime))

    routes = [
        abow.app.view_page,
        abow.app.edit_page,
        abow.app.list_pages,
        abow.app.about,
        ]

    for route in routes:
        assert route.__wrapped__('').status_code == 304


def test_error():
    '''test the error page
    '''
    err = bottle.HTTPError(404)
    data = abow.app.error.__wrapped__(err)
    assert data['action'] == 'error'
    assert 'err_body' in data.keys()


def test_save_page(monkeypatch):
    '''test the save page
    '''
    form = bottle.FormsDict()
    form['content'] = 'abc'
    form['new_pagename'] = 'page1'
    form['tags'] = 'tag1'
    monkeypatch.setitem(bottle.request.environ,
                        'bottle.request.forms',
                        form)

    with pytest.raises(bottle.HTTPResponse) as resp:
        abow.app.save_page('page1')
    assert resp.value.status_code == 302
    assert 'view/page1' in resp.value.headers['Location']

    with pytest.raises(bottle.HTTPResponse):
        abow.app.save_page('page2')

    form['new_pagename'] = 'page1/1'
    with pytest.raises(bottle.HTTPError) as err:
        abow.app.save_page('page1')
    assert err.value.status_code == 403

    form['new_pagename'] = 'page1|1'
    with pytest.raises(bottle.HTTPError) as err:
        abow.app.save_page('page1')
    assert err.value.status_code == 403

    form['new_pagename'] = 'page1'
    with pytest.raises(bottle.HTTPError) as err:
        abow.app.save_page('page2')
    assert err.value.status_code == 403

    form['new_pagename'] = 'page3'
    with pytest.raises(bottle.HTTPResponse) as resp:
        abow.app.save_page('page1')
    assert resp.value.status_code == 302
    assert 'view/page3' in resp.value.headers['Location']


def test_preview(monkeypatch):
    '''test the preview page
    '''
    monkeypatch.setitem(bottle.request.environ,
                        'CONTENT_TYPE',
                        'text/plain')
    monkeypatch.setitem(bottle.request.environ,
                        'bottle.request.body',
                        io.BytesIO(b'abc'))
    res = abow.app.preview()
    assert res['html'] == '<p>abc</p>'

    monkeypatch.setitem(bottle.request.environ,
                        'CONTENT_TYPE',
                        'text/plain; charset=UTF-8')
    res = abow.app.preview()
    assert res['html'] == '<p>abc</p>'
