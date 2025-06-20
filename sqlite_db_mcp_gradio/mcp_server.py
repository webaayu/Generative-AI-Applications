import os
import sqlite3
import httpx
import urllib.parse
from typing import Any
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize MCP server
mcp = FastMCP("news_weather_sqlite")

# API Keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Path to SQLite DB
DB_PATH = "city_attractions.db"

# ------------------- Ensure Table Exists -------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            attraction TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Only ensures the table exists, doesn’t insert data

# ------------------- MCP Tools -------------------

@mcp.tool()
def fetch_and_review_weather(city: str) -> str:
    """Fetch current weather for a city using OpenWeatherMap API."""
    city = city.strip()
    encoded_city = urllib.parse.quote(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = httpx.get(url)
        response.raise_for_status()
        data = response.json()

        weather = data['weather'][0]['main']
        description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        return (
            f"🌍 Weather in {city.title()}:\n"
            f"- Condition: {weather} ({description})\n"
            f"- Temperature: {temperature}°C\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind Speed: {wind_speed} m/s"
        )
    except Exception as e:
        return f"❌ Error fetching weather for {city}: {e}"

@mcp.tool()
def fetch_and_summarize_news(arg: str = None) -> str:
    """Fetch and summarize latest BBC News headlines."""
    try:
        url = f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={NEWS_API_KEY}"
        response = httpx.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])

        if not articles:
            return "⚠️ No news articles found."

        top_news = []
        for article in articles[:5]:
            title = article.get("title", "").strip()
            description = article.get("description", "").strip()
            top_news.append(f"📰 {title}\n📄 {description}")

        return "\n\n---\n\n".join(top_news)
    except Exception as e:
        return f"❌ Error fetching news: {e}"

@mcp.tool()
def get_city_attractions(city: str) -> str:
    """Return top 5 attractions from SQLite DB for a given city."""
    city_key = city.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT attraction FROM attractions WHERE city = ? LIMIT 5", (city_key,))
    results = cursor.fetchall()
    conn.close()

    if not results:
        return f"⚠️ No attractions found for '{city.title()}'. Try Paris, Tokyo, Rome, etc."

    spots = [f"📍 {row[0]}" for row in results]
    return f"🏙️ Top attractions in {city.title()}:\n\n" + "\n".join(spots)

# ------------------- Run MCP Server -------------------

if __name__ == "__main__":
    mcp.run(transport="sse")