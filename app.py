import streamlit as st
import yfinance as yf
import openai
import os

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'Name': info.get('longName', 'N/A'),
            'Sector': info.get('sector', 'N/A'),
            'Price': info.get('currentPrice', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            'PE Ratio': info.get('trailingPE', 'N/A'),
            'Dividend Yield': info.get('dividendYield', 'N/A'),
            '52W High': info.get('fiftyTwoWeekHigh', 'N/A'),
            '52W Low': info.get('fiftyTwoWeekLow', 'N/A'),
        }
    except Exception as e:
        return {"error": str(e)}

def generate_summary(ticker, data):
    prompt = f"""
    Generate an equity research summary for {ticker} using the following data:
    {data}
    Include valuation insight, business model, and sector relevance.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error generating summary: {str(e)}"

st.set_page_config(page_title="Equity Research Agent", layout="centered")
st.title("📊 AI Equity Research Agent")

ticker_input = st.text_input("Enter Stock Ticker (e.g., INFY.NS, TCS.NS)")

if ticker_input:
    with st.spinner("Fetching data and generating insights..."):
        data = fetch_stock_data(ticker_input.upper())
        if "error" in data:
            st.error(f"Error: {data['error']}")
        else:
            st.subheader("📌 Stock Data")
            st.json(data)

            st.subheader("🧠 AI Summary")
            summary = generate_summary(ticker_input.upper(), data)
            st.markdown(summary)
