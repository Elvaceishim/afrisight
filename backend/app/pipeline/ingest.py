import logging
from datetime import datetime, timedelta
from typing import Any

from newsapi import NewsApiClient

from app.config import get_settings

logger = logging.getLogger(__name__)

KEYWORDS = [
    "M-Pesa",
    "mobile money Africa",
    "remittance Africa",
    "Flutterwave",
    "Paystack",
    "fintech Nigeria",
    "fintech Kenya",
    "fintech Tanzania",
    "fintech Ethiopia",
    "fintech DRC",
]


def fetch_articles() -> list[dict[str, Any]]:
    settings = get_settings()
    client = NewsApiClient(api_key=settings.news_api_key)
    seen_urls: set[str] = set()
    articles: list[dict[str, Any]] = []

    from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

    for keyword in KEYWORDS:
        try:
            response = client.get_everything(
                q=keyword,
                language="en",
                sort_by="publishedAt",
                from_param=from_date,
                page_size=10,
            )
            for item in response.get("articles", []):
                url = item.get("url", "")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                content = " ".join(
                    filter(None, [item.get("title"), item.get("description"), item.get("content")])
                )
                articles.append(
                    {
                        "title": item.get("title", ""),
                        "url": url,
                        "content": content,
                        "published_at": item.get("publishedAt", ""),
                        "source": item.get("source", {}).get("name", ""),
                    }
                )
        except Exception as exc:
            logger.warning("Failed to fetch articles for keyword '%s': %s", keyword, exc)

    return articles
