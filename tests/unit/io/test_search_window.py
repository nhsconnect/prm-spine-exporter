from datetime import datetime

from freezegun import freeze_time

from prmexporter.io.search_window import SearchWindow


@freeze_time(datetime(year=2021, month=11, day=13, hour=2, minute=0, second=0))
def test_returns_end_datetime_midnight_string():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_end_datetime_midnight = search_window.get_end_datetime_string()

    expected_end_datetime_midnight = "2021-11-13T00:00:00"

    assert actual_end_datetime_midnight == expected_end_datetime_midnight


@freeze_time(datetime(year=2021, month=11, day=13, hour=2, minute=0, second=0))
def test_returns_start_datetime_midnight_string():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_start_datetime_midnight = search_window.get_start_datetime_string()

    expected_start_datetime_midnight = "2021-11-12T00:00:00"

    assert actual_start_datetime_midnight == expected_start_datetime_midnight


@freeze_time(datetime(year=2021, month=11, day=13, hour=0, minute=0, second=0))
def test_returns_end_datetime_midnight_string_when_at_midnight():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_end_datetime_midnight = search_window.get_end_datetime_string()

    expected_end_datetime_midnight = "2021-11-13T00:00:00"

    assert actual_end_datetime_midnight == expected_end_datetime_midnight


@freeze_time(datetime(year=2021, month=1, day=1, hour=2, minute=0, second=0))
def test_returns_start_datetime_midnight_string_when_changing_years():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_start_datetime_midnight = search_window.get_start_datetime_string()

    expected_start_datetime_midnight = "2020-12-31T00:00:00"

    assert actual_start_datetime_midnight == expected_start_datetime_midnight


@freeze_time(datetime(year=2021, month=1, day=1, hour=2, minute=4, second=45))
def test_returns_start_datetime():
    search_window = SearchWindow.prior_to_now(number_of_days=1)

    actual_start_datetime = search_window.get_start_datetime()

    expected_start_datetime = datetime(year=2020, month=12, day=31, hour=0, minute=0, second=0)

    assert actual_start_datetime == expected_start_datetime


@freeze_time(datetime(year=2021, month=1, day=1, hour=2, minute=4, second=45))
def test_returns_start_datetime_when_number_of_days_is_3():
    search_window = SearchWindow.prior_to_now(number_of_days=3)

    actual_start_datetime = search_window.get_start_datetime()

    expected_start_datetime = datetime(year=2020, month=12, day=29, hour=0, minute=0, second=0)

    assert actual_start_datetime == expected_start_datetime
