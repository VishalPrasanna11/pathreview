# PathReview — Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/159

**Issue title:** structlog output is not captured by pytest caplog — log assertions fail suite-wide

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**

PathReview uses structlog for application logging across modules like `ingestion/embeddings/batch_processor.py`. Several unit tests assert on log output using pytest's `caplog` fixture — for example, `test_empty_chunks_list_returns_empty` in `tests/unit/test_batch_processor.py` expects a warning when an empty chunk list is processed. Today, structlog is not wired into stdlib logging during tests, so log events print to stdout but never appear in `caplog.text` or `caplog.records`. I reproduced this locally: the warning is visible in captured stdout, but the assertion fails because `caplog.text` is empty. A successful fix will configure structlog in `tests/conftest.py` (likely using `structlog.stdlib` processors or an equivalent capture hook) so caplog-based assertions work suite-wide without changing production logging behavior.

**Selection notes ("Is this right for me?" checklist):**

- **Tier fit:** Tier 1 — scoped to test configuration, not a full subsystem rewrite. Good for a first contribution to a large codebase.
- **Files are identifiable:** Primary touch point is `tests/conftest.py`; reference implementation exists in `core/logging.py`.
- **Reproducible locally:** One failing test confirms the bug in under 5 seconds (`pytest tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_empty_chunks_list_returns_empty -q`).
- **No external API keys required:** Pure test-infra fix; LLM and GitHub integrations are not involved.
- **Effort is realistic:** Issue is tests-focused with a clear before/after signal — caplog assertions pass once structlog propagates correctly.
- **Risk is low:** Changes stay in test setup; production `configure_logging()` in `core/logging.py` should remain untouched.

**Branch name:** fix/159-structlog-caplog-capture

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** [https://github.com/VishalPrasanna11/pathreview/commit/b1be7950d83f4b1c7953f8d4bba52aacd473914d](https://github.com/VishalPrasanna11/pathreview/commit/b1be7950d83f4b1c7953f8d4bba52aacd473914d)

**Reproduction summary:**
Ran `pytest tests/unit/test_batch_processor.py::TestBatchEmbeddingProcessor::test_empty_chunks_list_returns_empty -q`. The warning from `BatchEmbeddingProcessor` printed to stdout (`Empty chunks list provided to BatchEmbeddingProcessor`), but the assertion failed because `caplog.text` was empty and `caplog.records` had no entries — structlog is not wired into stdlib logging in tests.

**PLAN.md link:** [https://github.com/VishalPrasanna11/pathreview/blob/fix/159-structlog-caplog-capture/PLAN.md](https://github.com/VishalPrasanna11/pathreview/blob/fix/159-structlog-caplog-capture/PLAN.md)

**Walkthrough video (recommended):**

**Blockers or open questions:**
Whether `cache_logger_on_first_use=True` in `core/logging.py` requires configuring structlog at `conftest` import time vs an autouse fixture; confirm the exact processor chain so `record.message` / `caplog.text` match the test’s substring checks.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
Implemented PLAN.md sub-tasks 1–3: import-time structlog→stdlib configuration in `tests/conftest.py` (`LoggerFactory`, `BoundLogger`, `cache_logger_on_first_use=False`, ConsoleRenderer) plus an autouse INFO-level fixture. Confirmed `test_empty_chunks_list_returns_empty` passes with assertions unchanged.

**Next steps:**
Add a focused unit test for caplog capture, run full `make test-unit` / lint on touched files, open the PR to upstream, and finish Check-in 2.

**Blockers:**

---

### Check-in 2 (end of week)

**PR link:** [https://github.com/ascherj/pathreview/pull/639](https://github.com/ascherj/pathreview/pull/639)

**Branch:** `fix/159-structlog-caplog-capture`

**What you built:**
Wired structlog into stdlib logging during pytest in `tests/conftest.py` so `caplog` receives application log events. Production `configure_logging()` is untouched; tests now see warnings such as the empty-chunks message from `BatchEmbeddingProcessor`.

**Tests added or updated:**
- `tests/unit/test_structlog_caplog.py` — asserts structlog warnings appear in `caplog.text` and `caplog.records`
- Verified existing `tests/unit/test_batch_processor.py::test_empty_chunks_list_returns_empty` now passes

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes

*(Repo-wide `make check` / `make test-unit` still report pre-existing unrelated failures; this change introduces no new failures — suite went from 52 failed / 345 passed to 51 failed / 348 passed. Touched files pass ruff/black; typed packages are unchanged.)*

**Draft PR feedback received from:** none
