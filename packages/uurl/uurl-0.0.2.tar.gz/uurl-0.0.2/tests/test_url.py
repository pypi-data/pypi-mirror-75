import pytest
from uurl.host import Host
from uurl.path import Path, UrlPath
from uurl.protocol import HttpProtocol, Protocol
from uurl.url import Address, Url

_host: str = '9.9.9.9'
_path: str = '/api/path'

pytestmark = pytest.mark.unit


@pytest.fixture(scope='module')
def host() -> Host:
    yield Host('example.com')


@pytest.fixture(scope='module')
def http_protocol() -> Protocol:
    yield HttpProtocol()


@pytest.fixture(scope='module')
def url_path() -> Host:
    yield UrlPath('api', 'path')


@pytest.fixture(scope='module')
def leading_slash_url_path() -> Path:
    yield UrlPath('/', 'api', 'path')


@pytest.fixture(scope='module')
def url_with_leading_slash(
    host: Host, http_protocol: Protocol, leading_slash_url_path: Path
) -> Address:
    yield Url(host, protocol=http_protocol, path=leading_slash_url_path)


@pytest.fixture(scope='module')
def url_without_leading_slash(host: Host, http_protocol: Protocol, url_path: Path) -> Address:
    yield Url(host, protocol=http_protocol, path=url_path)


def test_url_with_leading_slash(
    url_with_leading_slash: Address,
    http_protocol: Protocol,
    host: Host,
    leading_slash_url_path: Path,
) -> None:
    assert str(url_with_leading_slash) == (
        f'{http_protocol.value()}://{host.value_with_port(http_protocol.port())}/'
        f'{leading_slash_url_path}'
    )


def test_url_without_leading_slash(
    url_without_leading_slash: Address, http_protocol: Protocol, host: Host, url_path: Path
) -> None:
    assert str(url_without_leading_slash) == (
        f'{http_protocol.value()}://{host.value_with_port(http_protocol.port())}/' f'{url_path}'
    )


def test_matcher(
    url_with_leading_slash: Address,
    http_protocol: Protocol,
    host: Host,
    leading_slash_url_path: Path,
) -> None:
    assert url_with_leading_slash.matcher() == str(leading_slash_url_path)


def test_host(url_with_leading_slash: Address, host: Host, http_protocol: Protocol) -> None:
    assert url_with_leading_slash.host(with_port=True) == host.value_with_port(http_protocol.port())


def test_protocol(url_with_leading_slash: Address, http_protocol: Protocol) -> None:
    assert isinstance(url_with_leading_slash.protocol(), HttpProtocol)


def test_port(url_with_leading_slash: Address, http_protocol: Protocol) -> None:
    assert isinstance(url_with_leading_slash.port(), http_protocol.port().__class__)
