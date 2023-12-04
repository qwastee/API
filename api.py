from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import httpx

app = FastAPI()

@app.post("/parse_text")
async def parse_text(website_url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(website_url)
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Failed to fetch website")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch website")

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing website content: {str(e)}")

    return {"title": title}
