from unittest.mock import patch

import pytest

from kraken_spot.client import Client
from kraken_spot.http import KrakenResponse


@pytest.mark.integration
class TestPublicEndpointsIntegration:
    def setup_class(self):
        self.client = Client()

    def _assert_success_response(self, response: KrakenResponse):
        assert not response.errors
        assert response.result

    def test_get_server_time(self):
        self._assert_success_response(self.client.get_server_time())

    def test_get_system_status(self):
        self._assert_success_response(self.client.get_system_status())

    def test_get_asset_info(self):
        self._assert_success_response(self.client.get_asset_info("XBT,ETH"))

    def test_get_tradable_asset_pairs(self):
        self._assert_success_response(
            self.client.get_tradable_asset_pairs("XXBTZUSD,XETHXXBT")
        )

    def test_get_ticker_information(self):
        self._assert_success_response(self.client.get_ticker_information("XBTUSD"))

    def test_get_ohlc_data(self):
        self._assert_success_response(self.client.get_ohlc_data("XBTUSD"))

    def test_get_order_book(self):
        self._assert_success_response(self.client.get_order_book("XBTUSD"))

    def test_get_recent_trades(self):
        self._assert_success_response(self.client.get_recent_trades("XBTUSD"))

    def test_get_recent_spreads(self):
        self._assert_success_response(self.client.get_recent_spreads("XBTUSD"))


class TestPublicEndpoints:
    def setup_class(self):
        self.client = Client()

    @patch("kraken_spot.public.http_get")
    def test_get_server_time(self, mock_get):
        self.client.get_server_time()

        assert "https://api.kraken.com/0/public/Time" == mock_get.call_args[0][0]

    @patch("kraken_spot.public.http_get")
    def test_get_system_status(self, mock_get):
        self.client.get_system_status()

        assert (
            "https://api.kraken.com/0/public/SystemStatus" == mock_get.call_args[0][0]
        )

    @patch("kraken_spot.public.http_get")
    def test_get_asset_info(self, mock_get):
        self.client.get_asset_info("BTC", "currency")

        assert "https://api.kraken.com/0/public/Assets" == mock_get.call_args[0][0]
        assert "BTC" == mock_get.call_args[0][1]["asset"]
        assert "currency" == mock_get.call_args[0][1]["aclass"]

    @patch("kraken_spot.public.http_get")
    def test_get_tradable_asset_pairs(self, mock_get):
        self.client.get_tradable_asset_pairs("BTC")

        assert "https://api.kraken.com/0/public/AssetPairs" == mock_get.call_args[0][0]
        assert "BTC" == mock_get.call_args[0][1]["pair"]

    @patch("kraken_spot.public.http_get")
    def test_get_ticker_information(self, mock_get):
        self.client.get_ticker_information("BTC")

        assert "https://api.kraken.com/0/public/Ticker" == mock_get.call_args[0][0]
        assert "BTC" == mock_get.call_args[0][1]["pair"]

    @patch("kraken_spot.public.http_get")
    def test_get_ohlc_data(self, mock_get):
        self.client.get_ohlc_data("BTC")

        assert "https://api.kraken.com/0/public/OHLC" == mock_get.call_args[0][0]
        assert "BTC" == mock_get.call_args[0][1]["pair"]

    @patch("kraken_spot.public.http_get")
    def test_get_order_book(self, mock_get):
        self.client.get_order_book("BTC")

        assert "https://api.kraken.com/0/public/Depth" == mock_get.call_args[0][0]
        assert "BTC" == mock_get.call_args[0][1]["pair"]

    @patch("kraken_spot.public.http_get")
    def test_get_recent_trades(self, mock_get):
        self.client.get_recent_trades("BTC")

        assert "https://api.kraken.com/0/public/Trades" == mock_get.call_args[0][0]
        assert "BTC" == mock_get.call_args[0][1]["pair"]

    @patch("kraken_spot.public.http_get")
    def test_get_recent_spreads(self, mock_get):
        self.client.get_recent_spreads("BTC")

        assert "https://api.kraken.com/0/public/Spread" == mock_get.call_args[0][0]
        assert "BTC" == mock_get.call_args[0][1]["pair"]
