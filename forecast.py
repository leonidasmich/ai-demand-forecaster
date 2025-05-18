from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

def forecast_product_demand(df: pd.DataFrame, product_name: str, forecast_days: int = 30):
    product_df = df[df["product_name"] == product_name]
    daily = product_df.groupby("order_date")["quantity"].sum().reset_index()
    daily = daily.rename(columns={"order_date": "ds", "quantity": "y"})

    daily = daily.dropna()
    if len(daily) < 2:
        raise ValueError(f"Not enough data to forecast for '{product_name}'.")

    model = Prophet()
    model.fit(daily)

    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)

    fig = model.plot(forecast)
    return forecast, fig
