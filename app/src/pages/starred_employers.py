import math
import streamlit as st
import requests

from modules.nav import SideBarLinks

SideBarLinks()
st.title("Bookmarked Employers 👔")

# Get current user from session state
user = st.session_state["currentUser"][0]
NUID = user.get("NUID")
st.write(f"### Here's all of your saved employers, {user.get('firstName')}")
st.write("___")
st.write("")

# Fetch starred employers
starred_employers = requests.get(f'http://api:4000/e/employer/starred/{NUID}').json()

st.write(f"### {len(starred_employers)} employers:")
if len(starred_employers) > 0:
    # Loop through each starred employer
    for starred_employer in starred_employers:
        employer = requests.get(f'http://api:4000/e/employer/{starred_employer["employerID"]}').json()[0]
        # Display employer information
        st.markdown(f'##### {employer["Name"]}')
        st.write(f"**Location:** {employer.get('Address', 'Not Available')}")
        st.write(f"**Email:** {employer.get('Email', 'Not Available')}")

        # "View Details" button for the employer
        col1, col2 = st.columns([1, 2])

        with col1:
            if st.button(f"View Details", key=f'{employer["employerID"]}_from_employer'):
                st.session_state.page = "employer_details"
                st.session_state['prevPage'] = "starred_employers"
                st.session_state.selected_employer = employer
                st.switch_page('pages/employer_jobs.py')

        with col2:
            if st.button(f"🗑️", key=f'delete{starred_employer["employerID"]}_from_employer'):
                delete_url = f'http://api:4000/e/employer/starred/{starred_employer["employerID"]}'  # Correct URL path
                try:
                    response = requests.delete(delete_url)
                    if response.status_code == 200:
                        st.success(f"Employer deleted successfully!")
                    elif response.status_code == 404:
                        st.error(f"Employer not found.")
                    else:
                        st.error(f"Failed to delete resource. Status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
        st.write(f"")
        st.write(f"")


else:
    st.markdown("<i>Nothing yet! Go out and save some employers! 🚗</i>", unsafe_allow_html=True)
