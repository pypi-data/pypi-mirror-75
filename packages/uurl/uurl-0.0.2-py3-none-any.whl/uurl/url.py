"""The module provides API for Unified Resource Locator (URL) endpoints."""
from punish import AbstractStyle, abstractstyle
from uurl.host import Host
from uurl.path import EmptyPath, Path
from uurl.protocol import HttpProtocol, HttpsProtocol, Protocol
from uurl.port import Port


class Address(AbstractStyle):
    """The class represents an interface of an address."""

    @abstractstyle
    def matcher(self) -> str:
        """Returns a path of the URL."""
        pass

    @abstractstyle
    def host(self, with_port: bool = False) -> str:
        """Returns a domain name (host).

        Args:
            with_port (bool): host with port
        """
        pass

    @abstractstyle
    def protocol(self) -> Protocol:
        """Returns a protocol of the URL."""
        pass

    @abstractstyle
    def port(self) -> Port:
        """Returns a port of the URL."""
        pass

    @abstractstyle
    def __str__(self) -> str:
        """Returns address as a string."""
        pass


class Url(Address):
    """The class represents regular WEB URL item."""

    def __init__(self, host: Host, protocol: Protocol, path: Path = EmptyPath()) -> None:
        self._host = host
        self._path = path
        self._protocol = protocol

    def matcher(self) -> str:
        """Returns a path of the URL."""
        return str(self._path)

    def host(self, with_port: bool = False) -> str:
        """Returns a domain name (host).

        Args:
            with_port (bool): host with port
        """
        if with_port:
            return self._host.value_with_port(self._protocol.port())
        return self._host.value()

    def protocol(self) -> Protocol:
        """Returns a protocol of the URL."""
        return self._protocol

    def port(self) -> Port:
        """Returns a port of the URL."""
        return self._protocol.port()

    def __str__(self) -> str:
        """Returns address as a string."""
        if self._host.begin_with_protocol(self._protocol):
            return self.host(with_port=True)
        return f'{self._protocol.value()}://{self._host.value_with_port(self.port())}/{self._path}'


class HttpUrl(Address):
    """The class represents HTTP WEB URL item."""

    def __init__(self, host: Host, path: Path = EmptyPath()) -> None:
        self._http: Url = Url(host, protocol=HttpProtocol(), path=path)

    def matcher(self) -> str:
        """Returns a path of the HTTP URL."""
        return self._http.matcher()

    def host(self, with_port: bool = False) -> str:
        """Returns a domain name (host).

        Args:
            with_port (bool): host with port
        """
        return self._http.host(with_port)

    def protocol(self) -> Protocol:
        """Returns a protocol of the URL."""
        return self._http.protocol()

    def port(self) -> Port:
        """Returns a port of the URL."""
        return self._http.port()

    def __str__(self) -> str:
        """Returns address as a string."""
        return str(self._http)


class HttpsUrl(Address):
    """The class represents HTTPS WEB URL item."""

    def __init__(self, host: Host, path: Path = EmptyPath()) -> None:
        self._https: Url = Url(host, protocol=HttpsProtocol(), path=path)

    def matcher(self) -> str:
        """Returns a path of the HTTPS URL."""
        return self._https.matcher()

    def host(self, with_port: bool = False) -> str:
        """Returns a domain name (host).

        Args:
            with_port (bool): host with port
        """
        return self._https.host(with_port)

    def protocol(self) -> Protocol:
        """Returns a protocol of the URL."""
        return self._https.protocol()

    def port(self) -> Port:
        """Returns a port of the URL."""
        return self._https.port()

    def __str__(self) -> str:
        """Returns address as a string."""
        return str(self._https)
