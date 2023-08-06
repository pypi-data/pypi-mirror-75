"""Module contains a set of API to manipulate with URL paths."""
from typing import Sequence, Union
from punish import AbstractStyle, abstractstyle


class Path(AbstractStyle):
    """Represents an abstract path."""

    @abstractstyle
    def __len__(self) -> int:
        """Count path endpoints."""
        pass

    @abstractstyle
    def __str__(self) -> str:
        """Assemble a path."""
        pass

    @abstractstyle
    def __getitem__(self, index: int) -> Union[str, Sequence[str]]:
        """Returns path item(s).

        Args:
            index (int): an index.
        """
        pass


class UrlPath(Path):
    """Represents path endpoint."""

    def __init__(self, *path: str) -> None:
        self._path: Sequence[str] = path

    def __len__(self) -> int:
        """Count path endpoints."""
        return len(self._path)

    def __str__(self) -> str:
        """Assemble a path."""
        if self._has_forward_slash():
            return '/'.join(map(str, self._path[1:]))
        return '/'.join(map(str, self._path))

    def _has_forward_slash(self) -> bool:
        """Returns true/false if path starts with slash."""
        return self._path[0].startswith('/')

    def __getitem__(self, index: int) -> Union[str, Sequence[str]]:
        """Returns path item(s).

        Args:
            index (int): an index.
        """
        return self._path[index]


class EmptyPath(Path):
    """Represents empty path endpoint."""

    def __len__(self) -> int:
        """Count path endpoints."""
        return 0

    def __str__(self) -> str:
        """Assemble a path."""
        return ''

    def __getitem__(self, index: int) -> Union[str, Sequence[str]]:
        """Returns path item(s).

        Args:
            index (int): an index.
        """
        return ()
