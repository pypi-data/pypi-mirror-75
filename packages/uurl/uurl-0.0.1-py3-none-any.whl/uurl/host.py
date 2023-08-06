"""Module contains a set of API to manipulate with network hosts."""
from uurl.port import Port
from uurl.protocol import Protocol


class Host:
    """Represents network host."""

    def __init__(self, host: str) -> None:
        self._host = host

    def value(self) -> str:
        """Returns a network host."""
        return self._host

    def value_with_port(self, port: Port) -> str:
        """Returns a network host with port.

        Args:
            port (Port): a port
        """
        return f'{self._host}:{port.value()}'

    def begin_with_protocol(self, protocol: Protocol) -> bool:
        """Returns true of host contains a protocol otherwise false.

        Args:
            protocol (Protocol): a protocol
        """
        return self._host.startswith(protocol.value())
