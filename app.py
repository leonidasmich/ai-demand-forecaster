import streamlit as st
import pandas as pd
from forecast import forecast_product_demand
from ai_insights import summarize_forecast_with_cache
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
        selected_products = st.multiselect(
            "Select products to forecast", valid_products,
            default=valid_products[0] if valid_products else None,
        )

        forecast_days = st.selectbox("📆 Forecast range", [7, 30, 90, 180, 360], index=1)

        if st.button("Generate Forecast"):
            tabs = st.tabs([f"📦 {product}" for product in selected_products])

            for i, product in enumerate(selected_products):
                with tabs[i]:
                    st.markdown(f"### 📈 Forecast for **{product}**")

                    try:
                        # Run forecast
                        forecast_df, fig, model = forecast_product_demand(cleaned_df, product, forecast_days)
                        st.pyplot(fig, use_container_width=True)

                        # Seasonality components
                        st.subheader("📆 Seasonality Components")
                        seasonality_fig = model.plot_components(forecast_df)
                        seasonality_fig.set_size_inches(8, 4)
                        st.pyplot(seasonality_fig, use_container_width=True)

                        # Cached AI summary
                        forecast_tail = forecast_df.tail(30).to_csv(index=False)
                        summary = summarize_forecast_with_cache(product, forecast_tail)
                        st.subheader("🧠 AI Forecast & Seasonality Summary")
                        st.write(summary)

                        st.success(f"✅ Forecast generated for {forecast_days} days.")

                        st.download_button(
                            f"Download Forecast CSV - {product}",
                            forecast_df.to_csv(index=False),
                            file_name=f"{product.replace(' ', '_')}_forecast.csv"
                        )
                    except ValueError as e:
                        st.warning(f"{product}: {str(e)}")
    else:
        st.warning("No products have enough data to generate a forecast.")
