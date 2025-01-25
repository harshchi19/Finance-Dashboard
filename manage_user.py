import psycopg2
import bcrypt
import streamlit as st

# PostgreSQL connection details
DB_HOST = "localhost"
DB_NAME = "TSEC"
DB_USER = "postgres"
DB_PASS = "Saty@123"


def add_user(username, password):

    st.write(username)
    st.write(password)
    """Add a new user with a hashed password."""
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    conn.close()

# Example usage
if __name__ == "__main__":
    user = st.text_input("Enter the user name")
    pass1 = st.text_input("Enter the password")

    if st.button("Submit"):
        add_user(user, pass1)
