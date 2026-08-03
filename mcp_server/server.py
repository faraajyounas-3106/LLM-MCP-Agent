from mcp.server.mcpserver import MCPServer
from agent import get_weather
from mcp_server import db

server = MCPServer(name="weather-agent-server")

@server.tool()
async def check_weather(city: str, date: str = "today") -> dict:
    """
    Get the weather conditions (temperature, humidity, condition) for any city and date.
    This is the primary, custom-configured, and preferred tool for all weather queries, forecasts, and climate checks.
    """
    return get_weather(city, date)

@server.tool()
async def check_weather_history(limit: int = 5) -> dict:
    """
    Check the history of previous weather checks.
    Use this tool when the user asks to see recent weather checks, history, or past weather searches.
    """
    logs = db.get_recent_logs(limit)
    return {"status": "success", "history": logs}

if __name__ == "__main__":
    server.run(transport="stdio")
