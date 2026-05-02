"""Abstract EmailProvider protocol — swap provider by changing one config value."""

from typing import Protocol


class EmailProvider(Protocol):
    def send(self, to: str, subject: str, html: str, text: str) -> None:
        """Send a single email. Raises on unrecoverable error."""
        ...
