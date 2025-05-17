import pandas as pd
import re

def preprocess_orders(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=lambda x: x.lower().strip())

    line_item_cols = [col for col in df.columns if col.startswith("line_item")]
    parsed_rows = []

    for _, row in df.iterrows():
        order_date = pd.to_datetime(row["order_date"])
        for col in line_item_cols:
            val = row[col]
            if isinstance(val, str) and "×" in val:
                match = re.match(r"(.+?) × (\d+)", val.strip())
                if match:
                    product_name, qty = match.groups()
                    parsed_rows.append({
                        "order_date": order_date,
                        "product_name": product_name.strip(),
                        "quantity": int(qty)
                    })

    return pd.DataFrame(parsed_rows)


def get_forecastable_products(df: pd.DataFrame, min_points: int = 2) -> list:
    grouped = (
        df.groupby("product_name")
        .agg(non_nan_points=("quantity", lambda x: x.dropna().shape[0]))
        .reset_index()
    )
    valid = grouped[grouped["non_nan_points"] >= min_points]
    return valid["product_name"].tolist()
