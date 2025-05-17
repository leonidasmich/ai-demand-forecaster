from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

def forecast_product_demand(df: pd.DataFrame, product_name: str):
    product_df = df[df["product_name"] == product_name]
    daily = product_df.groupby("order_date")["quantity"].sum().reset_index()
    daily = daily.rename(columns={"order_date": "ds", "quantity": "y"})
    
    model = Prophet()
    model.fit(daily)
    
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    fig = model.plot(forecast)
    return forecast, fig