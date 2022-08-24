import os

from kraken_spot.client import Client

if __name__ == "__main__":
    client = Client(
        api_key=os.environ["KRAKEN_API_KEY"],
        private_key=os.environ["KRAKEN_PRIVATE_KEY"],
    )
    print(client.trade_balance("ZUSD"))
