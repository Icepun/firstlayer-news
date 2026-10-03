"""Checks the announcements file against the game's rules. Exits with code 1 on errors, which stops the GitHub publish.

Usage:  python tools/validate.py site/first-layer/announcements.json
"""
import json
import sys
from datetime import datetime
from urllib.parse import urlparse

DATE_FORMATS = ["%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%MZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S.%fZ"]
LIMITS = {"category": 32, "title": 120, "summary": 280, "body": 8000, "linkLabel": 40}
KNOWN = {"id", "pinned", "date", "category", "title", "summary", "body", "image", "link", "linkLabel", "start", "end",
         "minVersion", "maxVersion", "tr", "pl"}
LANGUAGES = ("tr", "pl")


def parse_date(value):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def is_https(value):
    parsed = urlparse(value.strip())
    return parsed.scheme == "https" and bool(parsed.netloc)


def main(path):
    errors, warnings = [], []
    raw = open(path, "rb").read()
    if len(raw) > 256 * 1024:
        errors.append("File is larger than 256 KB.")
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"ERROR  Not valid JSON: {error}")
        return 1

    items = data.get("announcements") if isinstance(data, dict) else None
    if not isinstance(items, list):
        print('ERROR  The file needs an "announcements" list.')
        return 1

    ids = set()
    for index, item in enumerate(items, 1):
        where = f"#{index}"
        if not isinstance(item, dict):
            errors.append(f"{where}: not an object.")
            continue
        item_id = str(item.get("id", "")).strip()
        where = f"#{index} ({item_id or 'no id'})"
        if not item_id:
            errors.append(f"{where}: missing \"id\".")
        elif item_id in ids:
            errors.append(f"{where}: \"id\" is used twice.")
        ids.add(item_id)
        if not str(item.get("title", "")).strip():
            errors.append(f"{where}: missing \"title\".")
        for key in item:
            if key not in KNOWN:
                warnings.append(f"{where}: unknown field \"{key}\" is ignored by the game.")
        for key in ("date", "start", "end"):
            if key in item and parse_date(str(item[key]).strip()) is None:
                errors.append(f"{where}: \"{key}\" must look like 2026-10-04 or 2026-10-04T18:00:00Z.")
        for key in ("link", "image"):
            if key in item and str(item[key]).strip() and not is_https(str(item[key])):
                errors.append(f"{where}: \"{key}\" must start with https://")
        texts = [("", item)] + [(f"{lang}.", item[lang]) for lang in LANGUAGES if isinstance(item.get(lang), dict)]
        for prefix, block in texts:
            for key, limit in LIMITS.items():
                value = str(block.get(key, ""))
                if len(value) > limit:
                    warnings.append(f"{where}: \"{prefix}{key}\" is {len(value)} characters; the game shortens it to {limit}.")
        if "start" in item and "end" in item:
            start, end = parse_date(str(item["start"])), parse_date(str(item["end"]))
            if start and end and end < start:
                errors.append(f"{where}: \"end\" is before \"start\".")

    for line in warnings:
        print("WARN   " + line)
    for line in errors:
        print("ERROR  " + line)
    print(f"{len(items)} announcements, {len(errors)} errors, {len(warnings)} warnings.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "site/first-layer/announcements.json"))
