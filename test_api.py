from mcp_server.agent import get_weather
import json

def run_tests():
    print("--- Test 1: Fetching weather for Dubai ---")
    result_dubai = get_weather("Dubai")
    print(json.dumps(result_dubai, indent=2))
    
    print("\n--- Test 2: Fetching weather for Atlantis-Fake-City ---")
    result_fake = get_weather("Atlantis-Fake-City")
    print(json.dumps(result_fake, indent=2))
    
    print("\n--- Test 3: Fetching weather for London on a specific date (e.g., Friday) ---")
    result_date = get_weather("London", "Friday")
    print(json.dumps(result_date, indent=2))

if __name__ == "__main__":
    run_tests()
