import textwrap
import abow


def test_empty():
    '''test empty string
    '''
    assert abow.render.render('') == {'html': '', 'toc': ''}


def test_text():
    '''make sure text is rendered
    Note: we are not testing markdown here
    '''
    text = 'abc'
    result = abow.render.render(text)
    assert text in result['html']
    assert result['toc'] != ''


def test_wikilinks():
    '''test the wikilinks extension
    '''
    # normal wiki link
    result = abow.render.render('[[label|target]]')
    assert result['html'] == \
        '<p><a class="wikilink text-danger" href="../view/target">label</a></p>'

    # action link
    result = abow.render.render('[[label|action:edit/target]]')
    assert result['html'] == '<p><a class="wikilink" href="../edit/target">label</a></p>'

    # invalid action link
    result = abow.render.render('[[action:]]')
    assert result['html'] == '<p></p>'

    # anchor link
    result = abow.render.render('[[#abc]]')
    assert result['html'] == '<p><a class="wikilink" href="#abc">#abc</a></p>'


def test_table():
    '''test the tables extension
    '''
    result = abow.render.render('| a | b |\n|---|---|\n| c | d |')
    expected = '''\
        <div class="table-responsive">
        <table class="table table-bordered">
        <thead class="thead-light">
        <tr>
        <th>a</th>
        <th>b</th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <td>c</td>
        <td>d</td>
        </tr>
        </tbody>
        </table>
        </div>'''
    assert result['html'] == textwrap.dedent(expected)
