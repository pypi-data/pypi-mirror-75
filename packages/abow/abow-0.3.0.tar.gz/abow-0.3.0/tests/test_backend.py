import time
import abow


def test_empty(backend_path):
    '''Test with an empty backend
    '''
    assert abow.backend.get_pages_list() == []
    assert abow.backend.get_mtime() == abow.backend._ref_mtime
    assert abow.backend.get_content('page1') == ''


def test_set_content(backend_path):
    '''Create some content and read it back
    '''
    abow.backend.set_content('page1', 'abc')
    assert abow.backend.get_content('page1') == 'abc'
    abow.backend.set_content('page1', 'def')
    assert abow.backend.get_content('page1') == 'def'
    abow.backend.set_content('page1', '')
    assert 'page1' not in abow.backend.get_pages_list()


def test_delete(backend_path):
    '''Test page deletion
    '''
    abow.backend.set_content('page1', 'abc')
    abow.backend.delete('page1')
    assert abow.backend.get_content('page1') == ''

    # make sure no exception is raised when deleting a non existing page
    abow.backend.delete('page1')


def test_set_attrs(backend_path):
    ''' test page attributes
    '''
    abow.backend.set_attr('page1', 'attr1', 'abc')
    assert abow.backend.get_attr('page1', 'attr1') == 'abc'

    # force a read from backend
    abow.backend._pages_attrs.clear()
    assert abow.backend.get_attr('page1', 'attr1') == 'abc'

    abow.backend.delete('page1')
    assert abow.backend.get_attr('page1', 'attr1') is None


def test_mtime(backend_path):
    ''' test backend mtime
    '''
    cur_time = int(time.time())
    abow.backend.set_content('page1', 'abc')
    assert abow.backend.get_mtime() >= cur_time
    assert abow.backend.get_mtime('page1') >= cur_time


def test_search(backend_path):
    '''test page search
    '''
    abow.backend.set_content('page1', 'abc')
    abow.backend.set_content('page2', 'abcd')

    assert abow.backend.search_pages('abc') == ['page1', 'page2']
    assert abow.backend.search_pages('d') == ['page2']
    assert abow.backend.search_pages('e') == []


def test_set_content_error(invalid_backend_path):
    '''check that an alert is raised if the content cannot be written or read
    '''
    abow.alerts.clear()
    abow.backend.set_content('page1', 'abc')
    assert len(abow.alerts.get_list()) == 1
    assert abow.backend.get_content('page1') == ''
    assert len(abow.alerts.get_list()) == 2


def test_set_attr_error(invalid_backend_path):
    '''check alerts when trying to access attribute
    '''
    abow.alerts.clear()
    # force a read from backend
    abow.backend._pages_attrs.clear()
    assert abow.backend.get_attr('page1', 'attr1') is None
    abow.backend.set_attr('page1', 'attr1', 'abc')
    assert len(abow.alerts.get_list()) == 2


def test_delete_error(invalid_backend_path):
    '''check that an alert is raised if the page cannot be deleted
    '''
    abow.alerts.clear()
    abow.backend.delete('page1')
    assert len(abow.alerts.get_list()) == 2


def test_list_error(invalid_backend_path):
    '''test pages list when the backend is invalid
    '''
    assert abow.backend.get_pages_list() == []
    assert abow.backend.get_mtime() == abow.backend._ref_mtime
