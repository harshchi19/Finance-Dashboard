import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import altair as alt
from datetime import date, timedelta
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards
from add_data import add_data  # Ensure this is in your working directory
from UI import UI  # Ensure this is in your working directory
import matplotlib.pyplot as plt
# Define the main sales function
def sales():
    # Page header
    st.header("SALES ANALYTICS KPI & TRENDS | DESCRIPTIVE ANALYTICS")
    st.write("Pick a date range from sidebar to view sales trends | the default date is today")

    # Load CSS styles
    with open('style_bussiness.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Load dataset
    df = pd.read_csv('sales.csv')

    # Date range input in the sidebar
    with st.sidebar:
        st.title("Select Date Range")
        start_date = st.date_input("Start Date", date.today() - timedelta(days=365 * 4))
        end_date = st.date_input("End Date", value=date.today())

    # Display selected date range in the main page
    if start_date > end_date:
        st.sidebar.error("Start date cannot be after the end date!")
    else:
        st.error(f"Business Metrics between [ {start_date} ] and [ {end_date} ]")

        # Filter the dataframe based on the selected date range
        df2 = df[(df['OrderDate'] >= str(start_date)) & (df['OrderDate'] <= str(end_date))]

        # Dataframe Explorer
        with st.expander("Filter Excel Dataset"):
            filtered_df = dataframe_explorer(df2, case=False)
            st.dataframe(filtered_df, use_container_width=True)

        # Add new record section
        b1, b2 = st.columns(2)
        with b1:
            st.subheader('Add New Record to Excel File')
            add_data()  # Function from `add_data.py` file

        # Metric cards section
        with b2:
            st.subheader('Dataset Metrics')
            col1, col2 = st.columns(2)
            col1.metric(label="All Inventory Products", value=df2['Product'].count(), delta="Items in stock")
            col2.metric(label="Total Price USD", value=f"{df2['TotalPrice'].sum():,.0f}", delta=f"{df2['TotalPrice'].median():,.0f}")
            
            col11, col22, col33 = st.columns(3)
            col11.metric(label="Maximum Price USD", value=f"{df2['TotalPrice'].max():,.0f}", delta="High Price")
            col22.metric(label="Minimum Price USD", value=f"{df2['TotalPrice'].min():,.0f}", delta="Low Price")
            col33.metric(label="Price Range USD", value=f"{df2['TotalPrice'].max() - df2['TotalPrice'].min():,.0f}", delta="Price Range")
            
            style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

        # Dot plot
        a1, a2 = st.columns(2)
        with a1:
            st.subheader('Products & Total Price')
            chart = alt.Chart(df2).mark_circle().encode(
                x='Product',
                y='TotalPrice',
                color='Category',
            ).interactive()
            st.altair_chart(chart, theme="streamlit", use_container_width=True)

        # Bar graph
        with a2:
            st.subheader('Products & Unit Price')
            energy_source = pd.DataFrame({
                "Product": df2["Product"],
                "UnitPrice ($)": df2["UnitPrice"],
                "Date": df2["OrderDate"]
            })

            bar_chart = alt.Chart(energy_source).mark_bar().encode(
                x="month(Date):O",
                y="sum(UnitPrice ($)):Q",
                color="Product:N"
            )
            st.altair_chart(bar_chart, use_container_width=True, theme=None)

        # Select numeric features for scatter plot
        p1, p2 = st.columns(2)
        with p1:
            st.subheader('Features by Frequency')
            feature_x = st.selectbox('Select feature for x (Qualitative data)', df2.select_dtypes("object").columns)
            feature_y = st.selectbox('Select feature for y (Quantitative Data)', df2.select_dtypes("number").columns)

            # Display scatter plot
            fig, ax = plt.subplots()
            sns.scatterplot(data=df2, x=feature_x, y=feature_y, hue=df2['Product'], ax=ax)
            st.pyplot(fig)

        # Bar chart for products and quantities
        with p2:
            st.subheader('Products & Quantities')
            source = pd.DataFrame({
                "Quantity ($)": df2["Quantity"],
                "Product": df2["Product"]
            })

            bar_chart = alt.Chart(source).mark_bar().encode(
                x="sum(Quantity ($)):Q",
                y=alt.Y("Product:N", sort="-x")
            )
            st.altair_chart(bar_chart, use_container_width=True, theme=None)

        # Sidebar logo image
        # st.sidebar.image("data/logo1.png")


# Call the sales function
if __name__ == "__main__":
    sales()
