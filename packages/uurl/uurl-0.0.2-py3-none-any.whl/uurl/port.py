"""Module contains a set of API to manipulate with network ports."""
from punish import AbstractStyle, abstractstyle


class Port(AbstractStyle):
    """Represents an abstraction of a port."""

    @abstractstyle
    def value(self) -> int:
        """Returns value of a port."""
        pass

    @abstractstyle
    def has_udp(self) -> bool:
        """Described UDP protocol is standardized, specified or widely used for the port number."""
        pass

    @abstractstyle
    def has_tcp(self) -> bool:
        """Described TCP protocol is standardized, specified or widely used for the port number."""
        pass

    @abstractstyle
    def __str__(self) -> str:
        """Returns string representation of a port."""
        pass


class NetworkPort(Port):
    """Represents network port."""

    def __init__(self, port: int, has_upd: bool, has_tcp: bool) -> None:
        self._port = port
        self._has_udp = has_upd
        self._has_tcp = has_tcp

    def value(self) -> int:
        """Returns value of a network port."""
        return self._port

    def has_udp(self) -> bool:
        """Supported by UPD protocol."""
        return self._has_udp

    def has_tcp(self) -> bool:
        """Supported by TCP protocol."""
        return self._has_tcp

    def __str__(self) -> str:
        """Returns string representation of a network port."""
        return f'{self._port} port; Has UDP = {self._has_udp}; Has TCP = {self._has_tcp}'


class HttpPort(Port):
    """Represents HTTP port."""

    def __init__(self) -> None:
        self._http: Port = NetworkPort(port=80, has_upd=True, has_tcp=False)

    def value(self) -> int:
        """Returns value of HTTP port."""
        return self._http.value()

    def has_udp(self) -> bool:
        """Supported by UPD protocol."""
        return self._http.has_udp()

    def has_tcp(self) -> bool:
        """Supported by TCP protocol."""
        return self._http.has_tcp()

    def __str__(self) -> str:
        """Returns value of HTTP port."""
        return str(self._http)


class HttpsPort(Port):
    """Represents HTTPS port."""

    def __init__(self) -> None:
        self._https: Port = NetworkPort(port=443, has_upd=True, has_tcp=True)

    def value(self) -> int:
        """Returns value of HTTPS port."""
        return self._https.value()

    def has_udp(self) -> bool:
        """Supported by UPD protocol."""
        return self._https.has_udp()

    def has_tcp(self) -> bool:
        """Supported by TCP protocol."""
        return self._https.has_tcp()

    def __str__(self) -> str:
        """Returns value of HTTPS port."""
        return str(self._https)


class FtpPort(Port):
    """Represents FTP port."""

    def __init__(self) -> None:
        self._ftp: Port = NetworkPort(port=21, has_upd=True, has_tcp=False)

    def value(self) -> int:
        """Returns value of FTP port."""
        return self._ftp.value()

    def has_udp(self) -> bool:
        """Supported by UPD protocol."""
        return self._ftp.has_udp()

    def has_tcp(self) -> bool:
        """Supported by TCP protocol."""
        return self._ftp.has_tcp()

    def __str__(self) -> str:
        """Returns value of FTP port."""
        return str(self._ftp)


class SftpPort(Port):
    """Represents SFTP port."""

    def __init__(self) -> None:
        self._sftp: Port = NetworkPort(port=22, has_upd=True, has_tcp=False)

    def value(self) -> int:
        """Returns value of SFTP port."""
        return self._sftp.value()

    def has_udp(self) -> bool:
        """Supported by UPD protocol."""
        return self._sftp.has_udp()

    def has_tcp(self) -> bool:
        """Supported by TCP protocol."""
        return self._sftp.has_tcp()

    def __str__(self) -> str:
        """Returns value of SFTP port."""
        return str(self._sftp)


class SnmpPort(Port):
    """Represents SNMP port."""

    def __init__(self) -> None:
        self._snmp: Port = NetworkPort(port=161, has_upd=False, has_tcp=True)

    def value(self) -> int:
        """Returns value of SNMP port."""
        return self._snmp.value()

    def has_udp(self) -> bool:
        """Supported by UPD protocol."""
        return self._snmp.has_udp()

    def has_tcp(self) -> bool:
        """Supported by TCP protocol."""
        return self._snmp.has_tcp()

    def __str__(self) -> str:
        """Returns value of SNMP port."""
        return str(self._snmp)
