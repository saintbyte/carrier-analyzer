from parser import detect_currency_string
from parser import get_currency_string_by_currency_marker
from parser import get_entries
from parser import get_feed
from parser import get_vacancy_id

import pytest


@pytest.fixture
def setup():
    pass


def teardown():
    pass


def test_first():
    return True


def test_get_feed():
    url = "https://ya.ru/"
    get_feed(url)


def test_get_entries():
    get_entries([])


def test_get_currency_string_by_currency_marker():
    s = ""
    get_currency_string_by_currency_marker(s)


def test_detect_currency_string():
    s = ""
    detect_currency_string(s)


def test_get_vacancy_id():
    url = "https://yandex.ru/"
    get_vacancy_id(url)


def test_get_job_title():
    pass


def test_get_developer_level():
    pass


def test_get_location_and_salary():
    pass


def test_get_fulltime():
    pass


def test_get_remote():
    pass


def test_get_skills():
    pass
