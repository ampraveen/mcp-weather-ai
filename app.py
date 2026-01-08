import streamlit as st
import requests

MCP_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="🌤 MCP Weather AI", layout="centered")

st.title("🌍 MCP Weather AI App")
st.write("Powered by MCP + LLM + OpenWeather")

city = st.text_input("Enter City Name").strip()


def safe_get_json(url, params):
    try:
        response = requests.get(url, params=params, timeout=5)

        # HTTP error
        if response.status_code != 200:
            try:
                error = response.json().get("detail", response.text)
            except ValueError:
                error = response.text

            st.error(f"❌ {error}")
            return None

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error("❌ MCP Server is not running")
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out")
    except ValueError:
        st.error("❌ Invalid JSON response from server")

    return None


if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name")
        st.stop()

    # ----------------------
    # Current Weather
    # ----------------------
    current = safe_get_json(
        f"{MCP_BASE_URL}/weather",
        {"city": city}
    )

    if not current:
        st.stop()

    st.subheader(f"📍 Current Weather in {city}")
    st.metric("🌡 Temperature", f"{current['temperature']} °C")
    st.write("☁️ Condition:", current["condition"])

    # ----------------------
    # 7-Day Forecast
    # ----------------------
    forecast = safe_get_json(
        f"{MCP_BASE_URL}/forecast",
        {"city": city}
    )

    if not forecast:
        st.stop()

    st.subheader("📅 7-Day Forecast")

    # 🔐 CRITICAL SAFETY CHECK
    if "forecast" not in forecast:
        st.warning(forecast.get("detail", "7-day forecast not available"))
        st.stop()

    for i, day in enumerate(forecast["forecast"], start=1):
        st.write(
            f"**Day {i}** → 🌡 {day['day_temperature']}°C | ☁️ {day['condition']}"
        )
