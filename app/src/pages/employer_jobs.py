import math

import streamlit as st
import requests

from modules.nav import SideBarLinks

# Check if selected employer exists in session state
if 'selected_employer' not in st.session_state:
    st.error("No employer selected.")
    st.stop()

# Get the selected employer from session state
selected_employer = st.session_state.selected_employer
SideBarLinks()
col1, col2 = st.columns([2, 3])
# Display employer details

nuid = st.session_state['currentUser'][0].get('NUID')


def saveEmployerButton(employer):

    try:
        allStarred = requests.get(f'http://api:4000/e/employer/starred/{nuid}').json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching saved reviews: {e}")
        return

    employer_saved = any(r['employerID'] == employer['employerID'] for r in allStarred)
    if employer_saved:
        st.button("Saved 📗", key=f"saveded{employer['employerID']}_fromemployer", disabled=True)
    else:
        if st.button("Save Employer 📕", key=f'save{employer["employerID"]}_fromemployer'):
            payload = {
                "NUID": nuid,
                "employerID": employer['employerID'],
            }
            try:
                response = requests.post(f"http://api:4000/e/employer/starred", json=payload)
                if response.status_code == 200:
                    st.success("Successfully saved employer!")
                else:
                    st.error(f"Failed to save employer. Status code: {response.status_code}")
                    st.write("Response:", response.text)
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")


with col1:
    if st.button("← Back to Search"):
        st.session_state.page = "employers"
        st.switch_page("pages/employers.py")


    st.write(f"### Employer: {selected_employer['Name']}")
    st.write(f"**Email**: {selected_employer['Email']}")
    st.write(f"**Address**: {selected_employer['Address']}")
    st.write(f"**Phone**: {selected_employer['phoneNumber']}")
    saveEmployerButton(selected_employer)


with col2:
    # Fetch jobs for the selected employer
    response = requests.get(f'http://api:4000/j/jobs/{selected_employer["employerID"]}/employer')
    if response.status_code == 200:
        jobs = response.json()
        if jobs:
            st.write("## Jobs Available:")

            for job in jobs:
                st.markdown(f"##### **{job['Name']}**")
                category = requests.get(f'http://api:4000/jc/jobCategory/{job.get("JobCategoryID")}').json()[0]
                st.markdown(f'**Category:** :gray[{category["Name"]}]')
                st.markdown(f"**Openings:** {job['numOpenings']}")
                st.markdown(f"**Salary:** ${job['Salary']}")
                st.markdown(f"**Return Offers:** {job['returnOffers']}")


                rating = requests.get(f'http://api:4000/j/jobs/averageRating/{job.get("JobID")}').json()[0]
                update = (float(rating['AVG(overallSatisfaction)']) / 10)
                scaledRating = update * 5
                st.write("⭐" * int(scaledRating) + "☆" * math.ceil(5 - scaledRating))
                # st.write(job)
                st.write(f"Job Description: {job['Description']}")

                # Add more job-related info as needed
                if st.button(f"View Details - {job['Name']}", key=job["Name"]):
                    st.session_state.page = "job_details"
                    st.session_state.selected_position = job
                    st.switch_page('pages/job_details.py')
                st.write("___")

        else:
            st.write("No jobs available for this employer.")
    else:
        st.error("Failed to fetch jobs for this employer.")
