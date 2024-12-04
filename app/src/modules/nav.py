# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ Student Role ------------------------
def StudentPageNav():
    st.sidebar.page_link("pages/student_home.py", label="Search For Jobs", icon="🔍")
    st.sidebar.page_link("pages/student_profile.py", label="Profile", icon="🙂️")
    st.sidebar.page_link("pages/write_review.py", label="Write a Review️", icon="✏️")
    st.sidebar.page_link("pages/reviews.py", label="Reviews", icon="📝")
    st.sidebar.page_link("pages/employers.py", label="Employers", icon="🏢")


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/statistics.py", label="Current Statistics", icon="🖥️")
    st.sidebar.page_link("pages/reviews.py", label="Reviews", icon="📝")
    st.sidebar.page_link("pages/job_details.py", label="Jobs", icon="💼")
    st.sidebar.page_link("pages/employers.py", label="Employers", icon="🏢")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "student":
            StudentPageNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
