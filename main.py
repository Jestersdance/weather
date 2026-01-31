from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ключ API OpenWeatherMap (замените на свой)
API_KEY = os.getenv("WEATHER_API_KEY", "6aeb705d7f9701500a924dd42e320595")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
    <head><title>Прогноз погоды</title></head>
    <body>
        <h1>Прогноз погоды в городах России</h1>
        <form id="weatherForm">
            <input type="text" id="city" placeholder="Введите город (например, Москва)" />
            <button type="submit">Узнать погоду</button>
        </form>
        <div id="result"></div>
        <script>
            document.getElementById("weatherForm").addEventListener("submit", async (e) => {
                e.preventDefault();
                const city = document.getElementById("city").value;
                const response = await fetch(`/api/weather?city=${city}`);
                const data = await response.json();
                document.getElementById("result").innerHTML = `
                    <p><b>${data.city}:</b> ${data.temperature}°C, ${data.description}</p>
                `;
            });
        </script>
    </body>
    </html>
    """

@app.get("/api/weather")
async def get_weather(city: str):
    params = {
        "q": f"{city},RU",
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": round(data["main"]["temp"]),
            "description": data["weather"][0]["description"]
        }
    else:
        return {"error": "Город не найден или ошибка API"}
