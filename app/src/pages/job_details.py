import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from modules.nav import SideBarLinks
from assets.fakedata import fakedata


# Page configuration
st.set_page_config(page_title="Job Details", layout="wide")
SideBarLinks()

# Simulated review data
therevs = fakedata.get('Review')
# reviews = [
#     {"name": "Sam Brown", "comment": "I really liked this job! Everyone was so nice and helpful.", "rating": 5},
#     {"name": "Jenny Martin", "comment": "Valuable experience! I feel as though I didn’t learn anything new", "rating": 3},
# ]
students = fakedata.get("Student")



# Function to get job titles and employer names
def get_student_review_info(reviews, students):
    student_review_info = []
    # Create a dictionary for fast lookup of employers by employerID
    student_dict = {student["NUID"]: student["firstName"] for student in students}

    # For each job, get the job title and employer name using the employerID
    for review in reviews:
        student_name = student_dict.get(review["StudentNUID"], "Unknown Student")

        ratings = [review["learningOpportunities"], review["workCulture"], review["overallSatisfaction"], review["Mentorship"]]
        averageRating = sum(ratings) / len(ratings)
        student_review_info.append({"studentName": student_name, "rating": averageRating, "comment": review["textReview"]})

    return student_review_info

reviews = get_student_review_info(therevs, students)

# Job details page logic
if st.session_state.page == "job_details":
    position = st.session_state.selected_position

    st.markdown("<h1 style='text-align: center; color: red;'>CO-OPer Rates</h1>", unsafe_allow_html=True)

    if st.button("← Back to Search"):
        st.session_state.page = "student_home"
        st.switch_page("pages/student_home.py")
    col1, col2 = st.columns([1, 3])

    with col2:
        st.markdown(f"**{position['title']}**")
        st.write(f"{position['reviews']} reviews")
        st.write(f"📍 {position['employer']}")
        st.write(f"📍 {position['description']}")
        st.write("⭐" * int(position["rating"]) + "☆" * (5 - int(position["rating"])))

        if st.session_state['first_name'] == 'Penny':
            st.button("I have worked as this position", disabled=True)

        else:
            st.button("❓ I'm interested in this position", disabled=True)

    st.write("Most users who have held this job found they learned a lot of technical skills, "
             "had their contributions valued, and experienced a supportive work culture.")

    if st.session_state['first_name'] == 'Penny':
        if st.button("Leave a review →", type = 'primary') :
            st.switch_page("pages/write_review.py")
    else :
        st.write("")

    # Display individual reviews
    st.write("### Reviews")
    for review in reviews:
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write("👤")
            with col2:
                st.markdown(f"**{review['studentName']}**")
                st.write(review["comment"])
                st.write("⭐" * int(review["rating"]) + "☆" * (5 - int(review["rating"])))
else:
    st.error("No job details found! Please return to the search page.")
