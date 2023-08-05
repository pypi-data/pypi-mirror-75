import bottle
import abow


def test_print_file(capsys):
    '''test default configuration generation
    '''
    abow.config.print_file()
    cfg_file = capsys.readouterr().out
    assert '[abow]' in cfg_file


def test_keys():
    '''make sure the expected config keys are here
    '''
    cfg = bottle.ConfigDict()
    abow.config.init(cfg)
    keys = [
        'abow.locale_path',
        'abow.static_path',
        'abow.template_path',
        'abow.backend_path',
        'abow.static_url',
        'abow.locale',
        'abow.welcome_page',
        'abow.help_page',
        ]
    assert len(keys) == len(cfg.keys())
    assert sorted(keys) == sorted(cfg.keys())


def test_load_cfg(monkeypatch, tmp_path):
    '''test configuration load from file
    '''
    # from XDG_CONFIG_HOME
    user_conf_dir = tmp_path / 'abow'
    user_conf_dir.mkdir()
    user_conf_file = user_conf_dir / 'config'
    user_conf_file.write_text('[abow]\nwelcome_page=abc\nhelp_page=def\n')
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path))

    cfg = bottle.ConfigDict()
    abow.config.init(cfg)
    assert abow.config.get('abow.welcome_page') == 'abc'
    assert abow.config.get('abow.help_page') == 'def'

    # from ABOW_CONFIG
    user_conf_file = tmp_path / 'abow.ini'
    user_conf_file.write_text('[abow]\nwelcome_page=xyz\n')
    monkeypatch.setenv('ABOW_CONFIG', str(user_conf_file))

    cfg = bottle.ConfigDict()
    abow.config.init(cfg)
    assert abow.config.get('abow.welcome_page') == 'xyz'
    assert abow.config.get('abow.help_page') == 'def'
