import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from modules.nav import SideBarLinks
from assets.fakedata import fakedata
from pages.student_home import make_listing

# Page configuration
st.set_page_config(page_title="Employer Details", layout="wide")
SideBarLinks()

