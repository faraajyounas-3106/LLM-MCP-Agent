from mcp_server.agent import get_weather
from mcp_server import db
import json

def test_db_logging():
    print("--- 1. Making first request for Dubai ---")
    result1 = get_weather("Dubai")
    print(f"Status: {result1['status']}")
    
    print("\n--- 2. Making second request for Dubai ---")
    result2 = get_weather("Dubai")
    print(f"Status: {result2['status']}")
    
    print("\n--- 3. Making request for Atlantis-Fake-City ---")
    result_fake = get_weather("Atlantis-Fake-City")
    print(f"Status: {result_fake['status']}")
    
    print("\n--- 4. Fetching recent database logs ---")
    logs = db.get_recent_logs(10)
    print(json.dumps(logs, indent=2))

if __name__ == "__main__":
    test_db_logging()
