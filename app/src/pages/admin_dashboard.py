import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
from assets.fakedata import fakedata
import requests



# Page configuration
st.set_page_config(page_title="CO-OPer Rates", layout="wide")
SideBarLinks()
st.session_state.selected_position = ""


# if st.button('see user',
#              type='primary',
#              use_container_width=True):
#   results = requests.get(f'http://api:4000/u/users/100042').json()
#   st.write(results)

# Simulated data
jobs = fakedata.get('Job') # routes to get all jobs
employers = fakedata.get('Employer') # routes to get all employers


# Function to get job titles and employer names
def get_job_employer_info(jobs, employers):
    job_employer_info = []
    # Create a dictionary for fast lookup of employers by employerID
    employer_dict = {employer["employerID"]: employer["Name"] for employer in employers}

    # For each job, get the job title and employer name using the employerID
    for job in jobs:
        employer_name = employer_dict.get(job["employerID"], "Unknown Employer")
        job_employer_info.append({"title": job["Name"], "employer": employer_name, "rating": job["Rating"], "reviews": job["numReviews"], "description": job["Description"]})

    return job_employer_info

st.title('Admin Dashboard')

  st.sidebar.title("Admin Dashboard")
page = st.sidebar.radio("Navigate to:", 
                         ["Search Reviews", "Search Flagged Reviews", "Search Students", "Search Jobs", "Search Employers"])

def sidebar_navigation():
    st.sidebar.title("Admin Dashboard")
    if st.sidebar.button("Search Reviews"):
        st.switch_page('pages/reviews.py')
    if st.sidebar.button("Search Statistics"):
        st.switch_page('pages/statistics.py')
    if st.sidebar.button("Search Students"):
        st.switch_page('pages/student_home.py')
    if st.sidebar.button("Search Jobs"):
        st.switch_page('pages/jobs.py')
    if st.sidebar.button("Search Employers"):
        st.switch_page('pages/employers.py')

# Render sidebar buttons
sidebar_navigation()


# Display content based on the current page
st.title(f"Admin Dashboard - {current_page}")

if current_page == "Search Reviews":
    st.subheader("Search Reviews")
    st.dataframe(reviews_data)

elif current_page == "Search Flagged Reviews":
    st.subheader("Search Flagged Reviews")
    if flagged_reviews_data.empty:
        st.warning("No flagged reviews at the moment.")
    else:
        st.dataframe(flagged_reviews_data)

elif current_page == "Search Students":
    st.subheader("Search Students")
    st.dataframe(students_data)

elif current_page == "Search Jobs":
    st.subheader("Search Jobs")
    st.dataframe(jobs_data)

elif current_page == "Search Employers":
    st.subheader("Search Employers")
    st.dataframe(employers_data)


