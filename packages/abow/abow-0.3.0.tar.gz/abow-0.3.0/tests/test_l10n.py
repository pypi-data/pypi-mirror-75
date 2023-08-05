import locale
import abow


def mock_cfg_valid(key):
    '''return a valid locale value
    '''
    return 'fr_FR.UTF-8'


def mock_cfg_invalid(key):
    '''return an invalid locale value
    '''
    return 'abcdef'


def test_deferred_gettext():
    '''test deferred gettext
    '''
    assert abow.l10n.deferred_gettext('abc') == 'abc'


def test_init(monkeypatch):
    '''test l10n initialisation and get_lang
    '''
    monkeypatch.setattr(abow.config, 'get', mock_cfg_valid)
    abow.l10n.init()
    assert abow.l10n.get_lang() == 'fr-FR'

    monkeypatch.setattr(abow.config, 'get', mock_cfg_invalid)
    abow.alerts.clear()
    abow.l10n.init()
    assert len(abow.alerts.get_list()) == 1


def test_get_lang():
    '''test get_lang with C locale
    '''
    cur_locale = locale.setlocale(locale.LC_ALL, 'C')
    assert abow.l10n.get_lang() == 'en'
    locale.setlocale(locale.LC_ALL, cur_locale)
