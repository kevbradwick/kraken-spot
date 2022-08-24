from typing import Dict, Optional

from .http import KrakenResponse, http_get


class PublicEndpoints:
    def _public_query(
        self, url_path: str, params: Optional[Dict[str, str]] = None
    ) -> KrakenResponse:
        resp = http_get(f"{self._base_url()}/public/{url_path}", params)  # type: ignore
        return KrakenResponse(resp.body.get("result", {}), resp.body.get("error", {}))

    def get_server_time(self) -> KrakenResponse:
        """
        Get's the server time.

        https://docs.kraken.com/rest/#tag/Market-Data/operation/getServerTime
        """
        return self._public_query("Time")

    def get_system_status(self) -> KrakenResponse:
        """
        Get current system status

        https://docs.kraken.com/rest/#tag/Market-Data/operation/getSystemStatus
        """
        return self._public_query("SystemStatus")

    def get_asset_info(
        self, asset: Optional[str] = None, a_class: Optional[str] = None
    ) -> KrakenResponse:
        """
        Get information about an asset

        https://docs.kraken.com/rest/#tag/Market-Data/operation/getAssetInfo
        """
        params = {}
        if asset:
            params["asset"] = asset

        if a_class:
            params["aclass"] = a_class

        return self._public_query("Assets", params)
