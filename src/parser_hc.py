from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

import feedparser
from db import db
from models import Vacancy
from peewee import IntegrityError

logger = logging.getLogger(__name__)
from constants import (
    RIGHT_QUOTE_MARKER,
    SPACE,
    COMMA,
    VACANCY_URL_STARTS,
    FULLTIME_MARKER,
    REMOTE_MARKER,
    SKILLS_MARKER,
    WANTS_PREFIX,
    HAS_TOWN_SALARY_MARKER,
    SALARY_START_MARKER,
    SALARY_END_MARKER,
    CURRENCY_MARKER_LIST,
    CURRENCY_NAMES_LIST,
    DEVELOPER_LEVELS,
)


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
    raise ValueError("cant get vacancy id from url")


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
    return FULLTIME_MARKER in text


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
    logger.info("Start parsing from Habr Career")
    db.connect()
    feed = get_feed(os.environ.get("RSS_URL"))
    exists_ids = Vacancy.get_exists_vacancies_ids()
    for entry in get_entries(feed):
        (town, salary_start, salary_end, salary_currency) = get_location_and_salary(
            entry.title
        )
        vacancy_id = get_vacancy_id(entry.link)
        if vacancy_id in exists_ids:
            continue
        v = Vacancy(
            vacancy_id=vacancy_id,
            job_title=get_job_title(entry.title, remove_level=True),
            developer_level=get_developer_level(get_job_title(entry.title)),
            town=town,
            salary_start=salary_start,
            salary_end=salary_end,
            salary_currency=salary_currency,
            is_fulltime=get_fulltime(entry.summary),
            is_remote=get_remote(entry.summary),
            company_name=entry.author,
            skills=get_skills(entry.summary),
            published=datetime(*entry.published_parsed[:6]),
            updated=datetime(*entry.updated_parsed[:6]),
            src_title=entry.title,
            src_link=entry.link,
            src_author=entry.author,
            src_published=entry.published,
            src_summary=entry.summary,
            src_updated=entry.updated,
        )
        try:
            v.save()
        except IntegrityError as e:
            logger.warning(f"IntegrityError {e}")
            continue
        exists_ids.append(vacancy_id)
    Vacancy.set_exists_vacancies_ids(exists_ids)
    logger.info("End")


if __name__ == "__main__":
    main()
