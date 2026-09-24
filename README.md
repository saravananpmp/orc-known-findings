# orc-known-findings — the counted-findings repo

Every finding in this repository was planted deliberately and counted. The counts
are properties of the code, not of any tool. A leaf that reports a different number
is a scoring defect.

## What is planted, and how many

| Finding | Count | Where | Verified with |
|---|---|---|---|
| **Hardcoded secrets** | **3** | `app/config.py` | published dummy values, hand-counted |
| **Unused imports** | **9** | `app/imports.py` | `ruff` F401 = 9, nothing else |
| **try/except/pass** (swallowed errors) | **2** | `app/handlers.py` | bandit B110 |
| **Duplicated block** | **1 pair** (2 copies, 11 identical lines each) | `app/handlers.py` | byte-identical, verified |
| **Dependency with a published CVE** | **1** | `requirements.txt` | `requests==2.19.1` → CVE-2018-18074 |

Everything else in the repository is clean: `ruff` reports **9** violations in total,
all of them the planted F401s.

## What the report must say

* Secret-detection leaves: **3** distinct secrets. Not 2, not 4, and not 0.
* Unused-import / dead-import leaf: **9**.
* Security (SAST) leaf: **2** findings, both low severity.
* Duplication leaf: **1** clone pair / 2 copies.
* SCA leaves: **at least 1** CVE — and crucially, **licence compliance must not be
  affected by the CVE count**. If removing the vulnerable dependency changes the
  licence score, the pip-audit `legal_risk` wiring defect is still present.

## Notes

* The three secrets are AWS's own published example credentials plus an obviously
  synthetic token. They are safe to commit and grant access to nothing.
* `requests==2.19.1` is pinned for the CVE only. Do not `pip install -r` this file
  into anything real; it is a fixture.
* The CVE expectation is the one value not verified locally (it needs a live
  advisory database). Everything else in the table was measured.
