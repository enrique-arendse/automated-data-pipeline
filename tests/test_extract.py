
import pytest
import requests

from extract import extract_posts


def test_extract_posts_returns_api_data(monkeypatch):
    """Test that extraction returns the data from the API."""

    expected_posts = [
        {
            "userId": 1,
            "id": 1,
            "title": "Example title",
            "body": "Example body",
        }
    ]

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return expected_posts

    def mock_get(url, timeout):
        assert url == "https://jsonplaceholder.typicode.com/posts"
        assert timeout == 30
        return MockResponse()

    monkeypatch.setattr("extract.requests.get", mock_get)

    result = extract_posts()

    assert result == expected_posts
    assert len(result) == 1


def test_extract_posts_raises_http_error(monkeypatch):
    """Test that extraction raises an error for a failed HTTP response."""

    class MockResponse:
        def raise_for_status(self):
            raise requests.exceptions.HTTPError(
                "500 Server Error"
            )

    def mock_get(url, timeout):
        return MockResponse()

    monkeypatch.setattr("extract.requests.get", mock_get)

    with pytest.raises(requests.exceptions.HTTPError):
        extract_posts()


def test_extract_posts_raises_connection_error(monkeypatch):
    """Test that extraction raises an error when the API is unreachable."""

    def mock_get(url, timeout):
        raise requests.exceptions.ConnectionError(
            "API unavailable"
        )

    monkeypatch.setattr("extract.requests.get", mock_get)

    with pytest.raises(requests.exceptions.ConnectionError):
        extract_posts()
