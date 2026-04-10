import pytest

@pytest.fixture
def sample_text() -> str:
      return """This is the first paragraph

      This is the second paragraph.

      This is the third paragrah"""
