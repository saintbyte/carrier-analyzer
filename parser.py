import logging
import os

import feedparser

logger = logging.getLogger(__name__)


def get_feed(url: str):
    return feedparser.parse(url)


def get_entries(feed):
    return feed["entries"]


def main():
    logger.info("Start")
    feed = get_feed(os.environ.get("RSS_URL"))
    for entry in get_entries(feed):
        logger.info(entry["title"])


if __name__ == "__main__":
    main()
