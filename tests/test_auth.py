from time import sleep

from kraken_spot.auth import generate_nonce, get_kraken_signature
from kraken_spot.errors import AuthError


def test_generate_nonce():
    nonce_1 = generate_nonce()
    sleep(1 / 1_000_000)  # sleep for 1 microsecond before generating another nonce
    nonce_2 = generate_nonce()
    assert nonce_2 > nonce_1


def test_get_kraken_signature_requires_nonce():
    try:
        get_kraken_signature("/", {}, "secret")
        assert False
    except AuthError as e:
        assert True
        assert "nonce" in str(e)
