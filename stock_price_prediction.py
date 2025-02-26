import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import datetime
from datetime import date
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_absolute_error

def stock():

    def set_background(image_url):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url({image_url});
                background-size: cover;
                background-position: top;
                background-repeat:repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    set_background("https://img.freepik.com/free-vector/paper-style-white-monochrome-background_52683-66443.jpg")
    
    st.markdown("""
    <style>
            html{
                font-family: Manrope;
                }
            .e1nzilvr2{
                text-align:center;
                text-shadow: 0px 2px 5.3px rgba(0, 0, 0, 0.19);
                font-family: Manrope;
                font-size: 102;
                font-style: normal;
                font-weight: 600;
                line-height: 100%; 
                letter-spacing: -2.16px;
                opacity: 0;
                animation: fadeIn 2s forwards;
                }
             .ea3mdgi5{
                max-width:100%;
                }
            
            
    </style>
        """, unsafe_allow_html=True)
    
    st.title('Stock Price Predictions')
    st.sidebar.info('Welcome to the Stock Price Prediction App. Choose your options below')

    @st.cache_resource
    def download_data(op, start_date, end_date):
        df = yf.download(op, start=start_date, end=end_date, progress=False)
        return df

    option = st.sidebar.text_input('Enter a Stock Symbol', value='SPY')
    option = option.upper()
    today = datetime.date.today()
    duration = st.sidebar.number_input('Enter the duration', value=3000)
    before = today - datetime.timedelta(days=duration)
    start_date = st.sidebar.date_input('Start Date', value=before)
    end_date = st.sidebar.date_input('End date', today)
    if st.sidebar.button('Send'):
        if start_date < end_date:
            st.sidebar.success('Start date: %s\n\nEnd date: %s' % (start_date, end_date))
            data = download_data(option, start_date, end_date)
        else:
            st.sidebar.error('Error: End date must fall after start date')
            return

    data = download_data(option, start_date, end_date)
    if data.empty:
        st.error("No data found for the given stock symbol and date range.")
        return

    scaler = StandardScaler()

    def calculate_indicators(df):
        """Calculate technical indicators manually using pandas"""
        # Create a copy of the dataframe with just the Close prices
        result = pd.DataFrame(index=df.index)
        result['Close'] = df['Close']
        
        # SMA - Simple Moving Average
        result['SMA'] = df['Close'].rolling(window=14).mean()
        
        # EMA - Exponential Moving Average
        result['EMA'] = df['Close'].ewm(span=14, adjust=False).mean()
        
        # RSI - Relative Strength Index
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        
        # Handle division by zero
        rs = avg_gain / avg_loss.replace(0, np.nan)
        result['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD - Moving Average Convergence Divergence
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        result['MACD'] = exp1 - exp2
        
        return result

    def tech_indicators():
        st.header('Technical Indicators')
        indicator_option = st.radio('Choose a Technical Indicator to Visualize', ['Close', 'MACD', 'RSI', 'SMA', 'EMA'])

        try:
            # Calculate indicators using our custom function
            indicators_df = calculate_indicators(data)
            
            if indicator_option == 'Close':
                st.write('Close Price')
                st.line_chart(indicators_df['Close'])
            elif indicator_option == 'MACD':
                st.write('Moving Average Convergence Divergence')
                st.line_chart(indicators_df['MACD'])
            elif indicator_option == 'RSI':
                st.write('Relative Strength Indicator')
                st.line_chart(indicators_df['RSI'])
            elif indicator_option == 'SMA':
                st.write('Simple Moving Average')
                st.line_chart(indicators_df['SMA'])
            else:
                st.write('Exponential Moving Average')
                st.line_chart(indicators_df['EMA'])
        except Exception as e:
            st.error(f"An error occurred while calculating technical indicators: {e}")

    def dataframe():
        st.header('Recent Data')
        st.dataframe(data.tail(10))

    def model_engine(model, num):
        df = data[['Close']].copy()
        df['preds'] = df.Close.shift(-num)
        
        # Drop NaN values
        df = df.dropna()
        
        if len(df) <= num:
            st.error(f"Not enough data points for prediction. Need more than {num} data points.")
            return
            
        # Use all available data except last 'num' rows for training
        train_data = df.iloc[:-num].copy()
        forecast_data = df.iloc[-num:, :-1].copy()  # Last 'num' rows without 'preds' column
        
        # Prepare training data
        X = train_data.drop('preds', axis=1).values
        y = train_data['preds'].values
        
        # Standardize features
        scaler_model = StandardScaler()
        X_scaled = scaler_model.fit_transform(X)
        
        # Split data for training and testing
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=7)
        
        # Train model
        model.fit(X_train, y_train)
        
        # Make predictions on test set
        test_preds = model.predict(X_test)
        
        # Calculate metrics
        r2 = r2_score(y_test, test_preds)
        mae = mean_absolute_error(y_test, test_preds)
        
        st.text(f'Model Performance:\nr2_score: {r2:.4f}\nMAE: {mae:.4f}')
        
        # Prepare forecast data
        forecast_scaled = scaler_model.transform(forecast_data.values)
        forecast_pred = model.predict(forecast_scaled)
        
        # Display forecast
        st.subheader(f"{num}-Day Price Forecast")
        
        # Create a forecast dataframe for better presentation
        forecast_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=num)
        forecast_df = pd.DataFrame({
            'Day': [f'Day {i+1}' for i in range(num)],
            'Date': [d.strftime('%Y-%m-%d') for d in forecast_dates],
            'Predicted Price': [f'${price:.2f}' for price in forecast_pred]
        })
        
        st.table(forecast_df)

    def predict():
        model = st.radio('Choose a model', ['LinearRegression', 'RandomForestRegressor', 'ExtraTreesRegressor', 'KNeighborsRegressor', 'XGBoostRegressor'])
        num = st.number_input('How many days forecast?', value=5)
        num = int(num)
        if st.button('Predict'):
            if model == 'LinearRegression':
                engine = LinearRegression()
            elif model == 'RandomForestRegressor':
                engine = RandomForestRegressor()
            elif model == 'ExtraTreesRegressor':
                engine = ExtraTreesRegressor()
            elif model == 'KNeighborsRegressor':
                engine = KNeighborsRegressor()
            else:
                engine = XGBRegressor()
            model_engine(engine, num)

    option = st.sidebar.selectbox('Make a choice', ['Visualize', 'Recent Data', 'Predict'])
    if option == 'Visualize':
        tech_indicators()
    elif option == 'Recent Data':
        dataframe()
    else:
        predict()

if __name__ == '__main__':
    stock()
