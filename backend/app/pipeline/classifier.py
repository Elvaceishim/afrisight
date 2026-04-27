from typing import Any

from sentence_transformers import SentenceTransformer, util

_model: SentenceTransformer | None = None

CATEGORY_ANCHORS: dict[str, list[str]] = {
    "regulatory": [
        "central bank regulation fintech",
        "government policy mobile money",
        "financial regulation compliance Africa",
        "licensing fintech operator",
    ],
    "funding": [
        "startup funding investment Africa",
        "venture capital fintech round",
        "seed series funding raised",
        "investors backing African startup",
    ],
    "product_launch": [
        "new product launch fintech",
        "app feature release mobile banking",
        "service launched payment platform",
        "product update digital wallet",
    ],
    "macro_risk": [
        "inflation currency risk Africa",
        "economic downturn recession",
        "political instability financial risk",
        "foreign exchange volatility",
    ],
    "payments": [
        "mobile payment transfer send money",
        "remittance cross-border payment",
        "merchant payment point of sale",
        "digital wallet transaction",
    ],
    "other": [
        "general fintech news Africa",
        "financial technology overview",
    ],
}


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model


def classify_article(article: dict[str, Any]) -> dict[str, Any]:
    model = _get_model()
    text = " ".join(filter(None, [article.get("title", ""), article.get("content", "")]))[:2000]

    text_emb = model.encode(text, convert_to_tensor=True)

    best_category = "other"
    best_score = -1.0

    for category, anchors in CATEGORY_ANCHORS.items():
        anchor_embs = model.encode(anchors, convert_to_tensor=True)
        scores = util.cos_sim(text_emb, anchor_embs)
        max_score = float(scores.max())
        if max_score > best_score:
            best_score = max_score
            best_category = category

    return {
        "classifier_category": best_category,
        "classifier_score": round(best_score, 4),
    }
