import logging
import os
from typing import Optional

import feedparser

# from db import db
# from models import Vacancy

logger = logging.getLogger(__name__)

DOT: str = "."
RIGHT_QUOTE_MARKER: str = "»"
SPACE: str = " "
COMMA: str = ","
VACANCY_URL_STARTS: str = "https://career.habr.com/vacancies/"
FULLTIME_MARKER: str = "Полный рабочий день."
REMOTE_MARKER: str = "Можно удалённо."
SKILLS_MARKER: str = "Требуемые навыки:"
WANTS_PREFIX: str = "Требуется «"
HAS_TOWN_SALARY_MARKER: str = "» ("

SALARY_START_MARKER: str = "от "
SALARY_END_MARKER: str = " до "
SALARY_IN_TEXT_MARKER: str = ". От"

CURRENCY_RUB_MARKER: str = "₽"
CURRENCY_EURO_MARKER: str = "€"
CURRENCY_DOLLAR_MARKER: str = "$"

CURRENCY_MARKER_LIST: list[str] = [
    CURRENCY_RUB_MARKER,
    CURRENCY_EURO_MARKER,
    CURRENCY_DOLLAR_MARKER,
]
CURRENCY_NAMES_LIST: list[str] = [
    "RUR",
    "EURO",
    "USD",
]

SENIOR_LEVEL: str = "Senior"
SENIOR_SHORT_LEVEL: str = "Sr"
SENIOR_RUS: str = "Ведущий"
SENIOR_OR_MIDDLE: str = "Middle/Senior"
SENIOR_OR_MIDDLE_PLUS: str = "Middle+/Senior"

MIDDLE_PLUS: str = "Middle+"
MIDDLE_LEVEL: str = "Middle"

JUINOR_LEVEL: str = "Junior"
JUINOR_RUS_LEVEL: str = "Младший"
LEAD_LEVEL: str = "Lead"

DEVELOPER_LEVELS: list[str] = [
    SENIOR_LEVEL,
    SENIOR_SHORT_LEVEL,
    SENIOR_OR_MIDDLE,
    MIDDLE_PLUS,
    MIDDLE_LEVEL,
    JUINOR_LEVEL,
    LEAD_LEVEL,
]


def get_feed(url: str) -> feedparser.util.FeedParserDict:
    return feedparser.parse(url)


def get_entries(feed: feedparser.util.FeedParserDict) -> list:
    return feed.entries


def get_currency_string_by_currency_marker(marker: Optional[str]) -> Optional[str]:
    if not marker:
        return None
    try:
        return dict(zip(CURRENCY_MARKER_LIST, CURRENCY_NAMES_LIST))[marker]
    except Exception as e:
        logger.warning(f"get_currency_string_by_currency_marker {marker} {e}")
        return None


def detect_currency_string(string: str) -> Optional[str]:
    string = string[::-1]
    for currency in CURRENCY_MARKER_LIST:
        if currency in string:
            return currency
    return None


def get_vacancy_id(vacancy_url: str) -> int:
    if vacancy_url.startswith(VACANCY_URL_STARTS):
        return int(vacancy_url.replace(VACANCY_URL_STARTS, ""))
    raise Exception("cant get vacancy id")


def get_job_title(title: str, *, remove_level: bool = False) -> Optional[str]:
    if not title.startswith(WANTS_PREFIX):
        return None
    try:
        result = title[
            len(WANTS_PREFIX) : title.index(RIGHT_QUOTE_MARKER, len(WANTS_PREFIX))
        ].strip()
        if not remove_level:
            return result
        level = get_developer_level(result)
        if not level:
            return result
        return result[len(level) :].strip()
    except Exception as e:
        logger.error(f"get_job_title: {e}")
    return None


def get_developer_level(job_title: str) -> Optional[str]:
    try:
        level = job_title[0 : job_title.index(SPACE)].strip().lower().replace(".", "")
    except Exception as e:
        logger.warning(f"get_developer_level: {e}")
        return None
    if level in [level.lower() for level in DEVELOPER_LEVELS]:
        return level
    return None


def get_location_and_salary(
    title: str,
) -> tuple[Optional[str], Optional[int], Optional[int], Optional[str]]:
    town = None
    salary_start = None
    salary_end = None
    salary_currency = None
    if HAS_TOWN_SALARY_MARKER not in title:
        return (None, None, None, None)
    title = title[
        title.index(HAS_TOWN_SALARY_MARKER)
        + len(HAS_TOWN_SALARY_MARKER) : len(title)
        - 1
    ]
    if COMMA in title:
        town = title[0 : title.index(COMMA)].strip()
    currency_str = detect_currency_string(title)
    if currency_str:
        title = title.replace(currency_str, "")
        salary_currency = get_currency_string_by_currency_marker(currency_str)
    if SALARY_START_MARKER in title:
        try:
            needed_position = title.index(SALARY_END_MARKER)
            salary_start = int(
                title[
                    title.index(SALARY_START_MARKER)
                    + len(SALARY_START_MARKER) : needed_position
                ]
                .strip()
                .replace(" ", "")
            )
        except ValueError:
            salary_start = int(
                title[title.index(SALARY_START_MARKER) + len(SALARY_START_MARKER) :]
                .strip()
                .replace(" ", "")
            )
    if SALARY_END_MARKER in title:
        salary_end = int(
            title[title.index(SALARY_END_MARKER) + len(SALARY_END_MARKER) :]
            .strip()
            .replace(" ", "")
        )
    if (not salary_start) and (not salary_end):
        town = title
    return (town, salary_start, salary_end, salary_currency)


def get_fulltime(text: str) -> bool:
    if FULLTIME_MARKER in text:
        return True
    return False


def get_remote(text: str) -> bool:
    if REMOTE_MARKER in text:
        return True
    return False


def get_skills(text: str) -> list:
    if SKILLS_MARKER not in text:
        return []
    skills_text = (
        text[text.index(SKILLS_MARKER) + len(SKILLS_MARKER) : len(text) - 1]
        .replace("#", "")
        .strip()
    )
    if COMMA not in skills_text:
        return [
            skills_text.strip(),
        ]
    return [skill.strip() for skill in skills_text.split(COMMA)]


def main():
    logger.info("Start")
    # db.connect()
    feed = get_feed(os.environ.get("RSS_URL"))

    for entry in get_entries(feed):
        print("---------------")
        print(f"title: {entry.title}")
        print(f"link: {entry.link}")
        print(f"autor: {entry.author}")
        print(f"published: {entry.published}")
        print(f"summary: {entry.summary}")
        print(f"updated: {entry.updated}")
        vacancy_id = get_vacancy_id(entry.link)
        print(f"vacancy_id: {vacancy_id}")
        job_title = get_job_title(entry.title, remove_level=True)
        print(f"job_title: {job_title}")
        developer_level = get_developer_level(get_job_title(entry.title))
        print(f"developer_level: {developer_level}")
        (town, salary_start, salary_end, salary_currency) = get_location_and_salary(
            entry.title
        )
        print(f"town: {town}")
        print(f"salary_start: {salary_start}")
        print(f"salary_end: {salary_end}")
        print(f"salary_currency: {salary_currency}")
        is_fulltime = get_fulltime(entry.summary)
        is_remote = get_remote(entry.summary)
        print(f"is_fulltime : {is_fulltime}")
        print(f"is_remote: {is_remote}")
        company_name = entry.author
        print(f"company_name: {company_name}")
        skills = get_skills(entry.summary)
        print(f"skills: {skills}")
        """
    #Times
    created = DateTimeField(default=datetime.datetime.now)
    published = DateTimeField(null=True)  # entry.published_parsed
    updated = DateTimeField(null=True)  # entry.updated_parsed

    #SRC data
    src_title = CharField(blank=True)
    src_link = CharField(blank=True)
    src_author = CharField(blank=True)
    src_published = CharField(blank=True)
    src_summary = TextField(blank=True)
    src_updated = CharField(blank=True)
        """


if __name__ == "__main__":
    main()
