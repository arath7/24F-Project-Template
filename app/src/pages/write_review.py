import logging

import requests


logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks




SideBarLinks()




# Set the current user
if st.session_state['first_name'] != 'Penny':
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("You cant write reviews yet because you haven't gone on Co-op.")
    st.subheader("Check in later! 🚀")
    st.stop()

user = st.session_state['currentUser']
# st.write()
# Set page title
st.title("🌟 Your Co-op Review Dashboard")
st.write(f"Hello, {st.session_state['first_name']}! Complete your review for your recent co-op. 📝")
import requests
import streamlit as st

if st.session_state['review_writing'] != 'editing':

    jobs = requests.get(f'http://api:4000/j/jobs/student/{user[0].get("NUID")}').json()
    if not st.session_state.get('selected_position'):
        job_names = []
        for job in jobs:
            employer = requests.get(f'http://api:4000/e/employer/{job["employerID"]}').json()[0].get('Name',
                                                                                                     'Unknown Employer')
            job_names.append(f'{job.get("Name", "Unknown Job")}, {employer}')

        selected_job_name = st.selectbox("Select Job to Review 💼", job_names)

        # Get the index of the selected job in the job list
        index = job_names.index(selected_job_name)
        selected_job = jobs[index]

        # Set the selected job to session state
        st.session_state.selected_position = selected_job
    else:
        # If a job is already selected, let the user switch between the jobs
        job_names = []
        for job in jobs:
            employer = requests.get(f'http://api:4000/e/employer/{job["employerID"]}').json()[0].get('Name',
                                                                                                     'Unknown Employer')
            job_names.append(f'{job.get("Name", "Unknown Job")}, {employer}')

        selectedEmployer = requests.get(f"http://api:4000/e/employer/{st.session_state.selected_position['employerID']}").json()[0]["Name"]
        selected_job_name = st.selectbox("Switch Job to Review 💼", job_names, index=job_names.index(
            f'{st.session_state.selected_position["Name"]}, {selectedEmployer}'))

        # Get the index of the selected job in the job list
        index = job_names.index(selected_job_name)
        selected_job = jobs[index]

        # Update the session state with the selected job
        st.session_state.selected_position = selected_job

    # After selecting the job, display the review form or the job details
    st.write(f"Selected job: {st.session_state.selected_position['Name']}")
    review = requests.get(f"http://api:4000/r/review/job/{selected_job['JobID']}").json()[0]
    user = st.session_state['currentUser']
    # Example of review structure (to be extended with actual form fields):
    st.session_state.selected_review = {
        "JobID": st.session_state.selected_position["JobID"],  # Use JobID from selected position
        "StudentNUID": user[0].get("NUID"),
        # Assuming you have access to the student's NUID from session or a global variable
        "learningOpportunities": st.slider("Learning Opportunities", 0, 10, 5),
        "workCulture": st.slider("Work Culture", 0, 10, 5),
        "overallSatisfaction": st.slider("Overall Satisfaction", 0, 10, 5),
        "Mentorship": st.slider("Mentorship", 0, 10, 5),
        "textReview": st.text_area("Write your review")
    }

    # Button to submit the updated review
    if st.button("Submit Review 📝"):
        payload = {
            "JobID": selected_job["JobID"],
            "StudentNUID": user[0].get("NUID"),
            "learningOpportunities": st.session_state.selected_review['learningOpportunities'],
            "workCulture": st.session_state.selected_review['workCulture'],
            "overallSatisfaction": st.session_state.selected_review['overallSatisfaction'],
            "Mentorship": st.session_state.selected_review['Mentorship'],
            "textReview": st.session_state.selected_review['textReview'],
        }
        try:
            # Make the POST request
            response = requests.post(f"http://api:4000/r/review", json=payload)
            # Handle the response
            if response.status_code == 200:
                st.success("Successfully added review!")
            else:
                st.error(f"Failed to add review. Status code: {response.status_code}")
                st.write("Response:", response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")





else:
    # Assuming selected_review is already defined in session state

    selected_job = st.session_state.selected_position
    selected_review = st.session_state.selected_review

    # Make sure to provide default values if selected_review values are None
    learning_opportunities = int(selected_review.get('learningOpportunities', 0))
    work_culture = int(selected_review.get('workCulture', 0))
    overall_satisfaction = int(selected_review.get('overallSatisfaction', 0))
    mentorship = int(selected_review.get('Mentorship', 0))
    text_review = selected_review.get('textReview', '')

    # Update selected_review in session state
    st.session_state.selected_review = {
        "JobID": selected_job["JobID"],
        "reviewID": st.session_state.selected_review["reviewID"],
        "StudentNUID": user[0].get("NUID"),
        "learningOpportunities": st.slider("Learning Opportunities", 0, 10, learning_opportunities),
        "workCulture": st.slider("Work Culture", 0, 10, work_culture),
        "overallSatisfaction": st.slider("Overall Satisfaction", 0, 10, overall_satisfaction),
        "Mentorship": st.slider("Mentorship", 0, 10, mentorship),
        "textReview": st.text_area("Write your review", text_review)
    }

    st.json(st.session_state.selected_review)

    # Button to submit the updated review
    if st.button("Save Review ✅"):
        # Prepare the payload for the PUT request
        payload = {
            "JobID": selected_job["JobID"],
            "StudentNUID": user[0].get("NUID"),
            "reviewID": st.session_state.selected_review["reviewID"],
            "learningOpportunities": st.session_state.selected_review['learningOpportunities'],
            "workCulture": st.session_state.selected_review['workCulture'],
            "overallSatisfaction": st.session_state.selected_review['overallSatisfaction'],
            "Mentorship": st.session_state.selected_review['Mentorship'],
            "textReview": st.session_state.selected_review['textReview'],
        }

        # Ensure selected_review has values before submitting
        try:
            if all(value is not None for value in payload.values()):
                # Make the PUT request
                response = requests.put(f"http://api:4000/r/review/{st.session_state.selected_review['reviewID']}",
                                        json=payload)

                # Handle the response
                if response.status_code == 200:
                    st.success("Successfully updated review!")
                else:
                    st.error(f"Failed to update review. Status code: {response.status_code}")
                    st.write("Response:", response.text)

            else:
                st.error("Some fields are missing. Please complete all fields before submitting.")

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

