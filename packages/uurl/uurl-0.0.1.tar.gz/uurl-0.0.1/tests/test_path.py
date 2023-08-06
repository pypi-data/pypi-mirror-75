import pytest
from uurl.path import EmptyPath, Path, UrlPath

pytestmark = pytest.mark.unit


@pytest.fixture()
def url_path() -> Path:
    yield UrlPath('path', 'to', 'place')


@pytest.fixture()
def empty_path() -> Path:
    yield EmptyPath()


def test_count_url_path(url_path: Path) -> None:
    assert len(url_path) == 3


def test_assemble_url_path(url_path: Path) -> None:
    assert str(url_path) == 'path/to/place'


def test_path_to_sequence(url_path: Path) -> None:
    assert tuple(url_path) == ('path', 'to', 'place')


def test_url_has_forward_slash(url_path: UrlPath) -> None:
    assert not url_path._has_forward_slash()


def test_count_empty_path(empty_path: Path) -> None:
    assert not len(empty_path)


def test_assemble_empty_path(empty_path: Path) -> None:
    assert str(empty_path) == ''
