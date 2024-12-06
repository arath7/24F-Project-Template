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

# Fetch job details
response = requests.get('http://api:4000/j/jobs')
if response.status_code == 200:
    job_details = response.json()
else:
    st.error("Failed to fetch jobs")
    st.stop()




# Search bar to filter jobs by name
search_query = st.text_input("Search for Job by Name")


# Filter jobs based on search query
if search_query:
    filtered_jobs = [job for job in job_details if search_query.lower() in job['Name'].lower()]
else:
    filtered_jobs = [job_details[0]]

# Display filtered job details with delete button
st.header("Jobs List")
for job in filtered_jobs:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"Name: {job['Name']}")
        st.write(f"Description: {job['Description']}")
        st.write(f"Number of Openings: {job['numOpenings']}")
        st.write(f"Return Offers: {'Yes' if job['returnOffers'] > 0 else 'No'}")
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
        num_openings = st.number_input("Number of Openings", value=st.session_state['update_job']['numOpenings'], step=1)
        return_offers = st.checkbox("Return Offers", value=st.session_state['update_job']['returnOffers'])
        salary = st.number_input("Salary", value=st.session_state['update_job']['Salary'], step=1)
        submitted = st.form_submit_button("Update Job")
        if submitted:
            updated_job = {
                "Name": name,
                "Description": description,
                "numOpenings": num_openings,
                "returnOffers": 1 if return_offers else 0,
                "Salary": salary,
            }
            response = requests.put(f'http://api:4000/j/jobs/{st.session_state["update_job"]["JobID"]}', json=updated_job)
            if response.status_code == 200:
                st.success("Job updated successfully")
                del st.session_state['update_job']
            else:
                st.error("Failed to update job")



# Fetch employer details
employer_response = requests.get('http://api:4000/e/employer')
if employer_response.status_code == 200:
    employers = employer_response.json()
else:
    st.error("Failed to fetch employer details")
    st.stop()

# Fetch job category details
job_category_response = requests.get('http://api:4000/jc/jobCategory')
if job_category_response.status_code == 200:
    job_categories = job_category_response.json()
else:
    st.error("Failed to fetch job category details")
    st.stop()


# Form to add a new job
st.header("Add New Job")
with st.form("add_job_form"):
    employer_names = [employer['Name'] for employer in employers]
    job_category_names = [category['Name'] for category in job_categories]

    selected_employer_name = st.selectbox("Employer", employer_names)
    selected_job_category_name = st.selectbox("Job Category", job_category_names)

    name = st.text_input("Name")
    description = st.text_area("Description")
    num_openings = st.number_input("Number of Openings", step=1)
    return_offers = st.checkbox("Return Offers")
    salary = st.number_input("Salary", step=1)
    submitted = st.form_submit_button("Add Job")
    if submitted:
        selected_employer = next(employer for employer in employers if employer['Name'] == selected_employer_name)
        selected_job_category = next(category for category in job_categories if category['Name'] == selected_job_category_name)

        new_job = {
            "employerID": selected_employer['employerID'],
            "JobCategoryID": selected_job_category['JobCategoryID'],
            "Name": name,
            "Description": description,
            "numOpenings": num_openings,
            "returnOffers": 1 if return_offers else 0,
            "Salary": salary,
        }
        response = requests.post('http://api:4000/j/jobs', json=new_job)
        if response.status_code == 200:
            st.success("Job added successfully")
        else:
            st.error("Failed to add job")

# Form to add a new job category
st.header("Add New Job Category")
with st.form("add_job_category_form"):
    category_name = st.text_input("Job Category Name")
    submitted = st.form_submit_button("Add Job Category")
    if submitted:
        new_category = {
            "Name": category_name,
        }
        response = requests.post('http://api:4000/jc/jobCategory', json=new_category)
        if response.status_code == 200:
            st.success("Job category added successfully")
        else:
            st.error("Failed to add job category")            

