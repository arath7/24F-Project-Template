import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
from datetime import datetime

import requests 

# Sidebar links (assuming this is a function you have defined elsewhere)
SideBarLinks()

# Fetch student details
response = requests.get('http://api:4000/s/Student')
if response.status_code == 200:
    students = response.json()
else:
    st.error("Failed to fetch student details")
    st.stop()

# Search bar to filter students by name
search_query = st.text_input("Search for Student by Name")

# Filter students based on search query
if search_query:
    filtered_students = [student for student in students if search_query.lower() in (student['firstName'] + ' ' + student['lastName']).lower()]
else:
    filtered_students = [students[0]]

# Display filtered student details with delete and update buttons
st.header("Students List")
for student in filtered_students:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"Name: {student['firstName']} {student['lastName']}")
        st.write(f"Email: {student['Email']}")
        st.write(f"School: {student['school']}")
        st.write(f"Major: {student['major']}")
        st.write(f"Graduation Year: {student['GradYear']}")
        st.write(f"Search Status: {'Looking for a job' if student['searchStatus'] else 'Not looking for a job'}")
        st.write("")

    with col2:
        if st.button("Delete", key=f"delete_{student['NUID']}"):
            response = requests.delete(f'http://api:4000/s/Student/{student["NUID"]}')
            if response.status_code == 200:
                st.success(f"Student {student['firstName']} {student['lastName']} deleted successfully")
            else:
                st.error(f"Failed to delete student {student['firstName']} {student['lastName']}")
    
    with col3:
        if st.button("Update", key=f"update_{student['NUID']}"):
            st.session_state['update_student'] = student

# Form to update a student
if 'update_student' in st.session_state:
    st.header(f"Update Student: {st.session_state['update_student']['firstName']} {st.session_state['update_student']['lastName']}")
    with st.form("update_student_form"):
        nuid = st.number_input("NUID", value=st.session_state['update_student']['NUID'], step=1)
        first_name = st.text_input("First Name", value=st.session_state['update_student']['firstName'])
        last_name = st.text_input("Last Name", value=st.session_state['update_student']['lastName'])
        bDate = datetime.strptime(st.session_state['update_student']['bDate'], '%a, %d %b %Y %H:%M:%S %Z').date()
        bDate = st.date_input("Birth Date", value=bDate)
        email = st.text_input("Email", value=st.session_state['update_student']['Email'])
        school = st.text_input("School", value=st.session_state['update_student']['school'])
        major = st.text_input("Major", value=st.session_state['update_student']['major'])
        grad_year = st.number_input("Graduation Year", value=st.session_state['update_student']['GradYear'], step=1)
        search_status = st.checkbox("Looking for a job", value=st.session_state['update_student']['searchStatus'])
        submitted = st.form_submit_button("Update Student")
        if submitted:
            updated_student = {
                "NUID": nuid,
                "bDate": bDate.isoformat(),
                "firstName": first_name,
                "lastName": last_name,
                "Email": email,
                "school": school,
                "major": major,
                "GradYear": grad_year,
                "searchStatus":  1 if search_status else 0
            }
            response = requests.put(f'http://api:4000/s/Student/{st.session_state["update_student"]["NUID"]}', json=updated_student)
            if response.status_code == 200:
                st.success("Student updated successfully")
                del st.session_state['update_student']
            else:
                st.error("Failed to update student")

# Form to add a new student
if 'update_student' not in st.session_state:
    st.header("Add New Student")
    with st.form("add_student_form"):
        nuid = st.number_input("NUID", step=1)
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        bDate = st.date_input("Birth Date")
        email = st.text_input("Email")
        school = st.text_input("School")
        major = st.text_input("Major")
        grad_year = st.number_input("Graduation Year", step=1)
        search_status = st.checkbox("Looking for a job")
        submitted = st.form_submit_button("Add Student")
        if submitted:
            new_student = {
                "NUID": nuid,
                "bDate": bDate.isoformat(),
                "firstName": first_name,
                "lastName": last_name,
                "Email": email,
                "school": school,
                "major": major,
                "GradYear": grad_year,
                "searchStatus": 1 if search_status else 0
            }
            response = requests.post('http://api:4000/s/Student', json=new_student)
            if response.status_code == 200:
                st.success("Student added successfully")
            else:
                st.error("Failed to add student")

# Fetch job details
response = requests.get('http://api:4000/j/jobs')
if response.status_code == 200:
    jobs = response.json()
else:
    st.error("Failed to fetch job details")
    st.stop()

# Create a dictionary to map student NUID to student name
student_name_map = {student['NUID']: f"{student['firstName']} {student['lastName']}" for student in students}

# Create a dictionary to map job ID to job name
job_name_map = {job['JobID']: job['Name'] for job in jobs}

# Form to add a job application
st.header("Add Job Application")
with st.form("add_job_application_form"):
    student_names = [f"{student['firstName']} {student['lastName']}" for student in students]
    job_names = [job['Name'] for job in jobs]

    selected_student_name = st.selectbox("Select Student", student_names)
    selected_job_name = st.selectbox("Select Job", job_names)
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    submitted = st.form_submit_button("Add Job Application")
    if submitted:
        selected_student = next(student for student in students if f"{student['firstName']} {student['lastName']}" == selected_student_name)
        selected_job = next(job for job in jobs if job['Name'] == selected_job_name)

        new_application = {
            "jobID": selected_job['JobID'],
            "StartDate": start_date.isoformat(),
            "EndDate": end_date.isoformat(),
        }
        response = requests.post(f'http://api:4000/s/student/{selected_student["NUID"]}/jobs', json=new_application)
        if response.status_code == 200:
            st.success("Job application added successfully")
        else:
            st.error("Failed to add job application")