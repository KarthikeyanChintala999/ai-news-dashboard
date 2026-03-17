from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


async def summarize_article(text: str):

    prompt = f"""
    Summarize the following AI news article in 3 bullet points.

    Article:
    {text}
    """

    completion = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "system", "content": "You summarize AI news."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return completion.choices[0].message.content