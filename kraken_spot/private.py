from typing import Dict, Optional

from .auth import generate_nonce, get_kraken_signature
from .errors import AuthError
from .http import KrakenResponse, clean_params, http_post


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
                    "you must configure the client with an api key and private key "
                    "to access private endpoints"
                )
            )

        full_url_path = f"/{api_version}/private/{url_path}"
        default_data = {"nonce": generate_nonce()}
        body = body or {}
        body = clean_params({**body, **default_data})
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "API-Key": api_key,
            "API-Sign": get_kraken_signature(full_url_path, body, private_key),
        }
        url = f"{endpoint}{full_url_path}"
        resp = http_post(url, body, headers)
        return KrakenResponse(resp.body.get("result", {}), resp.body.get("error", {}))

    def get_account_balance(self) -> KrakenResponse:
        """
        Get all cash balances
        """
        return self._authorised_query("Balance")

    def get_trade_balance(self, asset: str) -> KrakenResponse:
        """
        Retrieve a summary of collateral balances, margin position valuations, equity and
        margin level.
        """
        return self._authorised_query("TradeBalance", {"asset": asset})

    def get_open_orders(
        self, trades: Optional[bool] = None, user_ref: Optional[int] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getOpenOrders
        """
        return self._authorised_query(
            "OpenOrders", {"trades": trades, "userref": user_ref}
        )

    def get_closed_orders(
        self,
        trades: Optional[bool] = None,
        user_ref: Optional[int] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
        ofs: Optional[int] = None,
        close_time: Optional[str] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getClosedOrders
        """
        return self._authorised_query(
            "ClosedOrders",
            {
                "trades": trades,
                "userref": user_ref,
                "start": start,
                "end": end,
                "ofs": ofs,
                "closetime": close_time,
            },
        )

    def query_orders_info(
        self, tx_id: str, trades: Optional[bool] = None, user_ref: Optional[int] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getOrdersInfo
        """
        return self._authorised_query(
            "QueryOrders",
            {
                "trades": trades,
                "userref": user_ref,
                "txid": tx_id,
            },
        )

    def get_trades_history(
        self,
        trade_type: Optional[str] = None,
        trades: Optional[bool] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
        ofs: Optional[int] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getTradeHistory
        """
        return self._authorised_query(
            "TradeHistory",
            {
                "type": trade_type,
                "trades": trades,
                "start": start,
                "end": end,
                "ofs": ofs,
            },
        )

    def get_trades_info(
        self, tx_id: Optional[str] = None, trades: Optional[bool] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getTradesInfo
        """
        return self._authorised_query("QueryTrades", {"txid": tx_id, "trades": trades})

    def get_open_trades(
        self,
        tx_id: Optional[str] = None,
        do_calc: Optional[bool] = None,
        consolidation: Optional[str] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getOpenPositions
        """
        return self._authorised_query(
            "OpenPositions",
            {
                "txid": tx_id,
                "docalcs": do_calc,
                "consolidation": consolidation,
            },
        )

    def get_ledgers(
        self,
        asset: Optional[str] = None,
        a_class: Optional[str] = None,
        type: Optional[str] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
        ofs: Optional[int] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getLedgers
        """
        return self._authorised_query(
            "Ledgers",
            {
                "asset": asset,
                "aclass": a_class,
                "type": type,
                "start": start,
                "end": end,
                "ofs": ofs,
            },
        )

    def query_ledgers(
        self, ledger_id: Optional[str] = None, trades: Optional[bool] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getLedgersInfo
        """
        return self._authorised_query(
            "QueryLedgers",
            {
                "id": ledger_id,
                "trades": trades,
            },
        )

    def get_trade_volume(
        self, pair: Optional[str] = None, fee_info: Optional[bool] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getTradeVolume
        @todo check 'pair' query parameter - seems to shadow body parameter
        """
        return self._authorised_query(
            "TradeVolume",
            {
                "pair": pair,
                "fee-info": fee_info,
            },
        )

    def request_export_report(
        self,
        report: str,
        description: str,
        format: Optional[str] = None,
        fields: Optional[str] = None,
        start_tm: Optional[int] = None,
        end_tm: Optional[int] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/addExport
        """
        return self._authorised_query(
            "AddExport",
            {
                "report": report,
                "description": description,
                "format": format,
                "fields": fields,
                "starttm": start_tm,
                "endtm": end_tm,
            },
        )

    def get_export_status(self, report: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/exportStatus
        """
        return self._authorised_query("ExportStatus", {"report": report})

    def retrieve_data_export(self, report_id: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/retrieveExport
        """
        return self._authorised_query("RetrieveExport", {"id": report_id})

    def delete_export_report(self, report_id: str, type: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/removeExport
        """
        return self._authorised_query("RemoveExport", {"id": report_id, "type": type})
