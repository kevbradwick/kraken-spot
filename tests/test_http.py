from kraken_spot.http import clean_params


def test_clean_params_converts_bool_to_str():
    o = clean_params({"ok": True, "not": False})

    assert "true" == o["ok"]
    assert "false" == o["not"]


def test_clean_params_int_to_string():
    o = clean_params({"i": 123})

    assert "123" == o["i"]


def test_clean_params_removes_none_values():
    o = clean_params({"n": None})

    assert {} == o
