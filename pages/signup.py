
# import streamlit as st
# import requests
# from streamlit_extras.switch_page_button import switch_page

# st.set_page_config(layout="wide")

# # Signup function
# def signup(username, email, mobile_number, location, password):
#     url = "http://localhost:8083/api/v1/user/"
#     payload = {
#         "name": username,
#         "email": email,
#         "mobile_number": mobile_number,
#         "location": location,
#         "password": password
#     }
#     response = requests.post(url, json=payload)
#     return response

# # Streamlit signup page
# st.title("Sign Up")

# username = st.text_input("Username")
# email = st.text_input("Email")
# mobile_number = st.text_input("Mobile Number")
# location = st.text_input("Location")
# password = st.text_input("Password", type="password")

# if st.button("Sign Up"):
#     response = signup(username, email, mobile_number, location, password)
#     if response.status_code == 200:
#         st.success("Sign up successful")
#         # Redirect to login page with a success message
#         st.experimental_set_query_params(signup_success="true")
#         switch_page("login")
#     else:
#         st.error("Sign up failed. Please try again.")

# # Add a button to navigate to the login page
# if st.button("Login"):
#     switch_page("login")

import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide")

# Signup function
def signup(username, email, mobile_number, location, password):
    url = "http://localhost:8083/api/v1/user/"
    payload = {
        "name": username,
        "email": email,
        "mobile_number": mobile_number,
        "location": location,
        "password": password
    }
    response = requests.post(url, json=payload)
    return response

# Streamlit signup page
st.title("Sign Up")

username = st.text_input("Username")
email = st.text_input("Email")
mobile_number = st.text_input("Mobile Number")
location = st.text_input("Location")
password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    response = signup(username, email, mobile_number, location, password)
    if response.status_code == 200:
        st.success("Sign up successful")
        # Redirect to login page with a success message
        st.experimental_set_query_params(signup_success="true")
        switch_page("login")
    else:
        st.error("Sign up failed. Please try again.")

# Add a button to navigate to the login page
if st.button("Login"):
    switch_page("login")
