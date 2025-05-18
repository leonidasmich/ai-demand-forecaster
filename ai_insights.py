import streamlit as st
import ollama

@st.cache_data(show_spinner=False)
def summarize_forecast_with_cache(product_name: str, forecast_tail_csv: str) -> str:
    prompt = f"""
        Analyze the demand forecast for the product "{product_name}" and provide:

        1. A summary of the overall trend (e.g., growth, decline, stability, unusual patterns).
        2. An interpretation of any seasonality components (e.g., weekly or monthly peaks and dips).
        3. Practical recommendations for inventory planning or marketing strategy.
        4. Include possible reasons if applicable.
        5. If the forecast shows a significant increase or decrease, suggest a percentage change in inventory.
        6. If the forecast shows a seasonal peak, suggest the best time for a promotional campaign.

        Here is the forecast data (last 30 days of predictions):
        {forecast_tail_csv}
        """
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']
