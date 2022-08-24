from time import sleep

from kraken_spot.auth import generate_nonce


def test_generate_nonce():
    nonce_1 = generate_nonce()
    sleep(1 / 1_000_000)  # sleep for 1 microsecond before generating another nonce
    nonce_2 = generate_nonce()
    assert nonce_2 > nonce_1
