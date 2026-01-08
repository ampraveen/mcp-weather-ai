import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MCP_BASE_URL = "http://127.0.0.1:8000"


# -----------------------------------
# Safe MCP Caller
# -----------------------------------
def safe_call_mcp(endpoint, params):
    try:
        response = requests.get(
            f"{MCP_BASE_URL}{endpoint}",
            params=params,
            timeout=5
        )

        if response.status_code != 200:
            return {
                "error": f"MCP error {response.status_code}",
                "details": response.text
            }

        return response.json()

    except requests.exceptions.ConnectionError:
        return {"error": "MCP server not running"}
    except requests.exceptions.Timeout:
        return {"error": "MCP request timeout"}
    except ValueError:
        return {"error": "Invalid JSON from MCP server"}


# -----------------------------------
# LLM Intent Detection
# -----------------------------------
def ask_llm(user_input):
    system_prompt = """
You are an AI assistant.

If the user asks about:
- weather
- climate
- temperature
- forecast

Respond ONLY in JSON:
{
  "tool": "weather",
  "city": "CityName",
  "type": "current" | "forecast"
}

Otherwise respond normally.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content


# -----------------------------------
# Main Runner
# -----------------------------------
if __name__ == "__main__":
    user_input = input("Ask me anything: ")

    llm_reply = ask_llm(user_input)
    print("🤖 LLM:", llm_reply)

    # Try parsing JSON safely
    try:
        parsed = json.loads(llm_reply)
    except json.JSONDecodeError:
        print("💬 LLM response:", llm_reply)
        exit()

    if parsed.get("tool") == "weather":
        city = parsed["city"]
        request_type = parsed.get("type", "current")

        if request_type == "forecast":
            result = safe_call_mcp("/forecast", {"city": city})
        else:
            result = safe_call_mcp("/weather", {"city": city})

        if "error" in result:
            print("❌", result["error"])
            if "details" in result:
                print(result["details"])
        else:
            print("\n📍 City:", result["city"])

            if request_type == "forecast":
                for i, day in enumerate(result["forecast"], start=1):
                    print(
                        f"Day {i}: {day['day_temperature']}°C, {day['condition']}"
                    )
            else:
                print(f"🌡️ Temperature: {result['temperature']}°C")
                print(f"☁️ Condition: {result['condition']}")
