import pytest
import abow


@pytest.fixture(scope='module')
def monkeymodule():
    '''monkey patch with scope module
    '''
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


def setup_backend_path(tmp_path_factory, monkeymodule):
    '''Create a temporary folder to hold the backend,
    and points to it via monkey patching config.

    Can also points to a non-accessible folder for testing error paths
    '''
    path = tmp_path_factory.mktemp('backend')
    cfg = abow.config.get

    def mock_cfg(key, default=None):
        '''override the config to set the temporary backend
        '''
        if key == 'abow.backend_path':
            return str(path)
        else:
            return cfg(key, None)

    monkeymodule.setattr(abow.config, "get", mock_cfg)

    return path


@pytest.fixture(scope="module")
def backend_path(tmp_path_factory, monkeymodule):
    '''usable backend
    '''
    setup_backend_path(tmp_path_factory, monkeymodule)


@pytest.fixture(scope="module")
def invalid_backend_path(tmp_path_factory, monkeymodule):
    '''non-accessible backend
    '''
    path = setup_backend_path(tmp_path_factory, monkeymodule)
    path.chmod(0)
    yield
    path.chmod(0o755)
