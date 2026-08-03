import asyncio
from mcp_server.server import server

async def main():
    print("Listing registered tools:")
    tools = await server.list_tools()
    for tool in tools:
        print(f"Tool Name: {tool.name}")
        print(f"Description: {tool.description}")
        print(f"Input Schema: {tool.input_schema}\n")

    print("Calling check_weather for Dubai on Friday:")
    result = await server.call_tool("check_weather", {"city": "Dubai", "date": "Friday"})
    print("Result:", result)

    print("\nCalling check_weather for a city not in database (e.g., Paris):")
    result_not_found = await server.call_tool("check_weather", {"city": "Paris"})
    print("Result:", result_not_found)

if __name__ == "__main__":
    asyncio.run(main())
