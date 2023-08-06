import pytest

from seeq import spy

from .. import _login
from .. import _config
from . import test_common


@pytest.mark.system
def test_bad_login():
    with pytest.raises(RuntimeError):
        spy.login('mark.derbecker@seeq.com', 'DataLab!', url='https://bogus')

    # Remove overrides that resulted from spy.login() with bogus URL
    _config.unset_seeq_url()

    with pytest.raises(ValueError):
        spy.login('mark.derbecker@seeq.com', 'DataLab!', auth_provider='bogus')


@pytest.mark.system
def test_good_login():
    test_common.login()


@pytest.mark.system
def test_credentials_file_with_username():
    with pytest.raises(ValueError):
        spy.login('mark.derbecker@seeq.com', 'DataLab!', credentials_file='credentials.key')
