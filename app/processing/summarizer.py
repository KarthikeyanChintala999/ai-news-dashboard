from openai import OpenAI
from app.config import settings

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


async def summarize_article(title, text):

    prompt = f"""
You are an AI news analyst.

Analyze the following article and produce structured output.

TITLE:
{title}

CONTENT:
{text}

Return JSON with:

ai_summary
tldr_quick
tldr_technical
tags
impact_score
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content