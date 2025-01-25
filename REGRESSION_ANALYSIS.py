import streamlit as st
import pandas as pd 
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_extras.metric_cards import style_metric_cards


#navicon and header
def reg_analysis(): 
    st.header("PREDICTIVE ANALYTICS DASHBOARD")
    st.write("MULTIPLE REGRESSION WITH  SSE, SE, SSR, SST, R2, ADJ[R2], RESIDUAL")
    st.success("The main objective is to measure if Number of family dependents and Wives may influence a person to supervise many projects")

    # load CSS Style
    with open('style_bussiness.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Sidebar title
    st.sidebar.title("PREDICT NEW VALUES")

    # Load data
    df = pd.read_excel('regression.xlsx')
    X = df[['Dependant', 'Wives']]
    Y = df['Projects']

    # Fit a linear regression model
    model = LinearRegression()
    model.fit(X, Y)

    # Make predictions
    predictions = model.predict(X)

    # Regression coefficients (Bo, B1, B2)
    intercept = model.intercept_  # Bo
    coefficients = model.coef_    # B1, B2

    # Calculate R-squared and Adjusted R-squared
    r2 = r2_score(Y, predictions)
    n = len(Y)
    p = X.shape[1]
    adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

    # Calculate Sum Squared Error (SSE)
    sse = np.sum((Y - predictions) ** 2)

    # Sum of Squares Regression (SSR)
    ssr = np.sum((predictions - np.mean(Y)) ** 2)

    # Display regression coefficient output
    with st.expander("REGRESSION COEFFICIENT EQUATION OUTPUT"):
        col1, col2, col3 = st.columns(3)
        col1.metric('INTERCEPT:', value=f'{intercept:.4f}', delta="(Bo)")
        col2.metric('B1 COEFFICIENT:', value=f'{coefficients[0]:.4f}', delta="for X1 number of Dependant (B1)")
        col3.metric('B2 COEFFICIENT:', value=f'{coefficients[1]:.4f}', delta="for X2 number of Wives (B2)")
        style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

    # Display measure of variations
    with st.expander("MEASURE OF VARIATIONS"):
        col1, col2, col3 = st.columns(3)
        col1.metric('R-SQUARED:', value=f'{r2:.4f}', delta="Coefficient of Determination")
        col2.metric('ADJUSTED R-SQUARED:', value=f'{adjusted_r2:.4f}', delta="Adj[R2]")
        col3.metric('SUM SQUARED ERROR (SSE):', value=f'{sse:.4f}', delta="Squared(Y-Y_pred)")
        style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

    # Display predicted Y values in a table
    with st.expander("PREDICTION TABLE"):
        result_df = pd.DataFrame({
            'Name': df['Name'],
            'No of Dependant': df['Dependant'],
            'No of Wives': df['Wives'],
            'Done Projects | Actual Y': Y,
            'Y_predicted': predictions,
            'SSE': sse,
            'SSR': ssr
        })
        st.dataframe(result_df, use_container_width=True)

        # Download predicted CSV
        df_download = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="DOWNLOAD PREDICTED DATASET",
            data=df_download,
            key="download_dataframe.csv",
            file_name="my_dataframe.csv"
        )

    # Residual plot and line of best fit
    with st.expander("RESIDUAL & LINE OF BEST FIT"):
        residuals = Y - predictions
        residuals_df = pd.DataFrame({'Actual': Y, 'Predicted': predictions, 'Residuals': residuals})
        st.dataframe(residuals_df, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            plt.scatter(Y, predictions)
            plt.plot([min(Y), max(Y)], [min(Y), max(Y)], '--k', color='red', label='Best Fit Line')
            plt.xlabel('Actual Y | number of Projects')
            plt.ylabel('Predicted Y')
            plt.grid(True)
            plt.legend()
            st.pyplot()

        with col2:
            sns.displot(residuals, kind='kde', color='blue', fill=True)
            sns.set_style("whitegrid")
            st.pyplot()

    # Sidebar input for new predictions
    with st.sidebar:
        with st.form("input_form", clear_on_submit=True):
            x1 = st.number_input("Enter Dependant")
            x2 = st.number_input("Number of Wives")
            submit_button = st.form_submit_button(label="Predict")

    if submit_button:
        new_data = np.array([[x1, x2]])
        new_prediction = model.predict(new_data)
        with st.expander("NEW INCOMING DATA PREDICTION"):
            st.write(f"<span style='font-size: 34px;color:green;'>Predicted Output: </span> <span style='font-size: 34px;'> {new_prediction}</span>", unsafe_allow_html=True)

if __name__ == "__main__":
  reg_analysis()
