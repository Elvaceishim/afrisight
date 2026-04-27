import json
import logging
import re
from typing import Any

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from app.config import get_settings

logger = logging.getLogger(__name__)

PROMPT_VERSION = "v1"

_TEMPLATE = """\
You are an African fintech intelligence analyst. Analyze the following news article and respond with ONLY a valid JSON object — no markdown, no explanation.

Article title: {title}
Article content: {content}

Return this exact JSON structure:
{{
  "market": "<one of: ng, ke, tz, cd, et, pan-african, unknown>",
  "category": "<one of: regulatory, funding, product_launch, macro_risk, payments, other>",
  "sentiment": "<one of: positive, negative, neutral>",
  "summary": "<2-sentence max summary of the article>",
  "confidence_score": <float between 0.0 and 1.0 indicating how confident you are in this classification>
}}
"""

_prompt = PromptTemplate(
    input_variables=["title", "content"],
    template=_TEMPLATE,
)


def _get_chain():
    settings = get_settings()
    llm = ChatOpenAI(
        model=settings.openrouter_model,
        openai_api_key=settings.openrouter_api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        max_tokens=512,
    )
    return _prompt | llm | StrOutputParser()


def analyze_article(article: dict[str, Any]) -> dict[str, Any]:
    chain = _get_chain()
    raw = chain.invoke(
        {
            "title": article.get("title", ""),
            "content": article.get("content", "")[:3000],
        }
    )
    # Strip any accidental markdown fencing
    raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Failed to parse LLM JSON response: %s", raw[:200])
        result = {
            "market": "unknown",
            "category": "other",
            "sentiment": "neutral",
            "summary": article.get("title", ""),
            "confidence_score": 0.0,
        }
    result["prompt_version"] = PROMPT_VERSION
    return result
