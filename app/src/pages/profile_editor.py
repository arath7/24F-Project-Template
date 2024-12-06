import streamlit as st
import requests

from modules.nav import SideBarLinks

# Streamlit page configuration
st.set_page_config(page_title="Profile Editor", layout="wide")


st.title("Profile Editor")
SideBarLinks()

# Function to load current user's data from session state
def load_user():
    current_user = st.session_state.get('currentUser', [])
    if current_user:
        return current_user[0]  # Assuming 'currentUser' is a list with a single dict
    else:
        st.error("No user data found.")
        st.stop()

# Function to update user profile
def update_profile(user_data):
    # Here you would make an API call to update the user's profile in the database.
    response = requests.put(f"http://api:4000/student/{user_data['NUID']}", json=user_data)
    if response.status_code == 200:
        st.success("Profile updated successfully!")
    else:
        st.error(f"Failed to update profile. Status code: {response.status_code}")


# Load current user data from session state
user = load_user()

if st.button("← Back to Profile"):
    st.session_state.page = "student_profile"
    st.switch_page("pages/student_profile.py")


# # Display current profile information
# st.write("### Current Profile Information")
# st.write(f"**Name**: {user.get('firstName')} {user.get('lastName')}")
# st.write(f"**Email**: {user.get('Email')}")
# st.write(f"**Major**: {user.get('major')}")
# st.write(f"**Graduation Year**: {user.get('GradYear')}")
# st.write(f"**School**: {user.get('school')}")
# st.write(f"**NUID**: {user.get('NUID')}")
# st.write(f"**Birth Date**: {user.get('bDate')}")

with st.container(border=True):
    st.write("### Edit Profile")

    # Collect new user data from form inputs
    NUID = st.text_input("NUID", user.get('NUID'))
    firstName = st.text_input("First Name", user.get('firstName'))
    lastName = st.text_input("Last Name", user.get('lastName'))
    Email = st.text_input("Email", user.get('Email'))
    major = st.text_input("Major", user.get('major'))
    GradYear = st.number_input("Graduation Year", value=user.get('GradYear'), min_value=1900, max_value=2100)
    school = st.text_input("School", user.get('school'))

    # Submit button for the form
    submitted = st.button("Save Changes")

    payload = {
        # "NUID": NUID,
        "firstName": firstName,
        "lastName": lastName,
        "Email": Email,
        "major": major,
        "GradYear": GradYear,
        "school": school,
        # "bDate": user.get('bDate'),
        "searchStatus": user.get('searchStatus')
    }

    # If the form is submitted, process the update
    if submitted:

        try:
            response = requests.put(f"http://api:4000/s/Student/{user.get('NUID')}", json=payload)
            # Check if the request was successful
            if response.status_code == 200:
                st.success("Profile updated successfully!")
                # st.json(response)
            else:
                st.error(f"Failed to update profile. Status code: {response.status_code}")
                st.write("Response:", response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")