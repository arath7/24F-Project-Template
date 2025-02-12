##################################################
# This is the main/entry-point file for the
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)



# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks
from modules.nav import Header

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
# st.set_page_config(layout = 'wide')

st.set_page_config(page_title="CO-OPer Rates", layout="wide")

# If a user is at this page, we assume they are not
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false.
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel.
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt.
logger.info("Loading the Home page of the app")

# Home Screen Title
st.write('##### Welcome! Please choose the user you would like to log in as:')

if st.button("Kyle: a student searching for co-op 🧑‍💻",
             type = 'primary',
             use_container_width=True ):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'student'
    st.session_state['first_name'] = 'Kyle'
    st.switch_page('pages/student_home.py')



if st.button("Penny: a student who completed a co-op 👩‍🎓",
             type = 'primary',
             use_container_width=True ):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'student'
    st.session_state['first_name'] = 'Penny'
    st.session_state['review_writing'] = 'creating'
    st.switch_page('pages/student_home.py')




if st.button("Joe: an application administrator 👷‍♂️",
             type = 'primary',
             use_container_width=True ):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'Joe'
    st.switch_page('pages/admin_dashboard.py')



if st.button("Yasmil: a co-op advisor 👷‍♂️",
             type = 'primary',
             use_container_width=True ):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'advisor'
    st.session_state['first_name'] = 'Yasmil'
    st.switch_page('pages/advisor_dashboard.py')




