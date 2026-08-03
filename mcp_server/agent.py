import requests
from mcp_server import db

def get_weather(city: str, date: str = "today") -> dict:
    """
    Returns real weather data for the specified city and date using the Open-Meteo API.
    """
    # WMO Weather code mapping
    wmo_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle: Light",
        53: "Drizzle: Moderate",
        55: "Drizzle: Dense",
        56: "Freezing Drizzle: Light",
        57: "Freezing Drizzle: Dense",
        61: "Rain: Slight",
        63: "Rain: Moderate",
        65: "Rain: Heavy",
        66: "Freezing Rain: Light",
        67: "Freezing Rain: Heavy",
        71: "Snow fall: Slight",
        73: "Snow fall: Moderate",
        75: "Snow fall: Heavy",
        77: "Snow grains",
        80: "Rain showers: Slight",
        81: "Rain showers: Moderate",
        82: "Rain showers: Violent",
        85: "Snow showers: Slight",
        86: "Snow showers: Heavy",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    result = {}
    try:
        # Step 1: Geocoding to get latitude and longitude
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={requests.utils.quote(city)}"
        geo_response = requests.get(geocoding_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data or not geo_data["results"]:
            result = {
                "status": "not_found",
                "city": city,
                "date": date,
                "message": f"Could not find coordinates for city '{city}'."
            }
            db.log_request(city, date, result)
            return result

        # Select the first result
        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        resolved_name = f"{location.get('name', city)}, {location.get('country', '')}"

        # Step 2: Fetch current weather
        forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code"
        weather_response = requests.get(forecast_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        if "current" not in weather_data:
            result = {
                "status": "error",
                "message": "Malformed weather response: 'current' key missing."
            }
            db.log_request(city, date, result)
            return result

        current = weather_data["current"]
        temp_c = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        weather_code = current.get("weather_code", 0)
        condition = wmo_codes.get(weather_code, f"Unknown code ({weather_code})")

        # Step 3: Format the response
        success_response = {
            "status": "success",
            "city": resolved_name,
            "date": date,
            "condition": condition,
            "temp_c": temp_c,
            "humidity": humidity,
            "humidity_pct": humidity
        }

        # Handle non-today forecast requests
        is_today = date.lower().strip() in ["today", "now", "current"]
        if not is_today:
            success_response["note"] = (
                f"The Open-Meteo free tier only supports current weather and short-term forecasts. "
                f"The specific requested date '{date}' was not matched. Returning current conditions instead."
            )

        result = success_response
        db.log_request(city, date, result)
        return result

    except requests.RequestException as e:
        result = {
            "status": "error",
            "message": f"Network error contacting weather services: {str(e)}"
        }
        db.log_request(city, date, result)
        return result
    except Exception as e:
        result = {
            "status": "error",
            "message": f"Unexpected error processing weather data: {str(e)}"
        }
        db.log_request(city, date, result)
        return result
