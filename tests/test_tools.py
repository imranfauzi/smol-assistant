from types import SimpleNamespace

from pydantic import SecretStr
from requests import Timeout

from tools import google_search as google_search_module
from tools.google_search import google_search


def test_google_search_returns_formatted_results(monkeypatch):
    # Fake the Serper response so the test does not use the network.
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "organic": [
                    {
                        "title": "Example",
                        "link": "https://example.test",
                        "snippet": "Example snippet",
                    }
                ]
            }

    def fake_post(url, headers, json, timeout):
        assert url == "https://google.serper.dev/search"
        assert headers["X-API-KEY"] == "secret-key"
        assert json == {"q": "LangChain news", "num": 5}
        assert timeout == google_search_module.REQUEST_TIMEOUT_SECONDS
        return FakeResponse()

    fake_settings = SimpleNamespace(
        SERPER_URL="https://google.serper.dev/search",
        SERPER_API_KEY=SecretStr("secret-key"),
    )
    monkeypatch.setattr(
        google_search_module,
        "settings",
        fake_settings,
    )
    monkeypatch.setattr(google_search_module.requests, "post", fake_post)

    result = google_search.invoke({"query": "  LangChain news  "})

    assert result == (
        "Title: Example\n"
        "Link: https://example.test\n"
        "Snippet: Example snippet\n"
        "---"
    )


def test_google_search_rejects_empty_query():
    result = google_search.invoke({"query": "   "})

    assert result == "Search query cannot be empty."


def test_google_search_handles_request_error(monkeypatch):
    def fake_post(*args, **kwargs):
        raise Timeout()

    fake_settings = SimpleNamespace(
        SERPER_URL="https://google.serper.dev/search",
        SERPER_API_KEY=SecretStr("secret-key"),
    )

    monkeypatch.setattr(google_search_module, "settings", fake_settings)
    monkeypatch.setattr(
        google_search_module.requests,
        "post",
        fake_post,
    )

    result = google_search.invoke({"query": "current events"})

    assert result == "Google search request failed: Timeout."
