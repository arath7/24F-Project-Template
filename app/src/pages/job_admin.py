import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
from assets.fakedata import fakedata
from pages.student_home import make_listing
import requests 

# Page configuration
st.set_page_config(page_title="Job Details", layout="wide")
SideBarLinks()

# Fetch employer details
response = requests.get('http://api:4000/j/jobs')
if response.status_code == 200:
    job_details = response.json()
else:
    st.error("Failed to fetch jobs")
    st.stop()




# Search bar to filter employers by name
search_query = st.text_input("Search for Job by Name")


# Filter employers based on search query
if search_query:
    filtered_jobs = [job for job in job_details if search_query.lower() in job['Name'].lower()]
else:
    filtered_jobs = [job_details[0]]

# Display filtered employer details with delete button
st.header("Jobs List")
for job in filtered_jobs:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"Name: {job['Name']}")
        st.write(f"Description: {job['Description']}")
        st.write(f"Number of Openings: {job['numOpenings']}")
        st.write(f"Return Offers: {job['returnOffers']}")
        st.write(f"Salary: {job['Salary']}")
        st.write("")
        
    with col2:
        if st.button("Delete", key=job['JobID']):
            
            delete_response = requests.delete(f'http://api:4000/j/jobs/{job["JobID"]}')
            if delete_response.status_code == 200:
                st.success(f"Job {job['Name']} deleted successfully")
            else:
                st.error("Failed to delete job")
       
            
    with col3:
        if st.button("Update", key=f"update_{job['JobID']}"):
            st.session_state['update_job'] = job


# Form to update a job
if 'update_job' in st.session_state:
    st.header(f"Update Job: {st.session_state['update_job']['Name']}")
    with st.form("update_job_form"):
        name = st.text_input("Name", value=st.session_state['update_job']['Name'])
        description = st.text_area("Description", value=st.session_state['update_job']['Description'])
        num_openings = st.number_input("Number of Openings", value=st.session_state['update_job']['numOpenings'])
        return_offers = st.checkbox("Return Offers", value=st.session_state['update_job']['returnOffers'])
        salary = st.number_input("Salary", value=st.session_state['update_job']['Salary'])
        submitted = st.form_submit_button("Update Job")
        if submitted:
            updated_job = {
                "Name": name,
                "Description": description,
                "numOpenings": num_openings,
                "returnOffers": return_offers,
                "Salary": salary,
            }
            response = requests.put(f'http://api:4000/j/jobs/{st.session_state["update_job"]["JobID"]}', json=updated_job)
            if response.status_code == 200:
                st.success("Job updated successfully")
                del st.session_state['update_job']
                st.experimental_rerun()  # Refresh the page to update the list
            else:
                st.error("Failed to update job")

# Form to add a new job
st.header("Add New Job")
with st.form("add_job_form"):
    employer_id = st.text_input("Employer ID")
    job_category_id = st.text_input("Job Category ID")
    name = st.text_input("Name")
    description = st.text_area("Description")
    num_openings = st.number_input("Number of Openings")
    return_offers = st.checkbox("Return Offers")
    salary = st.number_input("Salary")
    submitted = st.form_submit_button("Add Job")
    if submitted:
        new_job = {
            "employerID": employer_id,
            "JobCategoryID" : job_category_id,
            "Name": name,
            "Description": description,
            "numOpenings": num_openings,
            "returnOffers": return_offers,
            "Salary": salary,
        }
        response = requests.post('http://api:4000/j/jobs', json=new_job)
        if response.status_code == 200:
            st.success("Job added successfully")
            st.experimental_rerun()  # Refresh the page to update the list
        else:
            st.error("Failed to add job")

