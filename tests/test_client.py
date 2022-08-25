import os

from kraken_spot import DefaultClient


class TestDefaultClient:
    def test_api_keys_set_from_env(self):
        os.environ["KRAKEN_API_KEY"] = "1"
        os.environ["KRAKEN_PRIVATE_KEY"] = "2"
        client = DefaultClient()

        assert "1" == client.api_key
        assert "2" == client.private_key

    def test_api_keys_not_set_if_one_missing(self):
        os.environ["KRAKEN_API_KEY"] = "1"
        del os.environ["KRAKEN_PRIVATE_KEY"]

        client = DefaultClient()

        assert not client.api_key
        assert not client.private_key
