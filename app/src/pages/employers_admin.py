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


# Form to add a new employer
st.header("Add New Employer")
with st.form("add_employer_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    address = st.text_input("Address")
    phone_number = st.text_input("Phone Number")
    num_jobs = st.number_input("Number of Jobs", min_value=0)
    submitted = st.form_submit_button("Add Employer")
    if submitted:
        new_employer = {
            "Name": name,
            "Email": email,
            "Address": address,
            "phoneNumber": phone_number,
            "numJobs": num_jobs
        }
        response = requests.post('http://api:4000/e/employer', json=new_employer)
        if response.status_code == 200:
            st.success("Employer added successfully")
        else:
            st.error("Failed to add employer")

# Form to update an existing employer
st.header("Update Employer")
with st.form("update_employer_form"):
    employer_id = st.text_input("Employer ID")
    name = st.text_input("Name", value=employer_details['Name'])
    email = st.text_input("Email", value=employer_details['Email'])
    address = st.text_input("Address", value=employer_details['Address'])
    phone_number = st.text_input("Phone Number", value=employer_details['phoneNumber'])
    num_jobs = st.number_input("Number of Jobs", min_value=0, value=employer_details['numJobs'])
    submitted = st.form_submit_button("Update Employer")
    if submitted:
        updated_employer = {
            "Name": name,
            "Email": email,
            "Address": address,
            "phoneNumber": phone_number,
            "numJobs": num_jobs
        }
        response = requests.put(f'http://api:4000/e/employer/{employer_id}', json=updated_employer)
        if response.status_code == 200:
            st.success("Employer updated successfully")
        else:
            st.error("Failed to update employer")

# Form to delete an employer
st.header("Delete Employer")
with st.form("delete_employer_form"):
    employer_id = st.text_input("Employer ID to Delete")
    submitted = st.form_submit_button("Delete Employer")
    if submitted:
        response = requests.delete(f'http://api:4000/e/employer/{employer_id}')
        if response.status_code == 200:
            st.success("Employer deleted successfully")
        else:
            st.error("Failed to delete employer")