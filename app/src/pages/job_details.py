import logging
import math


logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
# from pages.student_home import make_listing

import requests


# Page configuration
st.set_page_config(page_title="Job Details", layout="wide")
SideBarLinks()

reviews = requests.get(f'http://api:4000/r/review').json()

st.session_state['currentPage'] = 'job_details'

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


def saveJobButton(job):
    # Debugging: Display job data being passed
    try:
        # Fetch all starred jobs to check if the job is already saved
        allStarred = requests.get(f'http://api:4000/j/jobs/starred/{nuid}').json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching saved jobs: {e}")
        return

    # Debugging: Log all starred jobs for better insight
    # Check if the current job is already saved
    job_saved = any(r['JobID'] == job['JobID'] for r in allStarred)

    # If the job is already saved, show the saved button
    if job_saved:
        st.button("Position Saved 📗", key=f"saved{job['JobID']}_job", disabled=True)
    else:
        # Otherwise, show the "Save Position" button
        if st.button("Save Position 📕", key=f'save{job["JobID"]}_job'):
            # Check if nuid is available

            # Prepare payload
            payload = {
                "JobID": job['JobID'],
                "NUID": nuid

            }
            try:
                # Sending the POST request to save the job
                response = requests.post(f"http://api:4000/j/jobs/starred", json=payload)

                # Check if the response is successful
                if response.status_code == 200:
                    st.success("Successfully saved Job!")
                else:
                    st.error(f"Failed to save Job. Status code: {response.status_code}")
                    st.json(payload)  # Debugging the response
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while saving the job: {e}")


def saveReviewButton(review):
    try:
        allStarred = requests.get(f'http://api:4000/r/review/starred/{nuid}').json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching saved reviews: {e}")
        return

    review_saved = any(r['ReviewID'] == review['reviewID'] for r in allStarred)
    if review_saved:
        st.button("Saved 📗", key=f"saveded{review['reviewID']}", disabled=True)
    else:
        if st.button("Save Review 📕", key=f'save{review["reviewID"]}'):
            payload = {
                "NUID": nuid,
                "ReviewID": review['reviewID'],
            }
            try:
                response = requests.post(f"http://api:4000/r/review/starred", json=payload)
                if response.status_code == 200:
                    st.success("Successfully added review!")
                else:
                    st.error(f"Failed to add review. Status code: {response.status_code}")
                    st.write("Response:", response.text)
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")



def deleteReview(review):
    if st.button("Delete 🗑️", key=f'Delete{review["reviewID"]}',  type ='primary'):
        try:
            # Make the POST request
            response = requests.delete(f"http://api:4000/r/review/{review['reviewID']}")
            st.write("running!")
            # Handle the response
            if response.status_code == 200:
                st.success("Successfully added review!")
            else:
                st.error(f"Failed to add review. Status code: {response.status_code}")
                st.write("Response:", response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")



def editReview(review):
    if st.button("Edit ✏️", key=f'Edit{review["reviewID"]}',  type ='secondary'):
        st.session_state['review_writing'] = 'editing'
        st.session_state.page = "write_review"
        st.session_state['prevPage'] = st.session_state['currentPage']
        st.session_state.selected_review = review
        st.switch_page('pages/write_review.py')



def make_listing(pos):
    employer = requests.get(f'http://api:4000/e/employer/{pos["employerID"]}').json()[0]['Name']

    st.write(pos['Name'])
    st.write(f"💼 {employer}")

    rating = requests.get(f'http://api:4000/j/jobs/averageRating/{pos.get("JobID")}').json()[0]
    update = (float(rating['AVG(overallSatisfaction)']) / 10)
    scaledRating = update * 5
    st.write("⭐" * int(scaledRating) + "☆" * math.ceil(5 - scaledRating))

# Job details page logic
if st.session_state.page == "job_details":
    position = st.session_state.selected_position


    if studentjob:
        userstate = (position['JobID'] == studentjob['JobID'])
    else:
        userstate = position['JobID'] == 0

    if st.button("← Back to Search"):
        st.session_state.page = "student_home"
        st.switch_page("pages/student_home.py")
    col1, col2 = st.columns([1, 3])

    with col2:
        employer = requests.get(f'http://api:4000/e/employer/{position["employerID"]}').json()[0]['Name']
        make_listing(position)

        saveJobButton(position)

    st.write(position["Description"])
    st.write(f"Salary:", position['Salary'])
    st.write(f"Number of open positions:", position['numOpenings'])
    st.write(f"Return Offers: {'Yes' if position['returnOffers'] > 0 else 'No'}")

    if userstate:
        if st.button("Leave a review →", type = 'primary') :
            st.session_state['review_writing'] = 'creating'
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
                    st.session_state["visiting_student_role"] = 'reviewer'
                    st.session_state["visiting_student"] = author

                st.write(review["textReview"])

                ratings = [review["learningOpportunities"], review["workCulture"], review["overallSatisfaction"],
                           review["Mentorship"]]
                sumRating = int(sum(ratings))
                averageRating = sumRating/40
                scaledRating = (averageRating * 5)

                st.write("⭐" * int(scaledRating) + "☆" * math.ceil(5 - scaledRating))

                col11, col12 = st.columns([3, 4])
                # "View Details" button
                with col11:
                    if st.button(f"View Details", key=f'{review["reviewID"]}_in_jobs'):
                        st.session_state.page = "review_details"
                        st.session_state['prevPage'] = "job_details"
                        st.session_state.selected_review = review
                        st.switch_page('pages/review_details.py')
                with col12:

                    if review["StudentNUID"] == current_user[0].get('NUID'):
                        editReview(review)
                        deleteReview(review)
                    else:
                        saveReviewButton(review)



else:
    st.error("No job details found! Please return to the search page.")