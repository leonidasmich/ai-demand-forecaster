import streamlit as st
import pandas as pd
from forecast import forecast_product_demand
from ai_insights import OllamaProvider
from utils import preprocess_orders, get_forecastable_products

st.set_page_config(page_title="AI Demand Forecasting", layout="wide")
st.title("📦 AI Demand Forecaster for WooCommerce")

uploaded_file = st.file_uploader("Upload your WooCommerce Orders CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    cleaned_df = preprocess_orders(df)

    valid_products = get_forecastable_products(cleaned_df)
    
    if valid_products:
        st.info("🔍 Showing only products with enough data for forecasting (2+ records)")
        product = st.selectbox("Select a product", valid_products)

        if st.button("Generate Forecast"):
            forecast_df, fig = forecast_product_demand(cleaned_df, product)
            st.pyplot(fig)

            ai = OllamaProvider()
            summary = ai.summarize_forecast(forecast_df, product)

            st.subheader("🧠 AI Summary")
            st.write(summary)

            st.download_button("Download Forecast CSV", forecast_df.to_csv(index=False), "forecast.csv")
    else:
        st.warning("No products have enough data to generate a forecast.")
