import pytest

from certifier import Certificate


@pytest.fixture
def certifier():
    return Certificate()


def test_certifier(certifier):
    assert certifier.template_path is None
    assert certifier.destination_path
    with pytest.raises(NotImplementedError):
        certifier.get_meta()
    with pytest.raises(NotImplementedError):
        certifier.get_rows()
