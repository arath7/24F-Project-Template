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

# # Display employer details
# st.write(f"Name: {employer_details[0]['Name']}")
# st.write(f"Email: {employer_details[0]['Email']}")
# st.write(f"Address: {employer_details[0]['Address']}")
# st.write(f"Phone Number: {employer_details[0]['phoneNumber']}")
# st.write(f"Number of Jobs: {employer_details[0]['numJobs']}")
# Display employer details with delete button


# st.header("Employers List")
# for employer in employer_details:
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         st.write(f"Name: {employer['Name']}")
#         st.write(f"Email: {employer['Email']}")
#         st.write(f"Address: {employer['Address']}")
#         st.write(f"Phone Number: {employer['phoneNumber']}")
#         st.write(f"Number of Jobs: {employer['numJobs']}")
#     with col2:
#         if st.button(f"Delete {employer['Name']}", key=employer['employerID']):
#             response = requests.delete(f'http://api:4000/e/employer/{employer["employerID"]}')
#             if response.status_code == 200:
#                 st.success(f"Employer {employer['Name']} deleted successfully")
#                 st.experimental_rerun()  # Refresh the page to update the list
#             else:
#                 st.error(f"Failed to delete employer {employer['Name']}")



# Search bar to filter employers by name
search_query = st.text_input("Search for Employer by Name")


# Filter employers based on search query
if search_query:
    filtered_employers = [employer for employer in employer_details if search_query.lower() in employer['Name'].lower()]
else:
    filtered_employers = [employer_details[0]]

# Display filtered employer details with delete button
st.header("Employers List")
for employer in filtered_employers:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"Name: {employer['Name']}")
        st.write(f"Email: {employer['Email']}")
        st.write(f"Address: {employer['Address']}")
        st.write(f"Phone Number: {employer['phoneNumber']}")
        st.write("")
        
    with col2:
        if st.button(f"Delete {employer['Name']}", key=employer['employerID']):
            job_response = requests.get(f'http://api:4000/e/employer/{employer["employerID"]}/jobs')
            if job_response.status_code == 200:
                jobs = job_response.json()
                if len(jobs) > 0:
                    st.error(f"Cannot delete employer {employer['Name']} because there are job openings for this employer")
                else:
                    # Attempt to delete the employer
                    delete_response = requests.delete(f'http://api:4000/e/employer/{employer["employerID"]}')
                    if delete_response.status_code == 200:
                        st.success(f"Employer {employer['Name']} deleted successfully")
                        st.experimental_rerun()  # Refresh the page to update the list
                    else:
                        st.error(f"Failed to delete employer {employer['Name']}")
            else:
                st.error("Failed to check job openings for this employer")
            
    with col3:
        if st.button(f"Update {employer['Name']}", key=f"update_{employer['employerID']}"):
            st.session_state['update_employer'] = employer

# Form to update an employer
if 'update_employer' in st.session_state:
    st.header(f"Update Employer: {st.session_state['update_employer']['Name']}")
    with st.form("update_employer_form"):
        name = st.text_input("Name", value=st.session_state['update_employer']['Name'])
        email = st.text_input("Email", value=st.session_state['update_employer']['Email'])
        address = st.text_input("Address", value=st.session_state['update_employer']['Address'])
        phone_number = st.text_input("Phone Number", value=st.session_state['update_employer']['phoneNumber'])
        submitted = st.form_submit_button("Update Employer")
        if submitted:
            updated_employer = {
                "Name": name,
                "Email": email,
                "Address": address,
                "phoneNumber": phone_number,
            }
            response = requests.put(f'http://api:4000/e/employer/{st.session_state["update_employer"]["employerID"]}', json=updated_employer)
            if response.status_code == 200:
                st.success("Employer updated successfully")
                del st.session_state['update_employer']
                st.experimental_rerun()  # Refresh the page to update the list
            else:
                st.error("Failed to update employer")


# Form to add a new employer
st.header("Add New Employer")
with st.form("add_employer_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    address = st.text_input("Address")
    phone_number = st.text_input("Phone Number")
    submitted = st.form_submit_button("Add Employer")
    if submitted:
        new_employer = {
            "Name": name,
            "Email": email,
            "Address": address,
            "phoneNumber": phone_number,
        }
        response = requests.post('http://api:4000/e/employer', json=new_employer)
        if response.status_code == 200:
            st.success("Employer added successfully")
        else:
            st.error("Failed to add employer")

# # Form to update an existing employer
# st.header("Update Employer")
# with st.form("update_employer_form"):
#     employer_id = st.text_input("Employer ID")
#     name = st.text_input("Name", value=employer_details['Name'])
#     email = st.text_input("Email", value=employer_details['Email'])
#     address = st.text_input("Address", value=employer_details['Address'])
#     phone_number = st.text_input("Phone Number", value=employer_details['phoneNumber'])
#     submitted = st.form_submit_button("Update Employer")
#     if submitted:
#         updated_employer = {
#             "Name": name,
#             "Email": email,
#             "Address": address,
#             "phoneNumber": phone_number
#         }
#         response = requests.put(f'http://api:4000/e/employer/{employer_id}', json=updated_employer)
#         if response.status_code == 200:
#             st.success("Employer updated successfully")
#         else:
#             st.error("Failed to update employer")

# # Form to delete an employer
# st.header("Delete Employer")
# with st.form("delete_employer_form"):
#     employer_id = st.text_input("Employer ID to Delete")
#     submitted = st.form_submit_button("Delete Employer")
#     if submitted:
#         response = requests.delete(f'http://api:4000/e/employer/{employer_id}')
#         if response.status_code == 200:
#             st.success("Employer deleted successfully")
#         else:
#             st.error("Failed to delete employer")