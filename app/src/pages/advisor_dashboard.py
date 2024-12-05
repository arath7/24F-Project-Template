import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
from assets.fakedata import fakedata
import requests



# Page configuration
st.set_page_config(page_title="CO-OPer Rates", layout="wide")
SideBarLinks()
st.session_state.selected_position = ""


# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "advisor_dashboard"