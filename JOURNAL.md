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
