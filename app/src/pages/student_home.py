import logging
import math

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests



# Page configuration
st.set_page_config(page_title="CO-OPer Rates", layout="wide")
SideBarLinks()
st.session_state.selected_position = ""

if st.session_state['first_name'] == "Penny":
    penny = requests.get(f'http://api:4000/s/Student/100042').json()
    # st.write(penny)
    st.session_state['currentUser'] = penny
else:
    mark = requests.get(f'http://api:4000/s/Student/100064').json()
    st.session_state['currentUser'] = mark


# Simulated data
positions = requests.get(f'http://api:4000/j/jobs').json()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "student_home"




def make_listing(pos):
    employer = requests.get(f'http://api:4000/e/employer/{pos["employerID"]}').json()[0]['Name']

    st.write(pos['Name'])
    st.markdown(f"<small><i>{pos['numReviews']} reviews</i></small>", unsafe_allow_html=True)
    st.write(f"💼 {employer}")

    rating = requests.get(f'http://api:4000/j/jobs/averageRating/{pos.get("JobID")}').json()[0]
    update = (float(rating['AVG(overallSatisfaction)']) / 10)
    scaledRating = update * 5
    st.write("⭐" * int(scaledRating) + "☆" * math.ceil(5 - scaledRating))

# Main search page logic
if st.session_state.page == "student_home":
    st.markdown("<h1 style='text-align: center; color: red;'>CO-OPer Rates</h1>", unsafe_allow_html=True)
    st.subheader(f"Welcome to your Dashboard {st.session_state['first_name']}!")

    search_query = st.text_input("Search", placeholder="Search for companies or positions")

    if search_query:
        filtered_positions = [pos for pos in positions if search_query.lower() in pos["Name"].lower()]
    else:
        filtered_positions = positions  # Show all positions if no query is entered

    st.write("### Search Results")

    if not filtered_positions and search_query:
        st.write("No results found.")
    else:
        for position in filtered_positions:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.write(f"📘 {position['JobID']}")
                with col2:
                    make_listing(position)

                    # "View Details" button
                    if st.button(f"View Details - {position['Name']}", key=position["Name"]):
                        st.session_state.page = "job_details"
                        st.session_state.selected_position = position
                        st.switch_page('pages/job_details.py');

                        st.write("____")

                    # st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """,
                    #             unsafe_allow_html=True)
