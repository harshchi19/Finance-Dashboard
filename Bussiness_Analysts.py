import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
from numerize.numerize import numerize
import plotly.graph_objs as go
import time
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from scipy import stats
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go
fig = go.Figure()
from BUSINESS_LOCATIONS import bussiness_loc
from DESCRIPTIVE_STATISTICS import des_stat
from REGRESSION_ANALYSIS import reg_analysis
from SALES_BY_DATE import sales


# Set the page configuration at the very beginning
# st.set_page_config(page_title="InfoFinance", layout="wide")
# Load custom CSS for both the pages
with open('style_bussiness.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Covariance Analysis Function
def covariance_analysis():
    st.header("COVARIANCE FOR TWO RANDOM VARIABLES")
    st.success("The main objective is to measure if Number of family dependents or Wives may influence a person to supervise many projects")

    # Load the Excel data
    def load_data():
        return pd.read_excel('regression.xlsx')
    
    df = load_data()
    
    selected_column = st.selectbox('SELECT INPUT X FEATURE', df.select_dtypes("number").columns)
    X = sm.add_constant(df[selected_column])  # Adding a constant for intercept

    # Fitting the model
    model = sm.OLS(df['Projects'], X).fit()

    # Displaying the metrics
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric("INTERCEPT:", f"{model.params[0]:,.4f}")
    c2.metric("R SQUARED", f"{model.rsquared:,.2f}", delta="is it strong relationship?")
    c3.metric("ADJUSTED R", f"{model.rsquared_adj:,.3f}")
    c4.metric("STANDARD ERROR", f"{model.bse[0]:,.4f}")
    
    style_metric_cards(background_color="#FFFFFF", border_left_color="#686664")
    
    # Displaying the data table and scatter plot with regression line
    b1, b2 = st.columns(2)
    data = {
        'X feature': selected_column,
        'Prediction': model.predict(X),
        'Residuals': model.resid
    }
    dt = pd.DataFrame(data)
    b1.dataframe(dt, use_container_width=True)
    
    with b2:
        plt.figure(figsize=(8, 6))
        plt.scatter(df[selected_column], df['Projects'], label='Actual')
        plt.plot(df[selected_column], model.predict(X), color='red', label='Predicted')
        plt.xlabel(selected_column)
        plt.ylabel('Projects')
        plt.title(f'Line of Best Fit ({selected_column} vs Projects)')
        plt.grid(color='grey', linestyle='--')
        plt.legend()

        # Setting outer border color
        plt.gca().spines['top'].set_color('gray')
        plt.gca().spines['bottom'].set_color('gray')
        plt.gca().spines['left'].set_color('gray')
        plt.gca().spines['right'].set_color('gray')
        st.pyplot(plt)

def frequency_distribution():

    # Config page layout to wide


    st.success("**FREQUENCY DISTRIBUTION TABLE**")

    # Load CSS
    theme_plotly = None 

    # Load Style CSS
    with open('style_bussiness.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Load dataframe
    df = pd.read_csv("sales.csv")

    # Expandable section to view original dataset
    with st.expander("🔎 VIEW ORIGINAL DATASET"):
        showData = st.multiselect("", df.columns, default=["OrderDate", "Region", "City", "Category", "Product", "Quantity", "UnitPrice", "TotalPrice"]) 
        st.dataframe(df[showData], use_container_width=True)
    # Calculate frequency
    frequency = df.UnitPrice.value_counts().sort_index()

    # Calculate percentage frequency
    percentage_frequency = frequency / len(df.UnitPrice) * 100

    # Calculate cumulative frequency
    cumulative_frequency = frequency.cumsum()

    # Calculate relative frequency
    relative_frequency = frequency / len(df.UnitPrice)

    # Calculate cumulative relative frequency
    cumulative_relative_frequency = relative_frequency.cumsum()

    # Create summarized table
    summary_table = pd.DataFrame({
        'Frequency': frequency,
        'Percentage Frequency': percentage_frequency,
        'Cumulative Frequency': cumulative_frequency,
        'Relative Frequency': relative_frequency,
        'Cumulative Relative Frequency': cumulative_relative_frequency
    })

    # Display summary table with filters
    showData = st.multiselect("### FILTER", summary_table.columns, default=["Frequency", "Percentage Frequency", "Cumulative Frequency", "Relative Frequency", "Cumulative Relative Frequency"]) 
    st.dataframe(summary_table[showData], use_container_width=True)

    # Calculate the mean of UnitPrice
    valid_unitprice_values = df['UnitPrice'].dropna().values
    mean_unitprice = valid_unitprice_values.mean()

    # Plot the histogram using Plotly
    fig = px.histogram(df, x='UnitPrice', nbins=10, labels={'UnitPrice': 'UnitPrice', 'count': 'Frequency'})

    # Add a dashed line for the mean
    fig.add_hline(y=mean_unitprice, line_dash="dash", line_color="green", annotation_text=f"Mean UnitPrice: {mean_unitprice:.2f}", annotation_position="bottom right")

    # Customize the histogram
    fig.update_traces(marker=dict(color='#51718E', line=dict(color='rgba(33, 150, 243, 1)', width=0.5)), showlegend=True, name='UnitPrice')

    # Update layout for the graph
    fig.update_layout(
        title='UNIT PRICE DISTRIBUTION',
        xaxis_title='UnitPrice',
        yaxis_title='Frequency',
        bargap=0.1,
        legend=dict(title='Data', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)')
    )

    # Display the histogram
    st.success("**DISTRIBUTION GRAPH**")
    st.plotly_chart(fig, use_container_width=True)

def hypo_test():
    st.header("**HYPOTHESIS TESTING** UNDER T-STUDENT DISTRIBUTION CURVE, TWO TAILED TEST")
    theme_plotly = None 

    st.subheader("𝑡=(𝑋̅−𝜇)/(𝑆/√𝑛)~𝑡(𝑛−1)")
    
    # Load Style css
    with open('style_bussiness.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Read dataset
    df = pd.read_excel("hypothesis.xlsx")
    df.drop(columns=["Date"], axis=1, inplace=True)

    # Steps for hypothesis testing
    st.info("**Null hypothesis: The average Revenue of Group A and Group B are the same.**")
    st.info("**Alternative hypothesis: The average Revenue of Group A and Group B are different.**")

    # Determine confidence level
    confidence_level = 0.95  

    # Test statistic
    t_stat, p_value = stats.ttest_ind(df['GroupA'], df['GroupB'])

    # Basic statistics from the DataFrame
    sample_mean = df.mean()
    sample_std = df.std()
    sample_size = df.shape[0]

    if sample_size >= 30:
        st.error(f"ERROR: T-test is for sample size less than 30. Unable to solve for **{sample_size}** sample size.")
        return

    # Normal distribution and critical value
    alpha = 1 - confidence_level
    critical_value = stats.t.ppf(1 - alpha / 2, df=sample_size - 1)  # Two-tailed test

    # Generate x values for the normal distribution curve
    x = np.linspace(-4, 4, 1000)
    y = stats.t.pdf(x, df=sample_size - 1)

    # Decision-making based on computed t-statistic and critical value
    if abs(t_stat) > critical_value:
        st.success("**✔ REJECT NULL HYPOTHESIS:** The average Revenue of Group A and Group B are not the same")
    else:
        st.success("#### **⚠ FAIL TO REJECT NULL HYPOTHESIS:** The average Revenue of Group A and Group B are the same")

    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='gray'), name='Probability Density'))

    # Adding vertical lines for critical value, t-statistic, and center
    fig.add_shape(type="line", x0=critical_value, y0=0, x1=critical_value, y1=max(y),
                  line=dict(color='red', width=2, dash='dash'), name=f'Critical Value: {critical_value:.2f}')
    fig.add_shape(type="line", x0=t_stat, y0=0, x1=t_stat, y1=max(y),
                  line=dict(color='green', width=2), name=f'T-statistic: {t_stat:.2f}')
    fig.add_shape(type="line", x0=0, y0=0, x1=0, y1=max(y),
                  line=dict(color='blue', width=2), name='Center: 0')

    # Filling the rejection region
    x_fill = np.linspace(critical_value, max(x), 100)
    y_fill = stats.t.pdf(x_fill, df=sample_size - 1)
    fig.add_trace(go.Scatter(x=np.concatenate([x_fill, x_fill[::-1]]), 
                              y=np.concatenate([y_fill, [0] * len(y_fill)]),
                              fill='tozeroy', fillcolor='wheat', mode='none', 
                              name='Rejection Region'))

    # Adding values to the legend
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                              marker=dict(color='red', size=0),
                              name=f'Critical Value: {critical_value:.2f}'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                              marker=dict(color='green', size=0),
                              name=f'T-statistic: {t_stat:.2f}'))

    # Layout settings
    fig.update_layout(
        title='T DISTRIBUTION',
        xaxis_title='T-STATISTIC',
        yaxis_title='PROBABILITY DENSITY',
        showlegend=True,
        legend=dict(x=0, y=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=900,
        height=600
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("SAMPLE MEAN GROUP A AND B")
        st.dataframe(sample_mean, use_container_width=True)
        st.write("SAMPLE STANDARD DEV GROUP A AND B")
        st.dataframe(sample_std, use_container_width=True)

    with col2:
        a1, a2, a3 = st.columns(3)
        a1.metric("SAMPLE SIZE", f"{sample_size:,.0f}")
        a2.metric("COMPUTED VALUE", f"{t_stat:,.3f}")
        a3.metric("CRITICAL VALUE", f"{critical_value:,.3f}")
        style_metric_cards(background_color="#FFFFFF", border_left_color="red", border_color="blue", box_shadow="grey")
        
    st.plotly_chart(fig, use_container_width=True)

def python_query():
    st.subheader("PYTHON QUERY OPERATIONS | FETCH DATA FROM DATASET BY ADVANCED QUERY")

    theme_plotly = None 
    # Load Style css
    with open('style_bussiness.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
    # Load the Excel file into a DataFrame
    file_path = 'python_query.xlsx'  
    df = pd.read_excel(file_path)

    with st.expander("🔷 **View Original Dataset | Excel file**"):
        st.dataframe(df, use_container_width=True)

    # TASK 1: Display results using Streamlit metrics cards horizontally
    # Query 1
    with st.expander("**QUERY 1:** Select count **States** by Frequency"):
        state_count = df['State'].value_counts().reset_index()
        state_count.columns = ['State', 'Frequency']
        st.write("Count of States by Frequency:")
        st.dataframe(state_count, use_container_width=True)

    # Bar graph for Query 2
    with st.expander("**QUERY 2:** select count **State** by frequency and print in dataframe and show simple bar graph with grids and legend"):
        fig3 = px.bar(state_count, x='State', y='Frequency', labels={'x': 'State', 'y': 'Frequency'}, title='Frequency of States')
        fig3.update_layout(showlegend=True)
        fig3.update_xaxes(showgrid=True)
        fig3.update_yaxes(showgrid=True)
        st.plotly_chart(fig3, use_container_width=True)

    # Query 3
    with st.expander("**QUERY 3:** Select count **BusinessType** by frequency"):
        business_type_count = df['BusinessType'].value_counts().reset_index()
        business_type_count.columns = ['BusinessType', 'Frequency']
        st.write("Count of Business Types by Frequency:")
        st.dataframe(business_type_count, use_container_width=True)

    # Bar graph for Query 4
    with st.expander("**QUERY 4:** select count **BusinessType** by frequency and print in dataframe and show simple bar graph with grids and legend"):
        fig4 = px.bar(business_type_count, x='BusinessType', y='Frequency', labels={'x': 'BusinessType', 'y': 'Frequency'}, title='Frequency of Business Types')
        fig4.update_layout(showlegend=True)
        fig4.update_xaxes(showgrid=True)
        fig4.update_yaxes(showgrid=True)
        st.plotly_chart(fig4, use_container_width=True)

    # Query 5
    with st.expander("**QUERY 5:** select minimal **Investment** and minimal **Rating** where **State** is Mwanza and date is range from 2-jan-21 to 16-jan-21"):
        query_5 = df[(df['State'] == 'Mwanza') & (df['Expiry'] >= '2021-01-02') & (df['Expiry'] <= '2021-01-16')][['Investment', 'Rating']].agg('min')
        st.success("Minimum **Investment** and **Rating** where **State** is **Mwanza** and date is in the specified range:")
        st.dataframe(query_5)

    # Query 6
    with st.expander("**QUERY 6:** select count **Location** where **Location** ='Dodoma'"):
        count_location = df[df['State'] == "Dodoma"]['Location'].count()
        st.info(f"## {count_location}")

    # Query 7
    with st.expander("**QUERY 7:** select count **Location** and **Region** where **Location** ='Dodoma' and **Region**='East'"):
        count_location_region = df[(df['State'] == "Dodoma") & (df['Region'] == "East")]['Location'].count()
        st.info(f"## {count_location_region:,.3f}")

    # Query 8
    with st.expander("**QUERY 8:** select count **Location** and **Region** where **Location** ='Dodoma' and **Region**='East' and **Investment** is greater than 300000"):
        count_location_region_investment = df[(df['State'] == "Dodoma") & (df['Region'] == "East") & (df['Investment'] > 300000)]['Location'].count()
        st.info(f"## {count_location_region_investment:,.3f}")

    # Query 9
    with st.expander("**QUERY 9:** select average mean of **investment** where **State**='Dodoma' and **Location** is not 'Urban'"):
        avg_investment_dodoma_not_urban = df[(df['State'] == "Dodoma") & (df['Location'] != "Urban")]['Investment'].mean()
        st.info(f"## {avg_investment_dodoma_not_urban:,.3f} ")

    # Query 10- Sum of investments in the date range at Dodoma
    with st.expander("**QUERY 10:** select summation of **investment** where **Expiry** is a date range from 2-jan-21 to 16-jan-21 and region is Dodoma"):
        sum_investment_date_range_dodoma = df[(df['Expiry'] >= '2021-01-02') & (df['Expiry'] <= '2021-01-16') & (df['State'] == 'Dodoma')]['Investment'].sum()
        st.info(f"## {sum_investment_date_range_dodoma:,.3f}")

    # Query 11
    with st.expander("**QUERY 11:** select Median of **Investment** and **Rating** where **State** is Mwanza, **Location** is Urban and **Investment** is greater than 400,000"):
        query_1 = df[(df['State'] == 'Mwanza') & (df['Location'] == 'Urban') & (df['Investment'] > 400000)][['Investment', 'Rating']].median()
        st.success("Median of **Investment** and **Rating** where **State** is Mwanza, **Location** is Urban, and **Investment** is greater than 400,000 USD:")
        st.dataframe(query_1)

    # Query 12
    with st.expander("**QUERY 12:** select median of **Investment** and **Rating** where **State** is Mwanza **Location** is Urban and **Investment** is greater than 400,000 and **Expiry** is a date range from 2-jan-21 to 16-jan-21"):
        query_2 = df[(df['State'] == 'Mwanza') & (df['Location'] == 'Urban') & (df['Investment'] > 400000) & (df['Expiry'] >= '2021-01-02') & (df['Expiry'] <= '2021-01-16')][['Investment', 'Rating']].median()
        st.success("Median of Investment and Rating where State is Mwanza, Location is Urban, Investment is greater than 400000, and Expiry is in the specified date range:")
        st.dataframe(query_2)

    # Display tables using st.dataframe()
    st.success("SELECT QUERY RESULTS IN TABULAR")

    # Query 13
    with st.expander('**QUERY 13:** Select all from **Location** where **Location** ="Dodoma"'):
        st.dataframe(df[df['State'] == "Dodoma"], use_container_width=True)

    # Query 14
    with st.expander('**QUERY 14:** Select all from **Location** and **Region** where **Location** ="Dodoma" and **Region**="East"'):
        st.dataframe(df[(df['State'] == "Dodoma") & (df['Region'] == "East")], use_container_width=True)

    # Query 15
    with st.expander('**QUERY 15:** Select all from **Location** and **Region** where **Location** ="Dodoma" and **Region**="East" and **Investment** is greater than 300,000'):
        st.dataframe(df[(df['State'] == "Dodoma") & (df['Region'] == "East") & (df['Investment'] > 300000)], use_container_width=True)

    # Query 16
    with st.expander('**QUERY 16:** Select all **investment** where **State**="Dodoma" and **Location** is not "Urban"'):
        st.dataframe(df.loc[(df['State'] == "Dodoma") & (df['Location'] != "Urban"), 'Investment'], use_container_width=True)

    # Query 17
    with st.expander('**QUERY 17:** select at least 5 most frequent **Investment** where **Expiry** is a date range from 2-jan-21 to 16-jan-21'):
        freq_investment_date_range = df[(df['Expiry'] >= '2021-01-02') & (df['Expiry'] <= '2021-01-16')]['Investment'].value_counts().nlargest(5).reset_index()
        st.dataframe(freq_investment_date_range.rename(columns={'index': 'Investment', 'Investment': 'Count'}))

    # Query 18
    with st.expander('**QUERY 18:** select all **investments** where **Expiry** is a date range from 2-jan-21 to 16-jan-21'):
        st.dataframe(df[(df['Expiry'] >= '2021-01-02') & (df['Expiry'] <= '2021-01-16')]['Investment'], use_container_width=True)

def adv_reg():

    # Load external stylesheet
    with open('style_bussiness.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Current date
    from datetime import datetime
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime('%Y-%m-%d')
    formatted_day = current_datetime.strftime('%A')
    
    st.header(" MACHINE LEARNING WORKFLOW | MYSQL ")
    st.markdown(
    """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <hr>
    <div class="card mb-3">
    <div class="card">
    <div class="card-body">
        <h3 class="card-title" style="color:#007710;"><strong>⏱ MULTIPLE REGRESSION ANALYSIS DASHBOARD</strong></h3>
        <p class="card-text">There are three features: InterestRate, UnemploymentRate, and PriceIndex. The purpose is to check the linear relationship between these variables, where InterestRate and UnemploymentRate are X features and IndexPrice is the Y feature. This is a classification problem using multiple regression analysis for data stored in MySQL, finally visualizing measures of variations and the line of best fit.</p>
        <p class="card-text"><small class="text-body-secondary"></small></p>
    </div>
    </div>
    </div>
    <style>
        [data-testid=stSidebar] {
            color: white;
            font-size: 24px;
        }
    </style>
    """, unsafe_allow_html=True
    )

    # Uncomment the lines below if you are using a MySQL database
    # result = view_all_data()
    # df = pd.DataFrame(result, columns=["id", "year", "month", "interest_rate", "unemployment_rate", "index_price"])

    # Read from CSV (for now)
    df = pd.read_csv("advanced_regression.csv")

    # Sidebar logo and date
    with st.sidebar:
        st.markdown(f"<h4 class='text-success'>{formatted_day}: {formatted_date}</h4>Analytics Dashboard V: 01/2023<hr>", unsafe_allow_html=True)
    
    # Filter by year and month
    year_ = st.sidebar.multiselect(
        "PICK YEAR:",
        options=df["year"].unique(),
        default=df["year"].unique()
    )
    month_ = st.sidebar.multiselect(
        "PICK MONTH:",
        options=df["month"].unique(),
        default=df["month"].unique()
    )

    # Filter DataFrame
    df_selection = df.query("month == @month_ & year == @year_")

    # Download button for CSV export
    with st.sidebar:
        df_download = df_selection.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download DataFrame",
            data=df_download,
            file_name="filtered_dataframe.csv"
        )

    # Drop unnecessary fields
    df_selection.drop(columns=["id", "year", "month"], axis=1, inplace=True)

    # Exploratory Analysis
    with st.expander("⬇ EXPLORATORY ANALYSIS"):
        st.write("Examining the correlation between the independent variables (features) and the dependent variable before building a regression model.")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Interest Rate Vs Unemployment Rate")
            plt.figure(figsize=(4, 4))
            sns.regplot(x=df_selection['interest_rate'], y=df_selection['unemployment_rate'], color="#007710")
            plt.xlabel('Interest Rate')
            plt.ylabel('Unemployment Rate')
            plt.title('Interest Rate vs Unemployment Rate: Regression Plot')
            st.pyplot()

        with col_b:
            st.subheader("Interest Rate Vs Index Price")
            plt.figure(figsize=(4, 4))
            sns.regplot(x=df_selection['interest_rate'], y=df_selection['index_price'], color="#007710")
            plt.xlabel('Interest Rate')
            plt.ylabel('Index Price')
            plt.title('Interest Rate vs Index Price: Regression Plot')
            st.pyplot()

        st.subheader("Variables Outliers")
        fig, ax = plt.subplots()
        sns.boxplot(data=df_selection, orient='h', color="#FF4B4B")
        st.pyplot(fig)

    with st.expander("⬇ EXPLORATORY VARIABLE DISTRIBUTIONS BY FREQUENCY: HISTOGRAM"):
        df_selection.hist(figsize=(16, 8), color='#007710', zorder=2, rwidth=0.9)
        st.pyplot()

    with st.expander("⬇ NULL VALUES, TENDENCY & VARIABLE DISPERSION"):
        a1, a2 = st.columns(2)
        a1.write("Number of missing (NaN or None) values in each column:")
        a1.dataframe(df_selection.isnull().sum(), use_container_width=True)
        a2.write("Insights into the central tendency, dispersion, and distribution of the data:")
        a2.dataframe(df_selection.describe().T, use_container_width=True)

    # Train/Test Split
    try:
        # Independent and dependent features
        X = df_selection.iloc[:, :-1]  # Exclude the last column
        y = df_selection.iloc[:, -1]   # Last column (dependent)

        # Train/Test split
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        # Standardization
        with st.expander("⬇ UNIFORM DISTRIBUTION"):
            st.subheader("Standard Scores (Z-Scores)")
            st.write("Transform data to have a mean of 0 and a standard deviation of 1.")
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
            st.dataframe(X_train)

        # Linear Regression
        from sklearn.linear_model import LinearRegression
        regression = LinearRegression()
        regression.fit(X_train, y_train)

        # Cross-validation score
        from sklearn.model_selection import cross_val_score
        validation_score = cross_val_score(regression, X_train, y_train, scoring='neg_mean_squared_error', cv=3)
        col1, col3, col4, col5 = st.columns(4)
        col1.metric(label="🟡 MEAN VALIDATION SCORE", value=np.mean(validation_score), delta=f"{np.mean(validation_score):,.0f}")

        # Prediction
        y_pred = regression.predict(X_test)

        # Performance metrics
        from sklearn.metrics import mean_squared_error, mean_absolute_error
        meansquareerror = mean_squared_error(y_test, y_pred)
        meanabsluteerror = mean_absolute_error(y_test, y_pred)
        rootmeansquareerror = np.sqrt(meansquareerror)

        col3.metric(label="🟡 MEAN SQUARED ERROR", value=np.mean(meansquareerror), delta=f"{np.mean(meansquareerror):,.0f}")
        col4.metric(label="🟡 MEAN ABSOLUTE ERROR", value=np.mean(meanabsluteerror), delta=f"{np.mean(meanabsluteerror):,.0f}")
        col5.metric(label="🟡 ROOT MEAN SQUARED ERROR", value=np.mean(rootmeansquareerror), delta=f"{np.mean(rootmeansquareerror):,.0f}")

        # R2 Score
        with st.expander("⬇ COEFFICIENT OF DETERMINATION | R2"):
            from sklearn.metrics import r2_score
            score = r2_score(y_test, y_pred)
            st.metric(label="🔷 r", value=score)

        with st.expander("⬇ ADJUSTED CORRELATION COEFFICIENT | R"):
            st.metric(label="🔷 Adjusted R", value=((1-(1-score)*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1))))

        with st.expander("⬇ CORRELATION COEFFICIENT | r"):
            st.write(regression.coef_)

        # Visualization
        c1, c2, c3 = st.columns(3)
        with c1:
            with st.expander("⬇ LINE OF BEST FIT"):
                st.write("The regression line best represents the relationship between the variables.")
                plt.figure(figsize=(8, 6))
                sns.regplot(x=y_test, y=y_pred, color="#FF4B4B", line_kws=dict(color="#007710"))
                st.pyplot()

        with c2:
            with st.expander("⬇ RESIDUALS"):
                st.write("Residuals: Differences between actual and predicted values.")
                residuals = y_test - y_pred
                st.dataframe(residuals)

        with c3:
            with st.expander("⬇ MODEL PERFORMANCE | NORMALIZATION"):
                from scipy.stats import norm
                plt.figure(figsize=(6, 6))
                sns.histplot(residuals, kde=True, stat="density", linewidth=0)
                mu, std = norm.fit(residuals)
                plt.title('Residuals Distribution')
                plt.xlabel('Residuals')
                st.pyplot()

    except Exception as e:
        st.error(f"An error occurred: {e}")
# Bussiness Analysts Function
def bussiness_analysts():
    st.header("ANALYTICAL PROCESSING, KPI, TRENDS & PREDICTIONS")

    # Load the data
    df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

    # Filter selection
    region = st.sidebar.multiselect("SELECT REGION", options=df["Region"].unique(), default=df["Region"].unique())
    location = st.sidebar.multiselect("SELECT LOCATION", options=df["Location"].unique(), default=df["Location"].unique())
    construction = st.sidebar.multiselect("SELECT CONSTRUCTION", options=df["Construction"].unique(), default=df["Construction"].unique())

    df_selection = df.query("Region==@region & Location==@location & Construction==@construction")

    # Main KPIs and Descriptive Analytics
    def Home():
        with st.expander("VIEW EXCEL DATASET"):
            showData = st.multiselect('Filter: ', df_selection.columns, default=["Policy", "Expiry", "Location", "State", "Region", "Investment", "Construction", "BusinessType", "Earthquake", "Flood", "Rating"])
            st.dataframe(df_selection[showData], use_container_width=True)

        # Summary statistics
        total_investment = float(pd.Series(df_selection['Investment']).sum())
        investment_mode = float(pd.Series(df_selection['Investment']).mode())
        investment_mean = float(pd.Series(df_selection['Investment']).mean())
        investment_median = float(pd.Series(df_selection['Investment']).median())
        rating = float(pd.Series(df_selection['Rating']).sum())

        total1, total2, total3, total4, total5 = st.columns(5, gap='small')
        with total1:
            st.info('Sum Investment', icon="💰")
            st.metric(label="Sum TZS", value=f"{total_investment:,.0f}")

        with total2:
            st.info('Most Investment', icon="💰")
            st.metric(label="Mode TZS", value=f"{investment_mode:,.0f}")

        with total3:
            st.info('Average', icon="💰")
            st.metric(label="Average TZS", value=f"{investment_mean:,.0f}")

        with total4:
            st.info('Central Earnings', icon="💰")
            st.metric(label="Median TZS", value=f"{investment_median:,.0f}")

        with total5:
            st.info('Ratings', icon="💰")
            st.metric(label="Rating", value=numerize(rating))

        style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

    # Graphs function
    def graphs():
        investment_by_business_type = df_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
        fig_investment = px.bar(investment_by_business_type, x="Investment", y=investment_by_business_type.index, orientation="h", title="<b> INVESTMENT BY BUSINESS TYPE </b>", color_discrete_sequence=["#0083B8"] * len(investment_by_business_type), template="plotly_white")
        fig_investment.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color="black"), yaxis=dict(showgrid=True, gridcolor='#cecdcd'))

        investment_state = df_selection.groupby(by=["State"]).count()[["Investment"]]
        fig_state = px.line(investment_state, x=investment_state.index, y="Investment", orientation="v", title="<b> INVESTMENT BY STATE </b>", color_discrete_sequence=["#0083b8"] * len(investment_state), template="plotly_white")

        left, right, center = st.columns(3)
        left.plotly_chart(fig_state, use_container_width=True)
        right.plotly_chart(fig_investment, use_container_width=True)

        with center:
            fig = px.pie(df_selection, values='Rating', names='State', title='RATINGS BY REGIONS')
            fig.update_layout(legend_title="Regions", legend_y=0.9)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.plotly_chart(fig, use_container_width=True)

    # Sidebar Menu with option for Covariance Analysis
    def sideBar():
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",
                options=["Home", "Progress", "Covariance Analysis", "Frequency Distribution","Hypothesis Testing","Python Query","Advanced Regression","Bussiness Locations","Descriptive Statistic","Regression Analysis","Sales By Date"],
                icons = [ "house", "bar-chart", "calculator", "graph-up-arrow","question-circle", "terminal", "graph-up","geo-alt", "list-task", "bar-chart-line", "calendar2-date"],
                menu_icon="cast",
                default_index=0
            )
        if selected == "Home":
            Home()
            graphs()
        elif selected == "Progress":
            Progressbar()
            graphs()
        elif selected == "Covariance Analysis":
            covariance_analysis()
        elif selected == "Frequency Distribution":
            frequency_distribution()
        elif selected == "Hypothesis Testing":
            hypo_test()
        elif selected == "Python Query":
            python_query()
        elif selected == "Advanced Regression":
            adv_reg()
        elif selected == "Bussiness Locations":
            bussiness_loc()
        elif selected == "Descriptive Statistic":
            des_stat()
        elif selected == "Regression Analysis":
            reg_analysis()    
        elif selected == "Sales By Date":
            sales()


    # Progress Bar function
    def Progressbar():
        st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""", unsafe_allow_html=True,)
        target = 3000000000
        current = df_selection["Investment"].sum()
        percent = round((current / target * 100))
        mybar = st.progress(0)

        if percent > 100:
            st.subheader("Target done!")
        else:
            st.write("You have ", percent, "% ", "of ", format(target, 'd'), "TZS")
            for percent_complete in range(percent):
                time.sleep(0.1)
                mybar.progress(percent_complete + 1, text="Target Percentage")

    # Call the Sidebar
    sideBar()

    # Feature distribution by quartiles
    st.subheader('PICK FEATURES TO EXPLORE DISTRIBUTIONS TRENDS BY QUARTILES')
    feature_y = st.selectbox('Select feature for y Quantitative Data', df_selection.select_dtypes("number").columns)
    fig2 = go.Figure(data=[go.Box(x=df['BusinessType'], y=df[feature_y])], layout=go.Layout(title=go.layout.Title(text="BUSINESS TYPE BY QUARTILES OF INVESTMENT")))
    st.plotly_chart(fig2, use_container_width=True)

    # Hide Streamlit styling
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

if __name__ == "__main__":
    bussiness_analysts()
