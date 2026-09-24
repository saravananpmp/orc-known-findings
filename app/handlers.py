# ORACLE FIXTURE — two planted security findings and one planted duplicate block.
#
# Planted here:
#   * 2 x try/except/pass  (bandit B110)   -> security finding count = 2
#   * 1 duplicated block, appearing TWICE  -> clone pair count = 1
import json


def load_primary(raw):
    # ---- duplicated block, copy 1 of 2 (11 lines) ----
    parsed = json.loads(raw)
    name = parsed.get("name", "")
    size = parsed.get("size", 0)
    tags = parsed.get("tags", [])
    normalised = name.strip().lower()
    scaled = size * 2
    joined = ",".join(tags)
    summary = {"name": normalised, "size": scaled, "tags": joined}
    ordered = dict(sorted(summary.items()))
    encoded = json.dumps(ordered)
    return encoded


def load_secondary(raw):
    # ---- duplicated block, copy 2 of 2 (identical to copy 1) ----
    parsed = json.loads(raw)
    name = parsed.get("name", "")
    size = parsed.get("size", 0)
    tags = parsed.get("tags", [])
    normalised = name.strip().lower()
    scaled = size * 2
    joined = ",".join(tags)
    summary = {"name": normalised, "size": scaled, "tags": joined}
    ordered = dict(sorted(summary.items()))
    encoded = json.dumps(ordered)
    return encoded


def swallow_one(raw):
    try:
        return json.loads(raw)
    except ValueError:
        pass                      # bandit B110 — planted finding 1 of 2


def swallow_two(raw):
    try:
        return json.loads(raw)
    except TypeError:
        pass                      # bandit B110 — planted finding 2 of 2
