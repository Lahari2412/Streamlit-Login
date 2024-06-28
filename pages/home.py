# import streamlit as st
# from streamlit_extras.switch_page_button import switch_page

# st.set_page_config(layout="wide")

# # Redirect to login if not logged in
# if 'logged_in' not in st.session_state or not st.session_state.logged_in:
#     switch_page("login")

# # Streamlit home page
# st.title("Home")

# st.write("Welcome to the home page!")

import streamlit as st
import requests
from pymongo import MongoClient
from streamlit_modal import Modal
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide")

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    switch_page("login")

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["recruiter_ai"]
collection = db["job_descriptions"]

# Page configuration
st.header("Recruiter AI")

# Define modal
modal = Modal("Job Description", key="Job_Description", max_width=800, padding=20)

# Initialize session state to store current job description and selected job ID
if 'current_job_description' not in st.session_state:
    st.session_state['current_job_description'] = ""
if 'selected_job_id' not in st.session_state:
    st.session_state['selected_job_id'] = None
if 'modal_open' not in st.session_state:
    st.session_state['modal_open'] = False
if 'modal_content' not in st.session_state:
    st.session_state['modal_content'] = ""
if 'editable' not in st.session_state:
    st.session_state['editable'] = False

# Function to fetch job descriptions from MongoDB
def fetch_job_descriptions():
    return list(collection.find({}, {"_id": 1, "prompt": 1, "job_description": 1}))

# Function to handle New Job Description button
def new_job_description():
    st.session_state['current_job_description'] = ""
    st.session_state['selected_job_id'] = None
    st.session_state['editable'] = True
    

# Function to handle Edit Job Description button
def edit_job_description():
    st.session_state['editable'] = True
    

# Function to handle Submit or Update button
def submit_or_update():
    job_description = st.session_state['current_job_description']
    if job_description:
        if st.session_state['selected_job_id'] is None:
            # Create a new job description (POST request)
            api_url = "http://localhost:8000/api/v1/jd"
            payload = {"prompt": job_description}
            response = requests.post(api_url, json=payload)
            if response.status_code == 201:
                jd_response = response.json()
                job_id = jd_response.get("id")
                prompt_saved = job_description
                job_description_created = jd_response.get("job_description")
                if job_id and job_description_created:
                    collection.insert_one({"_id": job_id, "prompt": prompt_saved, "job_description": job_description_created})
                    st.session_state['selected_job_id'] = job_id
                    st.session_state['current_job_description'] = prompt_saved
                    st.success(f"Job description created successfully with Job ID: {job_id}")
                else:
                    st.error("Failed to retrieve job ID or job description from response.")
            else:
                st.error("Failed to create job description. Please try again.")
        else:
            # Update existing job description (PUT request)
            api_url = f"http://localhost:8000/api/v1/jd/{st.session_state['selected_job_id']}"
            payload = {"prompt": job_description}
            response = requests.put(api_url, json=payload)
            if response.status_code == 200:
                jd_response = response.json()
                updated_job_description = jd_response.get("job_description")
                if updated_job_description:
                    collection.update_one({"_id": st.session_state['selected_job_id']}, {"$set": {"prompt": job_description, "job_description": updated_job_description}})
                    st.success("Job description updated successfully.")
                else:
                    st.error("Failed to update job description.")
            else:
                st.error("Failed to update job description. Please try again.")
        st.session_state['editable'] = False
    else:
        st.warning("Please enter a job description before submitting.")

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    switch_page("login")

# Sidebar
with st.sidebar:
    st.sidebar.markdown("### Saved Job Descriptions")
    
    # Create a container for the job IDs to make it scrollable
    job_list_container = st.sidebar.empty()
    
    # Display existing job descriptions as clickable links inside the container
    with job_list_container:
        job_descriptions = fetch_job_descriptions()
        for job in job_descriptions:
            if st.sidebar.button(f"Job ID: {job['_id']}"):
                st.session_state['selected_job_id'] = job['_id']
                st.session_state['current_job_description'] = job['prompt']
                st.session_state['editable'] = False
    
    st.sidebar.markdown("---")  # Separator
    
    st.sidebar.button("New Job Description", on_click=new_job_description)
    
    # Place the buttons at the bottom
    if st.session_state['selected_job_id'] is not None:
        st.sidebar.button("Edit Job Description", on_click=edit_job_description)
    
    # Logout button
    st.sidebar.button("Logout", on_click=logout)

# Job description input
job_description = st.text_area("Describe the Job Profile", value=st.session_state['current_job_description'], key='job_description', disabled=not st.session_state['editable'])

# Create columns for buttons
col1, col2 = st.columns(2)

with col1:
    if not st.session_state['editable']:
        # Submit button
        if st.button("Submit"):
            submit_or_update()
    else:
        # Update button
        if st.button("Update"):
            submit_or_update()

with col2:
    open_modal = st.button("View Job Description")
    if open_modal:
        modal.open()

# Modal content
if modal.is_open():
    with modal.container():
        if st.session_state['selected_job_id'] is not None:
            api_url = f"http://localhost:8000/api/v1/jd/{st.session_state['selected_job_id']}"
            response = requests.get(api_url)
            if response.status_code == 200:
                jd_response = response.json()
                if 'job_description' in jd_response:
                    st.markdown(jd_response['job_description'], unsafe_allow_html=True)
                else:
                    st.error("Job description field not found in the response.")
            else:
                st.error("Failed to fetch job description. Please try again.")
        else:
            st.warning("No job description selected.")
