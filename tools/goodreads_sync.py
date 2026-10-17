#!/usr/bin/env python3
"""Pull the public Goodreads shelves into _data/goodreads.json for the Books page.

Goodreads closed its API in 2020, but each shelf still has a public RSS feed.
This reads the "currently-reading" and "read" shelves and writes one JSON file
that Jekyll exposes as site.data.goodreads.

The file is rewritten only when the books change, so a nightly run that finds
nothing new leaves the repository untouched. If Goodreads can't be reached the
script exits with an error and keeps the existing file.

Usage: python3 tools/goodreads_sync.py
"""

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

USER_ID = "36011711"
PROFILE_URL = "https://www.goodreads.com/user/show/36011711-srinivasan-nanduri"
FEED_URL = "https://www.goodreads.com/review/list_rss/{user}?shelf={shelf}&page={page}"
OUTPUT = Path(__file__).resolve().parent.parent / "_data" / "goodreads.json"
MAX_PAGES = 20  # 100 books per page


def fetch_shelf(shelf):
    books = []
    for page in range(1, MAX_PAGES + 1):
        url = FEED_URL.format(user=USER_ID, shelf=shelf, page=page)
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (site sync)"})
        with urllib.request.urlopen(request, timeout=30) as response:
            root = ET.fromstring(response.read())
        items = root.findall("channel/item")
        books.extend(parse_item(item) for item in items)
        if len(items) < 100:
            break
    return books


def parse_item(item):
    def text(tag):
        return " ".join((item.findtext(tag) or "").split())

    title = text("title")
    rating = int(text("user_rating") or 0)
    return {
        "id": text("book_id"),
        "title": title.split(":")[0].strip() if ":" in title else title,
        "author": text("author_name"),
        "rating": rating or None,
        "read_at": to_date(text("user_read_at")),
        "added_at": to_date(text("user_date_added")),
        "url": "https://www.goodreads.com/book/show/" + text("book_id"),
    }


def to_date(value):
    if not value:
        return None
    return parsedate_to_datetime(value).date().isoformat()


def main():
    try:
        reading = fetch_shelf("currently-reading")
        read = fetch_shelf("read")
    except Exception as error:  # network or feed format problem: keep the old file
        print(f"Could not read Goodreads: {error}", file=sys.stderr)
        return 1

    reading.sort(key=lambda b: b["added_at"] or "", reverse=True)
    read.sort(key=lambda b: b["read_at"] or b["added_at"] or "", reverse=True)
    books = {"profile": PROFILE_URL, "currently_reading": reading, "read": read}

    if OUTPUT.exists():
        previous = json.loads(OUTPUT.read_text())
        previous.pop("updated", None)
        if previous == books:
            print("No changes on Goodreads.")
            return 0

    books["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    OUTPUT.write_text(json.dumps(books, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(reading)} currently reading and {len(read)} read to {OUTPUT.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
