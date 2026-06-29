"""Exports the brief (and optionally the other sheets) to CSV."""

import csv
import io

from schema import BRIEF_FIELDS


def brief_to_csv_bytes(brief: dict) -> bytes:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Field", "Response"])
    for field in BRIEF_FIELDS:
        entry = brief.get(field, {"value": "Missing"})
        writer.writerow([field, entry["value"]])
    return buf.getvalue().encode("utf-8")
