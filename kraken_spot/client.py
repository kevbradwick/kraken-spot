from dataclasses import dataclass
from typing import Optional

from .private import PrivateEndpoints
from .public import PublicEndpoints


@dataclass
class Client(PublicEndpoints, PrivateEndpoints):
    api_key: Optional[str] = None
    private_key: Optional[str] = None
    endpoint: str = "https://api.kraken.com"
    api_version: int = 0

    def _base_url(self) -> str:
        return f"{self.endpoint}/{self.api_version}"
