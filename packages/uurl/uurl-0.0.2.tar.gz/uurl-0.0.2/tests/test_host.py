import pytest
from uurl.host import Host
from uurl.port import HttpPort, Port
from uurl.protocol import HttpProtocol, HttpsProtocol, Protocol

pytestmark = pytest.mark.unit

_host: str = 'example.com'
_http_host: str = f'http://{_host}'
_https_host: str = f'https://{_host}'


@pytest.fixture()
def host() -> Host:
    yield Host(_host)


@pytest.fixture()
def port() -> Port:
    yield HttpPort()


def test_host_value(host: Host) -> None:
    assert host.value() == _host


def test_host_value_with_port(host: Host, port: Port) -> None:
    assert host.value_with_port(port) == f'{_host}:{port.value()}'


@pytest.mark.parametrize(
    'host_input, protocol, outcome',
    (
        pytest.param(Host(_http_host), HttpProtocol(), True, id='http'),
        pytest.param(Host(_https_host), HttpsProtocol(), True, id='https'),
        pytest.param(Host(_host), HttpProtocol(), False, id='no protocol'),
    ),
)
def test_host_begin_with_protocol(host_input: Host, protocol: Protocol, outcome: bool) -> None:
    assert host_input.begin_with_protocol(protocol) is outcome
