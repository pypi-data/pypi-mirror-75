"""Module contains a set of API to manipulate with network protocols."""
from punish import AbstractStyle, abstractstyle
from uurl.port import FtpPort, HttpPort, HttpsPort, Port, SftpPort, SnmpPort


class Protocol(AbstractStyle):
    """Represents an abstraction of protocol."""

    @abstractstyle
    def value(self) -> str:
        """Returns value of a protocol."""
        pass

    @abstractstyle
    def port(self) -> Port:
        """Returns port of protocol."""
        pass

    @abstractstyle
    def __str__(self) -> str:
        """Returns string representation of a protocol."""
        pass


class NetworkProtocol(Protocol):
    """Represents network protocol."""

    def __init__(self, protocol: str, port: Port) -> None:
        self._protocol = protocol
        self._port = port

    def value(self) -> str:
        """Returns value of an application protocol."""
        return self._protocol

    def port(self) -> Port:
        """Returns port of protocol."""
        return self._port

    def __str__(self) -> str:
        """Returns string representation of an application protocol."""
        return f'{self._protocol}:{self._port.value()}'


class HttpProtocol(Protocol):
    """Represents HTTP protocol."""

    def __init__(self) -> None:
        self._http: Protocol = NetworkProtocol(protocol='http', port=HttpPort())

    def value(self) -> str:
        """Returns value of HTTP protocol."""
        return self._http.value()

    def port(self) -> Port:
        """Returns port of HTTP protocol."""
        return self._http.port()

    def __str__(self) -> str:
        """Returns value of HTTP protocol."""
        return str(self._http)


class HttpsProtocol(Protocol):
    """Represents HTTPS protocol."""

    def __init__(self) -> None:
        self._https: Protocol = NetworkProtocol(protocol='https', port=HttpsPort())

    def value(self) -> str:
        """Returns value of HTTPS protocol."""
        return self._https.value()

    def port(self) -> Port:
        """Returns port of HTTPS protocol."""
        return self._https.port()

    def __str__(self) -> str:
        """Returns value of HTTPS protocol."""
        return str(self._https)


class FtpProtocol(Protocol):
    """Represents FTP protocol."""

    def __init__(self) -> None:
        self._ftp: Protocol = NetworkProtocol(protocol='ftp', port=FtpPort())

    def value(self) -> str:
        """Returns value of FTP protocol."""
        return self._ftp.value()

    def port(self) -> Port:
        """Returns port of FTP protocol."""
        return self._ftp.port()

    def __str__(self) -> str:
        """Returns value of FTP protocol."""
        return str(self._ftp)


class SftpProtocol(Protocol):
    """Represents SFTP protocol."""

    def __init__(self) -> None:
        self._sftp: Protocol = NetworkProtocol(protocol='sftp', port=SftpPort())

    def value(self) -> str:
        """Returns value of SFTP protocol."""
        return self._sftp.value()

    def port(self) -> Port:
        """Returns port of SFTP protocol."""
        return self._sftp.port()

    def __str__(self) -> str:
        """Returns value of SFTP protocol."""
        return str(self._sftp)


class SnmpProtocol(Protocol):
    """Represents SNMP protocol."""

    def __init__(self) -> None:
        self._snmp: Protocol = NetworkProtocol(protocol='snmp', port=SnmpPort())

    def value(self) -> str:
        """Returns value of FTP protocol."""
        return self._snmp.value()

    def port(self) -> Port:
        """Returns port of protocol."""
        return self._snmp.port()

    def __str__(self) -> str:
        """Returns value of FTP protocol."""
        return str(self._snmp)
