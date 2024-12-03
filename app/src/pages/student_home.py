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
jobs = fakedata.get('Job')
employers = fakedata.get('Employer')


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

positions = get_job_employer_info(jobs, employers)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "student_home"

# Main search page logic
if st.session_state.page == "student_home":
    st.markdown("<h1 style='text-align: center; color: red;'>CO-OPer Rates</h1>", unsafe_allow_html=True)

    search_query = st.text_input("Search", placeholder="Search for companies or positions")

    if search_query:
        filtered_positions = [pos for pos in positions if search_query.lower() in pos["title"].lower()]
    else:
        filtered_positions = positions  # Show all positions if no query is entered

    st.write("### Search Results")

    if not filtered_positions and search_query:
        st.write("No results found.")
    else:
        for position in filtered_positions:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.write("📘")
                with col2:
                    st.markdown(f"**{position['title']}**")
                    st.write(f"{position['reviews']} reviews")
                    st.write(f"📍 {position['employer']}")
                    st.write("⭐" * int(position["rating"]) + "☆" * (5 - int(position["rating"])))

                    # "View Details" button
                    if st.button(f"View Details - {position['title']}", key=position["title"]):
                        st.session_state.page = "job_details"
                        st.session_state.selected_position = position
                        st.switch_page('pages/job_details.py');
