from typing import Any, List
from unittest.mock import patch

from kraken_spot.client import Client
from kraken_spot.errors import AuthError


def _assert_operation(post_mock, operation):
    assert post_mock.call_args[0][0].endswith(operation)


def _assert_body_params_absent(post_mock, param_names: List[str]):
    for name in param_names:
        assert name not in post_mock.call_args[0][1]


def _assert_body_param(post_mock, name: str, value: Any):
    assert post_mock.call_args[0][1][name] == value


def _assert_body_params_present(post_mock, param_names: List[str]):
    for name in param_names:
        assert name in post_mock.call_args[0][1]


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
    def test_otp_is_sent_and_code_is_reset(self, post_mock):
        """
        A OTP is set once, used on the next request and then removed afterwards
        """
        self.client.get_account_balance()
        _assert_body_params_absent(post_mock, ["otp"])

        self.client.set_otp(1234)
        self.client.get_account_balance()
        _assert_body_param(post_mock, "otp", "1234")

        # should now be reset
        self.client.get_account_balance()
        _assert_body_params_absent(post_mock, ["otp"])

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

        _assert_operation(post_mock, "TradeBalance")
        assert asset == post_mock.call_args[0][1]["asset"]

    @patch("kraken_spot.private.http_post")
    def test_get_open_orders(self, post_mock):
        # with defaults
        self.client.get_open_orders()
        _assert_operation(post_mock, "OpenOrders")
        _assert_body_params_absent(post_mock, ["trades", "userref"])
        _assert_body_params_present(post_mock, ["nonce"])

        # with params
        self.client.get_open_orders(trades=True, user_ref=123)
        _assert_body_params_present(post_mock, ["trades", "userref", "nonce"])

    @patch("kraken_spot.private.http_post")
    def test_get_closed_orders(self, post_mock):
        # with defaults
        self.client.get_closed_orders()
        _assert_operation(post_mock, "ClosedOrders")
        _assert_body_params_absent(
            post_mock, ["trades", "userref", "start", "end", "ofs", "closetime"]
        )
        _assert_body_params_present(post_mock, ["nonce"])

        # with params
        self.client.get_closed_orders(
            trades=True, user_ref=123, start=1, end=1, ofs=1, close_time="1"
        )
        _assert_body_params_present(
            post_mock,
            ["trades", "userref", "start", "end", "ofs", "closetime", "nonce"],
        )

    @patch("kraken_spot.private.http_post")
    def test_query_orders_info(self, post_mock):
        # with defaults
        self.client.query_orders_info(tx_id="123")
        _assert_operation(post_mock, "QueryOrders")
        _assert_body_params_absent(post_mock, ["trades", "userref"])
        _assert_body_params_present(post_mock, ["nonce", "txid"])

        # with params
        self.client.query_orders_info(tx_id="123", trades=True, user_ref=12)
        _assert_body_params_present(
            post_mock,
            ["trades", "userref", "txid", "nonce"],
        )

    @patch("kraken_spot.private.http_post")
    def test_get_trades_history(self, post_mock):
        # with defaults
        self.client.get_trades_history()
        _assert_operation(post_mock, "TradeHistory")
        _assert_body_params_absent(post_mock, ["trades", "type", "start", "end", "ofs"])
        _assert_body_params_present(post_mock, ["nonce"])

        # with params
        self.client.get_trades_history(
            trade_type="sd", trades=True, start=1, end=1, ofs=1
        )
        _assert_body_params_present(
            post_mock,
            ["trades", "nonce", "type", "start", "end", "ofs"],
        )

    @patch("kraken_spot.private.http_post")
    def test_get_trades_info(self, post_mock):
        # with defaults
        self.client.get_trades_info()
        _assert_operation(post_mock, "QueryTrades")
        _assert_body_params_absent(post_mock, ["trades", "txid"])
        _assert_body_params_present(post_mock, ["nonce"])

        # with params
        self.client.get_trades_info(tx_id="sd", trades=True)
        _assert_body_params_present(
            post_mock,
            ["trades", "nonce", "txid"],
        )

    @patch("kraken_spot.private.http_post")
    def test_get_open_trades(self, post_mock):
        # with defaults
        self.client.get_open_trades()
        _assert_operation(post_mock, "OpenPositions")
        _assert_body_params_absent(post_mock, ["consolidation", "txid", "docalcs"])
        _assert_body_params_present(post_mock, ["nonce"])

        # with params
        self.client.get_open_trades(tx_id="sd", consolidation="1", do_calc=True)
        _assert_body_params_present(
            post_mock,
            ["consolidation", "nonce", "txid", "docalcs"],
        )

    @patch("kraken_spot.private.http_post")
    def test_get_ledgers(self, post_mock):
        # with defaults
        self.client.get_ledgers()
        _assert_operation(post_mock, "Ledgers")
        _assert_body_params_absent(
            post_mock, ["asset", "aclass", "type", "start", "end", "ofs"]
        )
        _assert_body_params_present(post_mock, ["nonce"])

        # with params
        self.client.get_ledgers(asset="", a_class="", type="", start=1, end=1, ofs=1)
        _assert_body_params_present(
            post_mock,
            ["asset", "aclass", "type", "start", "end", "ofs", "nonce"],
        )

    @patch("kraken_spot.private.http_post")
    def test_query_ledgers(self, post_mock):
        # with defaults
        self.client.query_ledgers()
        _assert_operation(post_mock, "QueryLedgers")
        _assert_body_params_absent(post_mock, ["id", "trades"])
        _assert_body_params_present(post_mock, ["nonce"])

        # with params
        self.client.query_ledgers(ledger_id="", trades=False)
        _assert_body_params_present(
            post_mock,
            ["nonce", "id", "trades"],
        )

    @patch("kraken_spot.private.http_post")
    def test_get_trade_volume(self, post_mock):
        # with defaults
        self.client.get_trade_volume()
        _assert_operation(post_mock, "TradeVolume")
        _assert_body_params_absent(post_mock, ["pair", "fee-info"])
        _assert_body_params_present(post_mock, ["nonce"])

        # with params
        self.client.get_trade_volume(pair="", fee_info=True)
        _assert_body_params_present(
            post_mock,
            ["nonce", "pair", "fee-info"],
        )

    @patch("kraken_spot.private.http_post")
    def test_request_export_report(self, post_mock):
        # with defaults
        self.client.request_export_report(report="", description="")
        _assert_operation(post_mock, "AddExport")
        _assert_body_params_absent(post_mock, ["format", "fields", "starttm", "endtm"])
        _assert_body_params_present(post_mock, ["nonce", "report", "description"])

        # with params
        self.client.request_export_report(
            report="", description="", format="", fields="", start_tm=1, end_tm=1
        )
        _assert_body_params_present(
            post_mock,
            ["nonce", "report", "description", "format", "fields", "starttm", "endtm"],
        )

    @patch("kraken_spot.private.http_post")
    def test_get_export_status(self, post_mock):
        # with defaults
        self.client.get_export_status(report="")
        _assert_operation(post_mock, "ExportStatus")
        _assert_body_params_present(post_mock, ["nonce", "report"])

    @patch("kraken_spot.private.http_post")
    def test_retrieve_data_export(self, post_mock):
        # with defaults
        self.client.retrieve_data_export(report_id="")
        _assert_operation(post_mock, "RetrieveExport")
        _assert_body_params_present(post_mock, ["nonce", "id"])

    @patch("kraken_spot.private.http_post")
    def test_delete_export_report(self, post_mock):
        # with defaults
        self.client.delete_export_report(report_id="", report_type="")
        _assert_operation(post_mock, "RemoveExport")
        _assert_body_params_present(post_mock, ["nonce", "id", "type"])

    # - User Trading

    @patch("kraken_spot.private.http_post")
    def test_add_order(self, post_mock):
        self.client.add_order(order_type="", direction="", volume="", pair="")
        _assert_operation(post_mock, "AddOrder")
        _assert_body_params_present(
            post_mock, ["ordertype", "type", "volume", "pair", "nonce"]
        )
        _assert_body_params_absent(
            post_mock,
            [
                "userref",
                "price",
                "price2",
                "trigger",
                "leverage",
                "stp_type",
                "oflags",
                "timeinforce",
                "starttm",
                "expiretm",
                "close[ordertype]",
                "close[price]",
                "close[price2]",
                "deadline",
                "validate",
            ],
        )

        self.client.add_order(
            order_type="",
            direction="",
            volume="",
            pair="",
            user_ref="",
            price_1="",
            price_2="",
            trigger="",
            leverage="",
            stp_type="",
            o_flags="",
            time_in_force="",
            start_time="",
            expire_time="",
            close_order_type="",
            close_price="",
            close_price_2="",
            deadline="",
            validate=True,
        )

        _assert_body_params_present(
            post_mock,
            [
                "ordertype",
                "type",
                "volume",
                "pair",
                "nonce",
                "userref",
                "price",
                "price2",
                "trigger",
                "leverage",
                "stp_type",
                "oflags",
                "timeinforce",
                "starttm",
                "expiretm",
                "close[ordertype]",
                "close[price]",
                "close[price2]",
                "deadline",
                "validate",
            ],
        )

    @patch("kraken_spot.private.http_post")
    def test_edit_order(self, post_mock):
        self.client.edit_order(tx_id="", pair="")
        _assert_operation(post_mock, "EditOrder")
        _assert_body_params_present(post_mock, ["txid", "pair", "nonce"])
        _assert_body_params_absent(
            post_mock,
            [
                "volume",
                "price",
                "price2",
                "oflags",
                "deadline",
                "cancel_response",
                "validate",
            ],
        )

        self.client.edit_order(
            tx_id="",
            pair="",
            user_ref=1,
            volume="",
            price="",
            price_2="",
            o_flags="",
            deadline="",
            cancel_response=True,
            validate=True,
        )
        _assert_body_params_present(
            post_mock,
            [
                "txid",
                "pair",
                "nonce",
                "volume",
                "price",
                "price2",
                "oflags",
                "deadline",
                "cancel_response",
                "validate",
            ],
        )

    @patch("kraken_spot.private.http_post")
    def test_cancel_order(self, post_mock):
        self.client.cancel_order(tx_id="1")
        _assert_operation(post_mock, "CancelOrder")
        _assert_body_params_present(post_mock, ["txid", "nonce"])

    @patch("kraken_spot.private.http_post")
    def test_cancel_all_orders(self, post_mock):
        self.client.cancel_all_orders()
        _assert_operation(post_mock, "CancelAll")
        _assert_body_params_present(post_mock, ["nonce"])

    @patch("kraken_spot.private.http_post")
    def test_cancel_all_orders_after_timeout(self, post_mock):
        self.client.cancel_all_orders_after_timeout(10)
        _assert_operation(post_mock, "CancelAllOrdersAfter")
        _assert_body_params_present(post_mock, ["nonce", "timeout"])

    # - User funding

    @patch("kraken_spot.private.http_post")
    def test_get_deposit_methods(self, post_mock):
        self.client.get_deposit_methods(asset="")
        _assert_operation(post_mock, "DepositMethods")
        _assert_body_params_present(post_mock, ["nonce", "asset"])

    @patch("kraken_spot.private.http_post")
    def test_get_deposit_addresses(self, post_mock):
        self.client.get_deposit_addresses(asset="", method="")
        _assert_operation(post_mock, "DepositAddresses")
        _assert_body_params_present(post_mock, ["nonce", "asset", "method"])
        _assert_body_params_absent(post_mock, ["new"])

        self.client.get_deposit_addresses(asset="", method="", new=False)
        _assert_body_params_present(post_mock, ["nonce", "asset", "method", "new"])

    @patch("kraken_spot.private.http_post")
    def test_get_status_of_recent_deposits(self, post_mock):
        self.client.get_status_of_recent_deposits(asset="")
        _assert_operation(post_mock, "DepositStatus")
        _assert_body_params_present(post_mock, ["nonce", "asset"])
        _assert_body_params_absent(post_mock, ["method"])

        self.client.get_status_of_recent_deposits(asset="", method="")
        _assert_body_params_present(post_mock, ["nonce", "asset", "method"])

    @patch("kraken_spot.private.http_post")
    def test_get_withdrawal_information(self, post_mock):
        self.client.get_withdrawal_information(asset="", key="", amount="")
        _assert_operation(post_mock, "WithdrawInfo")
        _assert_body_params_present(post_mock, ["nonce", "asset", "key", "amount"])

    @patch("kraken_spot.private.http_post")
    def test_get_withdrawal_funds(self, post_mock):
        self.client.withdrawal_funds(asset="", key="", amount="")
        _assert_operation(post_mock, "Withdraw")
        _assert_body_params_present(post_mock, ["nonce", "asset", "key", "amount"])

    @patch("kraken_spot.private.http_post")
    def test_get_status_of_recent_withdrawal(self, post_mock):
        self.client.get_status_of_recent_withdrawal(asset="")
        _assert_operation(post_mock, "WithdrawStatus")
        _assert_body_params_present(post_mock, ["nonce", "asset"])
        _assert_body_params_absent(post_mock, ["method"])

        self.client.get_status_of_recent_withdrawal(asset="", method="")
        _assert_body_params_present(post_mock, ["nonce", "asset", "method"])

    @patch("kraken_spot.private.http_post")
    def test_request_withdrawal_cancellation(self, post_mock):
        self.client.request_withdrawal_cancellation(asset="", ref_id="")
        _assert_operation(post_mock, "WithdrawCancel")
        _assert_body_params_present(post_mock, ["nonce", "asset", "refid"])

    @patch("kraken_spot.private.http_post")
    def test_request_wallet_transfer(self, post_mock):
        self.client.request_wallet_transfer(
            asset="", address_from="", address_to="", amount=""
        )
        _assert_operation(post_mock, "WalletTransfer")
        _assert_body_params_present(
            post_mock, ["nonce", "asset", "from", "to", "amount"]
        )

    # - User staking

    @patch("kraken_spot.private.http_post")
    def test_stake_asset(self, post_mock):
        self.client.stake_asset(asset="", amount="", method="")
        _assert_operation(post_mock, "Stake")
        _assert_body_params_present(post_mock, ["nonce", "asset", "method", "amount"])

    @patch("kraken_spot.private.http_post")
    def test_unstake_asset(self, post_mock):
        self.client.unstake_asset(asset="", amount="")
        _assert_operation(post_mock, "Unstake")
        _assert_body_params_present(post_mock, ["nonce", "asset", "amount"])

    @patch("kraken_spot.private.http_post")
    def test_stakeable_assets(self, post_mock):
        self.client.list_stakeable_assets()
        _assert_operation(post_mock, "Staking/Assets")
        _assert_body_params_present(post_mock, ["nonce"])

    @patch("kraken_spot.private.http_post")
    def test_get_pending_staking_transactions(self, post_mock):
        self.client.get_pending_staking_transactions()
        _assert_operation(post_mock, "Staking/Pending")
        _assert_body_params_present(post_mock, ["nonce"])

    @patch("kraken_spot.private.http_post")
    def test_list_of_staking_transactions(self, post_mock):
        self.client.list_of_staking_transactions()
        _assert_operation(post_mock, "Staking/Transactions")
        _assert_body_params_present(post_mock, ["nonce"])

    # - Websockets

    @patch("kraken_spot.private.http_post")
    def test_get_websockets_token(self, post_mock):
        self.client.get_websockets_token()
        _assert_operation(post_mock, "GetWebSocketsToken")
        _assert_body_params_present(post_mock, ["nonce"])
