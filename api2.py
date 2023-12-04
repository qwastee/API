from fastapi import FastAPI, HTTPException, Query
from bs4 import BeautifulSoup
import httpx
from collections import Counter
from pydantic import BaseModel

app = FastAPI()

class ProcessTextRequest(BaseModel):
    website_url: str = Query(..., description="URL of the website to process")

@app.post("/process_text")
async def process_text(request: ProcessTextRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(request.website_url)
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Failed to fetch website")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch website")

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip()
        words = title.split()
        most_common_word = max(set(words), key=words.count)
        longest_word = max(words, key=len)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing website content: {str(e)}")

    # Используем Counter для подсчета частоты слов в заголовке
    title_word_counts = dict(Counter(words))

    # Вывод результатов
    return {
        "title": title,
        "most_common_word_in_title": most_common_word,
        "longest_word_in_title": longest_word,
        "title_word_counts": title_word_counts
    }
