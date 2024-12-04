import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
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

# Display employer details
st.write(f"Name: {employer_details['Name']}")
st.write(f"Email: {employer_details['Email']}")
st.write(f"Address: {employer_details['Address']}")
st.write(f"Phone Number: {employer_details['phoneNumber']}")
st.write(f"Number of Jobs: {employer_details['numJobs']}")

