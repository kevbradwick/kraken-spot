from unittest.mock import patch

from kraken_spot.client import Client
from kraken_spot.errors import AuthError


class TestPrivateEndpoints:
    def setup_class(self):
        # randomised api key and secret!!!
        self.client = Client(
            api_key="I1IIIcw+WHHHHaHH2NXnTQaaHIOT1a/Gz+aa8aa4CaaMXUzP43DQHHH8",
            private_key="YYNDDLLL+PTEE6EJE2HEEERN8sQUwl2J2CQ/YEREUVVaa3W8aaBEE6xF3DUoFnwjMHDfbOEoB00ERREAXEE1EQ==",
        )

    def test_api_keys_must_be_set(self):
        client = Client()
        try:
            client.get_account_balance()
            assert False
        except AuthError:
            assert True

    @patch("kraken_spot.private.http_post")
    def test_base_url_is_correct(self, post_mock):
        self.client.get_account_balance()
        assert post_mock.call_args[0][0] == "https://api.kraken.com/0/private/Balance"

    @patch("kraken_spot.private.http_post")
    def test_nonce_is_added_to_every_request(self, post_mock):
        self.client.get_account_balance()
        assert "nonce" in post_mock.call_args[0][1]

    @patch("kraken_spot.private.http_post")
    def test_correct_headers_for_every_request(self, post_mock):
        self.client.get_account_balance()
        headers = post_mock.call_args[0][2]

        assert "application/x-www-form-urlencoded" == headers["Content-Type"]
        assert self.client.api_key == headers["API-Key"]
        assert "API-Sign" in headers

    @patch("kraken_spot.private.http_post")
    def test_get_trade_balance(self, post_mock):
        asset = "BTC"
        self.client.get_trade_balance(asset)

        assert asset == post_mock.call_args[0][1]["asset"]
