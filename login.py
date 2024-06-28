import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide")

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login function
def login(email, password):
    url = "http://localhost:8000/api/v1/login/"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    return response

# Streamlit login page
st.title("Login")

email = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = login(email, password)
    if response.status_code == 200:
        st.success("Login successful")
        st.session_state.logged_in = True
        # Redirect to home page
        switch_page("home")
    elif response.status_code == 401:
        st.error("Invalid username or password. Please try again.")
    elif response.status_code == 404:
        st.error("User not found. Please sign up.")
        # Redirect to sign up page
        switch_page("signup")
    else:
        st.error("Login failed. Please check your credentials or try again later.")

# Link to sign up page
if st.button("Sign Up"):
    switch_page("signup")
