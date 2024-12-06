import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
from assets.fakedata import fakedata
from pages.student_home import make_listing
import requests

# Page configuration
st.set_page_config(page_title="Employer Details", layout="wide")
SideBarLinks()

# Fetch employer details
response = requests.get('http://api:4000/e/employer')
if response.status_code == 200:
    employer_details = response.json()
else:
    st.error("Failed to fetch employer details")
    st.stop()


st.write("### Search Employers")

search_query = st.text_input("", placeholder="Search for companies or positions")

if search_query:
    filtered = [emp for emp in employer_details if search_query.lower() in emp["Name"].lower()]
else:
    filtered = employer_details  # Show all positions if no query is entered


if not filtered and search_query:
    st.write("No results found.")
else:
    # Display employer details
    for employer in filtered:
        st.markdown(f"##### {employer['Name']}")
        st.write(f"{employer['Email']}")
        st.write(f"{employer['Address']}")
        st.write(f"{employer['phoneNumber']}")
        st.write(f"Number of Jobs: {employer['numJobs']}")
        if st.button(f"View Details - {employer['Name']}", key=employer["Name"]):
            st.session_state.page = "job_details"
            st.session_state.selected_employer = employer
            st.switch_page('pages/employer_jobs.py');

        st.write(f"__________")

