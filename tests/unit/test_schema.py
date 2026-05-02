"""Basic schema validation tests."""

from datetime import UTC, datetime

from sinyra.normalize.schema import RawItem


def test_raw_item_minimal() -> None:
    item = RawItem(title="Test", link="https://example.com")
    assert item.title == "Test"
    assert item.summary == ""
    assert item.pub_date is None


def test_raw_item_full() -> None:
    item = RawItem(
        title="OpenAI launches GPT-5",
        link="https://openai.com/blog/gpt-5",
        summary="OpenAI today announced GPT-5...",
        pub_date=datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC),
        source_name="OpenAI Blog",
        hint_company="openai",
    )
    assert item.hint_company == "openai"
