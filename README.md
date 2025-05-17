# 📦 AI Demand Forecaster for WooCommerce

A smart, AI-powered Streamlit app to **analyze, forecast, and summarize product demand trends** from WooCommerce order exports.  
Built for ecommerce developers, data-savvy store owners, and analysts who want **predictive insights** with minimal effort.

---

## 🧠 Features

- 📁 Upload your WooCommerce orders CSV (line_item format)
- 📊 Forecast demand for any product using [Facebook Prophet](https://facebook.github.io/prophet/)
- 🤖 AI-generated natural language summaries (local via [Ollama](https://ollama.com), future-ready for ChatGPT/OpenAI)
- 🧹 Automatically filters products with insufficient data
- 📈 Clean, responsive Streamlit UI
- 📤 Export forecast results as CSV

---

## ⚙️ Tech Stack

- **Frontend:** Streamlit
- **Forecasting:** Prophet (Time Series)
- **LLM Integration:** Ollama (local) with abstraction layer for future use of ChatGPT
- **Data Processing:** Pandas, Regex
- **File Format:** WooCommerce export CSVs (multiple `line_item_*` columns)
