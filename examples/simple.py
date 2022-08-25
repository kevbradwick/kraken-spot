import os

from kraken_spot import DefaultClient

if __name__ == "__main__":
    client = DefaultClient()

    # public endpoints don't require authentication
    print(client.get_server_time())

    # private endpoints need valid api keys with the appropriate permissions
    print(client.get_account_balance())
