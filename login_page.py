import streamlit as st
import psycopg2
import bcrypt


DB_HOST = "localhost"
DB_NAME = "TSEC"
DB_USER = "postgres"
DB_PASS = "Saty@123"

def set_background(image_url):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url({image_url});
                background-size: fit;
                background-position: center;
                background-repeat: repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    

def get_user_credentials(username):
    """Fetch the password for a given username from the database."""
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    conn.close()
    return result

def check_login(username, password):
    """Check if the provided username and password are correct."""
    stored_password = get_user_credentials(username)
    if stored_password and bcrypt.checkpw(password.encode(), stored_password[0].encode()):
        return True
    return False


def load_login_page():

    set_background("https://www.shutterstock.com/shutterstock/photos/2268772887/display_1500/stock-vector-gray-digital-data-matrix-of-binary-code-numbers-isolated-on-a-white-background-with-a-copy-text-2268772887.jpg")

    
    st.markdown("""
    <style>
            html{
                font-family: Manrope;
                }
            .e1nzilvr2{
                text-align:center;
                text-shadow: 0px 2px 5.3px rgba(0, 0, 0, 0.19);
                font-family: Manrope;
                font-size: 72px;
                font-style: normal;
                font-weight: 600;
                line-height: 83px; 
                opacity: 0;
                animation: fadeIn 2s forwards;
                }
             .ea3mdgi5{
                max-width:100%;
                }
    </style>
        """, unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1.5])  # Adjust the ratio as needed

    # Display the image in the first column
    with col2:
        st.image(
            "https://img.freepik.com/free-vector/tablet-login-concept-illustration_114360-7863.jpg",
            use_column_width=True,
            width=100  # Adjust width as needed
        )

    # Display the login form in the second column
    with col1:
        st.markdown("""
        <style>
            h1 {
                text-align: center;
                text-shadow: 0px 2px 5.3px rgba(0, 0, 0, 0.19);
                font-family: Manrope;
                font-size: 72px;
                font-style: normal;
                font-weight: 600;
                line-height: 83px;
                letter-spacing: -2.16px;
                opacity: 0;
                animation: fadeIn 2s forwards;
            }
            input {
                margin-top: 10px;
                padding: 10px;
                width: 100%;
                font-size: 18px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
        </style>
        """, unsafe_allow_html=True)

        st.title("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
           is_authenticated = check_login(username, password)
           if is_authenticated:
                    st.session_state.is_authenticated = True
                    st.success("Logged in successfully!")
                    st.rerun()
           else:
                st.error("Invalid username or password")

   

