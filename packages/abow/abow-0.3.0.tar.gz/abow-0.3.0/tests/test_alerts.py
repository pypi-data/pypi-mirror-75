import abow


def test_init():
    '''No alert at startup
    '''
    assert abow.alerts.get_list() == []


def test_add():
    '''add some alerts
    '''
    abow.alerts.add('info', '1')
    abow.alerts.add('danger', '2')
    assert abow.alerts.get_list() == [('info', '1'), ('danger', '2')]


def test_clear():
    '''clear alerts
    '''
    abow.alerts.clear()
    assert abow.alerts.get_list() == []
