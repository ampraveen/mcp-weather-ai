import requests

def ask_weather(city):
    url = "http://127.0.0.1:8000/weather"
    response = requests.get(url, params={"city": city})

    data = response.json()

    if "error" in data:
        print("❌ City not found")
    else:
        print(f"🌍 City: {data['city']}")
        print(f"🌡️ Temperature: {data['temperature']}°C")
        print(f"☁️ Condition: {data['condition']}")

if __name__ == "__main__":
    city = input("Enter city name: ")
    ask_weather(city)
