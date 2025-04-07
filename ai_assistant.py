import streamlit as st
import os
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
from gtts import gTTS
import tempfile
import speech_recognition as sr
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyDXACe0tXmUKnSqKd3RZCarT2HXJaGETxc"  # Replace with your actual Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# News API Key
NEWS_API_KEY = "55f8b079335a4cdda914e2a67621de7a"  # Replace with your actual News API key from newsapi.org

# File handling for fine-tuning and CSV data
def load_fine_tuning_data():
    fine_tuning_file = 'tune_data.txt'
    return open(fine_tuning_file, 'r').read() if os.path.exists(fine_tuning_file) else ""

def load_csv_data():
    csv_file = 'data.csv'
    return pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame()

fine_tuning_data = load_fine_tuning_data()
csv_data = load_csv_data()

# Stock information and charting
def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = stock.history(period='1d')['Close'].iloc[-1]
        company_name = info.get('longName', 'Unknown Company')
        return f"{company_name} (${ticker}) - Current Price: ${current_price:.2f}"
    except Exception as e:
        return f"Error fetching {ticker}: {str(e)}"

def generate_stock_chart(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)
    
    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                         open=hist['Open'],
                                         high=hist['High'],
                                         low=hist['Low'],
                                         close=hist['Close'])])
    fig.update_layout(title=f'{ticker} Stock Price (Past Year)', xaxis_title='Date', yaxis_title='Price')
    return fig

# Fetch real news data using News API
def get_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}+finance+stocks+markets+-sports+-entertainment&apiKey={NEWS_API_KEY}&language=en&sortBy=publishedAt&pageSize=5"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            if not articles:
                return "No recent finance-related news found for this query."
            return articles
        else:
            return f"News API error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error fetching news: {str(e)}"

# Finance-related check
def is_finance_related(prompt):
    finance_keywords = ["finance", "stock", "investment", "money", "bank", "credit", "loan", "insurance", "budget", 
                        "saving", "debt", "economy", "market", "fund", "portfolio", "dividend", "asset", "liability", 
                        "interest", "mortgage", "tax", "retirement", "401k", "IRA"]
    return any(keyword in prompt.lower() for keyword in finance_keywords)

# AI response generation with increased context length
def generate_ai_response(prompt):
    greeting_responses = {
        "hi": "Hello! How can I assist you with your financial queries today?",
        "hello": "Hi there! I'm here to help with finance, stocks, or insurance. What’s on your mind?"
    }
    
    # Handle greetings
    prompt_lower = prompt.lower().strip()
    if prompt_lower in greeting_responses:
        return greeting_responses[prompt_lower]

    # Restrict to finance-related queries
    if not is_finance_related(prompt):
        return "I’m specialized in finance-related topics like stocks, investments, and insurance. Please ask a finance-related question!"

    # Build detailed context
    context = f"""You are an expert AI Financial Assistant specializing in personal finance, insurance, credit scoring, stocks, and investments. 
    Provide detailed, accurate, and comprehensive responses only to finance-related questions. For non-finance queries, politely redirect the user to financial topics.

    Additional Information:
    - Fine-tuning Data: {fine_tuning_data if fine_tuning_data else "No fine-tuning data available."}
    - CSV Data: {csv_data.to_string() if not csv_data.empty else "No CSV data available."}
    
    For stock-related queries, include real-time stock information where applicable."""

    # Add stock info if relevant
    stock_info = ""
    if "stock" in prompt_lower or "$" in prompt:
        words = prompt.replace("$", "").split()
        potential_tickers = [word.upper() for word in words if word.isalpha() and len(word) <= 5]
        for ticker in potential_tickers:
            stock_info += get_stock_info(ticker) + "\n"
        if stock_info:
            prompt += f"\n\nStock Information:\n{stock_info}"

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        full_prompt = f"{context}\n\nUser Query: {prompt}\n\nProvide a detailed response (at least 150 words if possible):"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I’m your AI Financial Assistant. How can I assist you with financial matters today?"}]

# Text-to-speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# Speech-to-text
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Please speak.")
        audio = r.listen(source)
        st.write("Processing...")
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn’t understand the audio."
    except sr.RequestError:
        return "Error processing speech."

# Theme setting
def set_theme(theme):
    if theme == "dark":
        st.markdown("""
        <style>
        .stApp { background-color: #1E1E1E; color: #FFFFFF; }
        .stButton>button { color: #FFFFFF; background-color: #4CAF50; border-radius: 5px; }
        .stTextInput>div>div>input { color: #FFFFFF; background-color: #2E2E2E; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; color: #000000; }
        .stButton>button { color: #000000; background-color: #4CAF50; border-radius: 5px; }
        .stTextInput>div>div>input { color: #000000; background-color: #F0F0F0; }
        </style>
        """, unsafe_allow_html=True)

# Main application
def ai_assistant():
    st.title("AI Financial Assistant")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        theme = st.radio("Theme", ("Light", "Dark"))
        set_theme(theme.lower())
        
        st.button("Clear Chat", on_click=clear_chat_history)
        
        uploaded_txt = st.file_uploader("Upload Fine-Tuning Data (TXT)", type="txt")
        if uploaded_txt:
            fine_tuning_data = uploaded_txt.getvalue().decode("utf-8")
            with open('tune_data.txt', 'w') as f:
                f.write(fine_tuning_data)
            st.success("Fine-tuning data uploaded!")

        uploaded_csv = st.file_uploader("Upload CSV Data", type="csv")
        if uploaded_csv:
            csv_data = pd.read_csv(uploaded_csv)
            csv_data.to_csv('data.csv', index=False)
            st.success("CSV data uploaded!")

        st.subheader("Stock Chart")
        stock_ticker = st.text_input("Stock Ticker (e.g., AAPL):", key="chart_ticker")
        if stock_ticker:
            st.plotly_chart(generate_stock_chart(stock_ticker))

    # Chat initialization
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I’m your AI Financial Assistant. How can I assist you with financial matters today?"}]

    # Chat interface
    chat_container = st.container()
    with st.container():
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            user_input = st.chat_input("Ask about finance, stocks, or insurance:")
        with col2:
            if st.button("🎤"):
                user_input = speech_to_text()
                st.write(f"You said: {user_input}")

    # Process input
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = generate_ai_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display real news tied to the query
        if is_finance_related(user_input):
            news = get_news(user_input)
            if isinstance(news, list) and news:
                st.subheader("📰 Latest Finance News")
                for article in news:
                    st.write(f"**{article['title']}**")
                    st.write(article['description'] or "No description available.")
                    if article.get('urlToImage'):
                        st.image(article['urlToImage'], width=200, caption="News Image")
                    st.write(f"[Read more]({article['url']})")
                    st.write(f"Published: {article['publishedAt']}")
                    st.write("---")
            elif isinstance(news, str):
                st.warning(news)  # Display error or no-news message
            else:
                st.warning("No relevant news found.")

    # Display chat history
    with chat_container:
        for i, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if st.button("🔊", key=f"play_{i}"):
                    audio_file = text_to_speech(msg["content"])
                    st.audio(audio_file)

if __name__ == "__main__":
    ai_assistant()
