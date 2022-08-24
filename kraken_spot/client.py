from dataclasses import dataclass, field
from typing import Dict, List, Optional

import requests

from .auth import generate_nonce, get_kraken_signature
from .errors import AuthError


@dataclass
class KrakenResponse:
    result: Dict = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


@dataclass
class Client:
    api_key: Optional[str] = None
    private_key: Optional[str] = None
    endpoint: str = "https://api.kraken.com"
    api_version: int = 0

    def _authorised_query(self, url_path: str, body: Optional[Dict] = None):
        """
        Makes a request to an endpoint that requires API Key authorisation
        """
        if not self.api_key or not self.private_key:
            raise AuthError(
                (
                    "you must configure the client with an api key and private key' \
                'to access private endpoints"
                )
            )

        full_url_path = f"/{self.api_version}{url_path}"
        default_data = {"nonce": generate_nonce()}
        body = body or {}
        body = {**body, **default_data}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "API-Key": self.api_key,
            "API-Sign": get_kraken_signature(full_url_path, body, self.private_key),
        }
        url = f"{self.endpoint}/{full_url_path}"
        return requests.post(url, headers=headers, data=body)

    def account_balance(self) -> KrakenResponse:
        """
        Get all cash balances
        """
        r = self._authorised_query("/private/Balance")
        data = r.json()
        return KrakenResponse(
            errors=data.get("error", {}), result=data.get("result", {})
        )

    def trade_balance(self, asset: str) -> KrakenResponse:
        """
        Retrieve a summary of collateral balances, margin position valuations, equity and
        margin level.
        """
        path = "/private/TradeBalance"
        data = self._authorised_query(path, {"asset": asset}).json()
        return KrakenResponse(
            errors=data.get("error", {}), result=data.get("result", {})
        )
