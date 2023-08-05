import pytest
import abow


pytestmark = pytest.mark.usefixtures('backend_path')


@pytest.fixture(scope="module")
def create_pages():
    '''pages must exist to search for tags
    '''
    abow.backend.set_content('page1', 'abc')
    abow.backend.set_content('page2', 'abc')


def test_set_tag():
    '''test setting and getting tags
    '''
    assert abow.tags.get_tags('page1') == []
    abow.tags.set_tags('page1', [])
    assert abow.tags.get_tags('page1') == []

    abow.tags.set_tags('page1', ['b', 'b', 'a'])
    assert abow.tags.get_tags('page1') == ['b', 'a']

    abow.tags.set_tags('page1', 'abc, def; gh, i j k , ; ,zzz  ')
    assert abow.tags.get_tags('page1') == ['abc', 'def', 'gh', 'i j k', 'zzz']

    with pytest.raises(TypeError):
        abow.tags.set_tags('page1', 0)


def test_search(create_pages):
    '''test searching by tag
    '''
    abow.tags.set_tags('page1', ['a', 'b'])
    abow.tags.set_tags('page2', ['a', 'c'])

    assert abow.tags.search('a') == ['page1', 'page2']
    assert abow.tags.search('b') == ['page1']
    assert abow.tags.search('c') == ['page2']
    assert abow.tags.search('d') == []


def test_get_all_tags(create_pages):
    '''test retreiving all the tags
    '''
    abow.tags.set_tags('page1', ['a', 'b'])
    abow.tags.set_tags('page2', ['a', 'c'])

    assert abow.tags.get_all_tags() == ['a', 'b', 'c']
