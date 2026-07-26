"""Shared test fixtures for PathReview.

Issue #159 reproduction (structlog vs pytest caplog):
  Command (from repo root):
    pytest tests/unit/test_batch_processor.py -k
    test_empty_chunks_list_returns_empty -q
  Observed (2026-07-26):
    - BatchEmbeddingProcessor.process([]) emits
      "Empty chunks list provided to BatchEmbeddingProcessor" on stdout.
    - Assertion on caplog fails: caplog.text == "" and caplog.records
      is empty.
  Cause:
    Application code uses structlog.get_logger(); this conftest does not
    yet configure structlog to propagate into stdlib logging, so
    pytest's caplog fixture never sees those events.
  Week 9:
    Add test logging configuration here (structlog.stdlib /
    ProcessorFormatter) so caplog-based assertions work suite-wide
    without changing production configure_logging() in core/logging.py.
"""

import pytest


@pytest.fixture
def sample_resume_text() -> str:
    """Return a sample resume text for testing."""
    return """
    Jane Doe
    Software Engineer
    jane.doe@example.com | github.com/janedoe

    Experience:
    - Software Engineer at TechCorp (2022-2024)
      Built REST APIs using Python and FastAPI.

    Education:
    - B.S. Computer Science, State University (2022)

    Skills: Python, JavaScript, React, PostgreSQL, Docker
    """


@pytest.fixture
def sample_readme_text() -> str:
    """Return a sample README text for testing."""
    return """
    # Weather App
    A weather forecasting application built with React and OpenWeatherMap API.

    ## Features
    - Current weather display
    - 5-day forecast
    - Location search

    ## Tech Stack
    - React 18
    - TypeScript
    - Tailwind CSS
    - OpenWeatherMap API
    """
