import os

from kraken_spot import DefaultClient

if __name__ == "__main__":
    client = DefaultClient()

    # client.set_otp(482934)
    print(client.get_account_balance())
