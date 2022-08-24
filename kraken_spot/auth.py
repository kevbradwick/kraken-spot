import time


def generate_nonce() -> int:
    """
    Each API request needs a nonce value that increases on each request. For simplicity
    this will return the current unix timestamp
    """
    return time.time_ns()
