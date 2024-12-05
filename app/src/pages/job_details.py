import logging
import math

logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from modules.nav import SideBarLinks
from assets.fakedata import fakedata
from pages.student_home import make_listing
import requests


# Page configuration
st.set_page_config(page_title="Job Details", layout="wide")
SideBarLinks()

reviews = requests.get(f'http://api:4000/r/review').json()



if st.session_state['currentUser'] != 'Mark':
    current_user = st.session_state['currentUser']
    nuid = current_user[0].get('NUID')
    if nuid:
        student_jobs = requests.get(f"http://api:4000/j/jobs/student/{nuid}").json()
        studentjob = student_jobs[0] if student_jobs else None
    else:
        studentjob = None
else:
    studentjob = None


# Job details page logic
if st.session_state.page == "job_details":
    position = st.session_state.selected_position


    if studentjob:
        userstate = (position['JobID'] == studentjob['jobID'])
    else:
        userstate = position['JobID'] == 0


    st.markdown("<h1 style='text-align: center; color: red;'>CO-OPer Rates</h1>", unsafe_allow_html=True)
    if st.button("← Back to Search"):
        st.session_state.page = "student_home"
        st.switch_page("pages/student_home.py")
    col1, col2 = st.columns([1, 3])

    with col2:
        employer = requests.get(f'http://api:4000/e/employer/{position["employerID"]}').json()[0]['Name']
        make_listing(position)

        if userstate:
            st.button("I have worked as this position", disabled=True)

        else:
            st.button("❓ I'm interested in this position", disabled=True)

    st.write(position["Description"])
    st.write(f"Salary:", position['Salary'])
    st.write(f"Number of open positions:", position['numOpenings'])
    st.write(f"Average return offers:", position['returnOffers'])

    if userstate:
        if st.button("Leave a review →", type = 'primary') :
            st.switch_page("pages/write_review.py")
    else :
        st.write("")


    filtered_reviews = [rev for rev in reviews if rev['JobID'] == position['JobID']]

    # Display individual reviews
    st.write("### Reviews")
    for review in filtered_reviews:
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write("👤")
            with col2:

                # st.write("hi")

                author = requests.get(f'http://api:4000/s/Student/{review["StudentNUID"]}').json()[0]

                if st.page_link("pages/student_viewer.py", label=f"**{author['firstName']}**") :
                    st.session_state["visiting_student"] = author

                st.write(review["textReview"])

                ratings = [review["learningOpportunities"], review["workCulture"], review["overallSatisfaction"],
                           review["Mentorship"]]
                sumRating = int(sum(ratings))
                averageRating = sumRating/40
                scaledRating = (averageRating * 5)

                st.write("⭐" * int(scaledRating) + "☆" * math.ceil(5 - scaledRating))


                # "View Details" button
                if st.button(f"View Details", key=f'{review["reviewID"]}'):
                    st.session_state.page = "review_details"
                    st.session_state.selected_position = position
                    st.session_state.selected_review = review
                    st.switch_page('pages/review_details.py');

else:
    st.error("No job details found! Please return to the search page.")


