"""Package contains a set of interfaces to operate `uurl` application."""
from typing import Tuple
from uurl.url import Address, HttpUrl, HttpsUrl, Url
from uurl.host import Host
from uurl.path import EmptyPath, Path, UrlPath
from uurl.protocol import HttpProtocol, HttpsProtocol, NetworkProtocol, Protocol
from uurl.port import HttpPort, HttpsPort, NetworkPort, Port

__author__: str = 'Volodymyr Yahello'
__email__: str = 'vyahello@gmail.com'
__license__: str = 'MIT'
__copyright__: str = f'Copyright 2020, {__author__}'
__version__: str = '0.0.2'

__all__: Tuple[str, ...] = (
    'Address',
    'Url',
    'HttpUrl',
    'HttpsUrl',
    'Host',
    'EmptyPath',
    'UrlPath',
    'Path',
    'HttpProtocol',
    'HttpsProtocol',
    'NetworkProtocol',
    'Protocol',
    'HttpPort',
    'HttpsPort',
    'NetworkPort',
    'Port',
)
