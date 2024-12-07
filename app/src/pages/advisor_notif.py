import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
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

# Form to send a notification
st.header("Send Notification to Student")
with st.form("send_notification_form"):
    student_names = [f"{student['firstName']} {student['lastName']}" for student in students]
    selected_student_name = st.selectbox("Select Student", student_names)
    notification_message = st.text_area("Notification Message")
    submitted = st.form_submit_button("Send Notification")
    if submitted:
        selected_student = next(student for student in students if f"{student['firstName']} {student['lastName']}" == selected_student_name)
        notification = {
            "NUID": selected_student['NUID'],
            "Content": notification_message,
        }
        response = requests.post('http://api:4000/n/Notifications', json=notification)
        if response.status_code == 200:
            st.success("Notification sent successfully")
        else:
            st.error("Failed to send notification")