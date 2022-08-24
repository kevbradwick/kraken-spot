from typing import Dict, Optional

from .auth import generate_nonce, get_kraken_signature
from .errors import AuthError
from .http import KrakenResponse, http_post


class PrivateEndpoints:
    """
    PrivateEndpoints is a mixin to be used on the Client class
    """

    def _authorised_query(
        self, url_path: str, body: Optional[Dict] = None
    ) -> KrakenResponse:
        """
        Makes a request to an endpoint that requires API Key authorisation
        """
        api_key = self.api_key  # type: ignore
        private_key = self.private_key  # type: ignore
        api_version = self.api_version  # type: ignore
        endpoint = self.endpoint  # type: ignore

        if not api_key or not private_key:
            raise AuthError(
                (
                    "you must configure the client with an api key and private key' \
                'to access private endpoints"
                )
            )

        full_url_path = f"/{api_version}/private/{url_path}"
        default_data = {"nonce": generate_nonce()}
        body = body or {}
        body = {**body, **default_data}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "API-Key": api_key,
            "API-Sign": get_kraken_signature(full_url_path, body, private_key),
        }
        url = f"{endpoint}{full_url_path}"
        resp = http_post(url, body, headers)
        return KrakenResponse(resp.body.get("result", {}), resp.body.get("error", {}))

    def account_balance(self) -> KrakenResponse:
        """
        Get all cash balances
        """
        return self._authorised_query("Balance")

    def trade_balance(self, asset: str) -> KrakenResponse:
        """
        Retrieve a summary of collateral balances, margin position valuations, equity and
        margin level.
        """
        return self._authorised_query("TradeBalance", {"asset": asset})
