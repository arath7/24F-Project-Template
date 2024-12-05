import logging
import math

import requests


logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks


SideBarLinks()
st.write('#### Profile')

current = st.session_state['currentUser'][0]
# st.title(f'Welcome, {user["firstName"]}!')
st.title(f'Welcome, {current.get("firstName")}!')



def writeReviews(review):
    job = requests.get(f'http://api:4000/j/jobs/{review.get("JobID")}').json()[0]
    employerReview = requests.get(f'http://api:4000/e/employer/{job.get("employerID")}').json()[0]
    st.markdown(f'###### Written for {job["Name"]}, {employerReview["Name"]}')
    st.write(review['textReview'])
    reviewSum = sum([review['learningOpportunities'], review['workCulture'],
                     review['overallSatisfaction'], review['Mentorship']])
    rating = (reviewSum / 10)
    st.write("⭐" * int(rating) + "☆" * math.ceil(5 - rating))



def Student(user):
    st.write(f'###### Name:  {user.get("firstName")} {user.get("lastName")}')

    col1, col2 = st.columns([2, 3])
    with col1:
        st.image("https://www.shutterstock.com/image-illustration/no-picture-available-placeholder-thumbnail-600nw-2179364083.jpg",
             caption="Edit your profile ✏️", width=300)

    with col2:
        st.write('###### NUID')
        st.write(f"{user.get('NUID')}")

        st.write('###### Email')
        st.write(f"{user.get('Email')}", disabled=True,)

        st.write('###### Birth Date')
        st.write(f"{user.get('bDate')}")
        st.write("___")

    st.write('### Academics')

    st.markdown(f"**Major:** {user.get('major')}, College of {user.get('school')}")
    st.markdown(f"**Graduation Year:** {user.get('GradYeaar')}")

    st.write("___")

    st.write('### Work Experience')
    pastJobs = requests.get(f'http://api:4000/j/jobs/student/{user.get("NUID")}').json()

    if pastJobs:
        for job in pastJobs:
            st.markdown(f'###### {job["Name"]}')
            rating = requests.get(f'http://api:4000/j/jobs/averageRating/{job.get("JobID")}').json()[0]
            employer = requests.get(f'http://api:4000/e/employer/{job.get("employerID")}').json()[0]

            update = (float(rating['AVG(overallSatisfaction)']) / 10)
            st.write(f"💼 {employer['Name']}")
            scaledRating = update * 5
            st.write("⭐" * int(scaledRating) + "☆" * math.ceil(5 - scaledRating))

    else:
        st.markdown(f"<small><i>Nothing yet! 🔧</i></small>", unsafe_allow_html=True)
    st.write("___")

    st.write('### Reviews Written')
    reviewsWritten = requests.get(f'http://api:4000/r/review/student/{user.get("NUID")}').json()



    if reviewsWritten:
        for review in reviewsWritten:
            writeReviews(review)
            # job = requests.get(f'http://api:4000/j/jobs/{review.get("JobID")}').json()[0]
            # employerReview = requests.get(f'http://api:4000/e/employer/{job.get("employerID")}').json()[0]
            # st.markdown(f'###### Written for {job["Name"]}, {employerReview["Name"]}')
            # st.write(review['textReview'])
            # reviewSum = sum([review['learningOpportunities'], review['workCulture'],
            #                        review['overallSatisfaction'], review['Mentorship']])
            # rating = (reviewSum / 10)
            # st.write("⭐" * int(rating) + "☆" * math.ceil(5 - rating))

    else:
        st.markdown(f"<small><i>Nothing yet! 🔧</i></small>", unsafe_allow_html=True)



    # "View Details" button
    if st.button(f"View Details", key=f'{review["reviewID"]}'):
        st.session_state.page = "review_details"
        st.session_state['prevPage'] = "student_profile"
        st.session_state.selected_review = review
        st.session_state.selected_position = job
        st.switch_page('pages/review_details.py');
Student(current)