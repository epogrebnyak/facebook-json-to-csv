import datetime

from friends import extract_timestamp


def test_get_timestamp():
    assert extract_timestamp(1582964988) == datetime.datetime(2020, 2, 29, 11, 29, 48)
    #pd.Timestamp("2020-02-29 08:29:48")
