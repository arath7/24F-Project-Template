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

# Display employer details
for employer in employer_details:
    st.markdown(f"Name: {employer['Name']}")
    st.write(f"Email: {employer['Email']}")
    st.write(f"Address: {employer['Address']}")
    st.write(f"Phone Number: {employer['phoneNumber']}")
    st.write(f"Number of Jobs: {employer['numJobs']}")
    st.write(f"__________")

