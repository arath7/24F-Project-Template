import logging
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from modules.nav import SideBarLinks
from assets.fakedata import fakedata

# Logger configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Page configuration
st.set_page_config(page_title="Admin Dashboard", layout="wide")
SideBarLinks()

# Simulated admin data
reviews = fakedata.get('Review')
students = fakedata.get("Student")

# Function to get student review info
def get_student_review_info(reviews, students):
    student_review_info = []
    student_dict = {student["NUID"]: student["firstName"] for student in students}

    for review in reviews:
        student_name = student_dict.get(review["StudentNUID"], "Unknown Student")
        ratings = [review["learningOpportunities"], review["workCulture"], review["overallSatisfaction"], review["Mentorship"]]
        average_rating = sum(ratings) / len(ratings)
        student_review_info.append({"studentName": student_name, "rating": average_rating, "comment": review["textReview"]})

    return student_review_info

student_review_info = get_student_review_info(reviews, students)

# Admin dashboard logic
st.markdown("<h1 style='text-align: center; color: blue;'>Admin Dashboard</h1>", unsafe_allow_html=True)

# Navigation Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("View All Students"):
        logger.info("Admin clicked to view all students")
        switch_page("pages/students_list.py")

with col2:
    if st.button("Manage Jobs"):
        logger.info("Admin clicked to manage jobs")
        switch_page("pages/manage_jobs.py")

with col3:
    if st.button("Statistics Dashboard"):
        logger.info("Admin clicked to view statistics dashboard")
        switch_page("pages/statistics_dashboard.py")

# Display student reviews
st.write("### Recent Reviews")

for review in student_review_info:
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write("👤")
        with col2:
            st.markdown(f"**{review['studentName']}**")
            st.write(review["comment"])
            st.write("⭐" * int(review["rating"]) + "☆" * (5 - int(review["rating"])))
