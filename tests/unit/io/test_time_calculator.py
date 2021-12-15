from datetime import datetime

from freezegun import freeze_time

from prmexporter.io.time_calculator import TimeCalculator


@freeze_time(datetime(year=2021, month=11, day=13, hour=2, second=0))
def test_returns_today_midnight():
    time_calculator = TimeCalculator()

    actual_today_midnight = time_calculator.get_today_midnight_unix_timestamp()

    expected_today_midnight = 1636761600

    assert actual_today_midnight == expected_today_midnight


@freeze_time(datetime(year=2021, month=11, day=13, hour=2, second=0))
def test_returns_yesterday_midnight():
    time_calculator = TimeCalculator()

    actual_yesterday_midnight = time_calculator.get_yesterday_midnight_unix_timestamp()

    expected_yesterday_midnight = 1636675200

    assert actual_yesterday_midnight == expected_yesterday_midnight