# Kraken Spot

[![Build Status](https://app.travis-ci.com/kevbradwick/kraken-spot.svg?branch=master)](https://app.travis-ci.com/kevbradwick/kraken-spot)

A Python library for interacting with the [Kraken Spot REST API](https://docs.kraken.com/rest/).

## Quick Start

Install from source of via `pip`

    pip install kraken-spot

```python
from kraken_spot import DefaultClient

client = DefaultClient()
client.get_account_balance()
```

The default client will attempt to configure the client with api keys from environment variables. Both `KRAKEN_API_KEY` and `KRAKEN_PRIVATE_KEY` needs to be set.

## OTP Authentication

At the moment, one time password (OTP) is not currently supported in this client for API keys that have 2FA enabled.

## Features

This library is currently in development so *should not* be used in production. The following endpoints are currently supported;

| Endpoint Set | Supported |
| ------ | ------- |
| Market Data | ✅ |
| User Data | ✅ |
| User Trading | ❌ |
| User Funding | ❌ |
| User staking | ❌ |
