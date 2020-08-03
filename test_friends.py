import pandas as pd

from friends import extract_timestamp


def test_get_timestamp():
    assert extract_timestamp(1582964988) == pd.Timestamp("2020-02-29 08:29:48")
