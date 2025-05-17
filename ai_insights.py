import ollama

class OllamaProvider:
    def summarize_forecast(self, forecast_df, product_name):
        prompt = f"""Analyze this demand forecast for '{product_name}' and summarize any trends, spikes, or drops in simple terms. Include possible reasons if applicable.

        {forecast_df.tail(10).to_string(index=False)}
        """
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
 