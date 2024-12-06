import math
import streamlit as st
import requests

from modules.nav import SideBarLinks

# Display sidebar and title
SideBarLinks()
st.title("Bookmarked Jobs 📌")

# Get current user from session state
user = st.session_state["currentUser"][0]
NUID = user.get("NUID")
st.write(f"### Here's all of your saved reviews, {user.get('firstName')}")
st.write("___")
st.write("")

# Fetch starred jobs
try:
    starred_jobs = requests.get(f'http://api:4000/j/jobs/starred/{NUID}').json()
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching starred jobs: {e}")
    starred_jobs = []

# Display the number of starred jobs
st.write(f"##### {len(starred_jobs)} jobs:")

jobs = []
for j in starred_jobs:
    tempJob = requests.get(f'http://api:4000/j/jobs/{j.get("JobID")}').json()[0]
    jobs.append(tempJob)



if len(starred_jobs) > 0:
    for job in jobs:
        # Ensure 'Name' and 'JobID' exist in job object
        job_name = job.get('Name', 'Unnamed Job')
        employer_id = job.get('employerID')

        if employer_id:
            # Fetch employer data
            try:
                employer_response = requests.get(f'http://api:4000/e/employer/{employer_id}')
                employer_response.raise_for_status()
                employer_data = employer_response.json()[0]  # Assuming it's a list and fetching first element
                employer_name = employer_data.get('Name', 'Unknown Employer')
            except requests.exceptions.RequestException as e:
                employer_name = f"Error fetching employer: {e}"

        # Display job and employer info
        st.write(job_name)
        st.write(f"💼 {employer_name}")

        # Get job rating
        job_id = job.get('JobID')
        if job_id:
            try:
                rating_response = requests.get(f'http://api:4000/j/jobs/averageRating/{job_id}')
                rating_response.raise_for_status()
                rating_data = rating_response.json()[0]
                if 'AVG(overallSatisfaction)' in rating_data:
                    rating = float(rating_data['AVG(overallSatisfaction)']) / 10
                    scaled_rating = rating * 5
                    st.write("⭐" * int(scaled_rating) + "☆" * math.ceil(5 - scaled_rating))
                else:
                    st.write("No rating available")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching job rating: {e}")
                st.write("Rating not available.")
        else:
            st.write("Job ID missing!")

        # Add View Details and Delete buttons
        col1, col2 = st.columns([1, 2])

        with col1:
            if st.button(f"View Details", key=f'{job["JobID"]}_from_jobstar'):
                st.session_state.page = "job_details"
                st.session_state['prevPage'] = "starred_jobs"
                st.session_state.selected_position = job
                st.switch_page('pages/job_details.py')

        with col2:
            if st.button(f"🗑️", key=f'delete{job["JobID"]}_from_jobstar'):
                delete_url = f'http://api:4000/j/jobs/starred/{job["JobID"]}'  # Correct URL path
                try:
                    response = requests.delete(delete_url)
                    if response.status_code == 200:
                        st.success(f"Job removed from saved list!")
                    elif response.status_code == 404:
                        st.error(f"Job not found.")
                    else:
                        st.error(f"Failed to delete job. Status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")

else:
    st.markdown("<i>Nothing yet! Go out and save some! 🚗</i>", unsafe_allow_html=True)
