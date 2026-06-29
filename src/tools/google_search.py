import requests
from pydantic import SecretStr
from requests import RequestException

from langchain_core.tools import tool

from core.config import settings


REQUEST_TIMEOUT_SECONDS = 10

@tool
def google_search(query: str) -> str:
    """
    Search Google for real-time information.
    Use this when you need to find news, facts, or current events.
    """
    normalized_query = query.strip()
    if not normalized_query:
        return "Search query cannot be empty."

    url = settings.SERPER_URL
    api_key = settings.SERPER_API_KEY.get_secret_value()
    if not url or not api_key:
        return "Google search is not configured. Please set SERPER_URL and SERPER_API_KEY."

    payload = {"q": normalized_query, "num": 5}
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        results = response.json()
    except RequestException as exc:
        return f"Google search request failed: {exc.__class__.__name__}."
    except ValueError:
        return "Google search request failed: invalid JSON response."

    snippets = []
    for result in results.get("organic", []):
        title = result.get("title") or "Untitled"
        link = result.get("link") or "No link"
        snippet = result.get("snippet") or "No snippet"
        snippets.append(
            f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n---"
        )

    return "\n".join(snippets) if snippets else "No results found."
