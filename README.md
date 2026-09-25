# orc-known-findings — the counted-findings repo

Every finding in this repository was planted deliberately and counted. The counts
are properties of the code, not of any tool. A leaf that reports a different number
is a scoring defect.

**All counts below were measured on 2026-09-25 by running the tools themselves.**
Where two tools disagree, both numbers are stated — an oracle that hides a
disagreement is worse than no oracle.

## What is planted, and how many

| Finding | Count | Where | Measured with |
|---|---|---|---|
| **Hardcoded secrets** | **3** (detect-secrets) / **2** (bandit B105) | `app/config.py` | `detect-secrets scan` → 3; `bandit` → 2 |
| **Unused imports** | **9** | `app/imports.py` | `ruff --select F401` → 9 |
| **Swallowed exceptions** | **2** | `app/handlers.py` | `bandit` B110 → 2 |
| **Duplicated block** | **1 pair** (2 copies, 14 lines / 102 tokens) | `app/handlers.py` | `jscpd --min-lines 5` → 1 |
| **Vulnerable direct dependency** | **1 package, 1 advisory** | `requirements.txt` | `pip-audit` → certifi 2023.7.22, PYSEC-2024-230 |

Tests: `pytest` → **3 passed**. The tests exist only so the tools have something to
run; they are not part of what is being measured.

## The two tool disagreements you must know about

**Secrets: 3 or 2, depending on the tool.** `detect-secrets` finds all three
(AWS Access Key, Base64 High Entropy String, Secret Keyword). `bandit` finds only
two — its B105 check matches on variable *names* containing password/token/secret,
and `AWS_ACCESS_KEY_ID` does not match. So before calling a secrets leaf wrong,
check which tool feeds it. 3 for detect-secrets, 2 for bandit; anything else is a
defect.

**Swallowed exceptions must use a BARE `except:`.** Bandit's B110 defaults to
`check_typed_exception: False`, so `except ValueError: pass` is deliberately NOT
reported. The two planted handlers in `app/handlers.py` use a bare `except:` on
purpose. If someone "tidies" them into typed excepts, the expected count silently
becomes 0 and this fixture stops testing anything.

## What the report must say

* Secret-detection leaf: **3** (detect-secrets) or **2** (bandit). Never 0.
* Unused-import / dead-import leaf: **9**.
* Security (SAST) leaf: **4** bandit findings total — 2 × B105 + 2 × B110, all low
  severity. The B110 count on its own is **2**.
* Duplication leaf: **1** clone pair / 2 copies.
* SCA leaf: **1** vulnerable direct dependency. And crucially, **licence compliance
  must not be affected by the CVE count** — if removing the vulnerable dependency
  changes the licence score, the pip-audit `legal_risk` wiring defect is present.

## Notes on the dependency pin

`certifi==2023.7.22` is pinned because certifi has **no dependencies of its own**,
so the resolved tree is one package with one advisory and there is no transitive
noise.

Do **not** swap it for `requests==2.19.1` or any other old `requests`. That pulls in
vulnerable `urllib3` and `idna`, and the resolved count becomes roughly 36
advisories across 4 packages — which makes the count unusable as an oracle. (An
earlier version of this fixture made exactly that mistake and claimed "1 CVE".)

**Advisory counts drift** as new CVEs are published against old versions. The stable
oracle value is "**1 vulnerable direct dependency**". Treat the advisory count as
informational and re-measure with `pip-audit -r requirements.txt` if it matters.

## Re-measuring everything yourself

```bash
pip install ruff bandit detect-secrets pip-audit
npm install -g jscpd

ruff check --select F401 .                 # expect 9
bandit -r app                              # expect 4 (2x B105, 2x B110)
detect-secrets scan app/config.py          # expect 3
jscpd app --min-lines 5                    # expect 1 clone pair
pip-audit -r requirements.txt              # expect certifi, 1 advisory
python3 -m pytest -q                       # expect 3 passed
```
