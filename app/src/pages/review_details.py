import math

import requests
import streamlit as st

from modules.nav import SideBarLinks
from modules.nav import Header

SideBarLinks()

Header()

review = st.session_state.selected_review
position = st.session_state.selected_position

if st.button("← Back to Job"):
    st.session_state.page = "job_details"
    st.switch_page("pages/job_details.py")
col1, col2 = st.columns([1, 3])

employer = requests.get(f'http://api:4000/e/employer/{position["employerID"]}').json()[0]['Name']


# Display review data without allowing edits
st.write(f"### Review for {position['Name']} at {employer}")

# Display the ratings and review text as static text
st.write(f"**Learning Opportunities**: {review['learningOpportunities']} ⭐")
st.progress(review['learningOpportunities'] * 10)

st.write(f"**Work Culture**: {review['workCulture']} 🌍")
st.progress(review['workCulture'] * 10)

st.write(f"**Mentorship**: {review['Mentorship']} 🧑‍🏫")
st.progress(review['Mentorship'] * 10)

st.write(f"**Overall Satisfaction**: {review['overallSatisfaction']} 🌟")
st.progress(review['overallSatisfaction'] * 10)



st.subheader("Final Rating:")

ratings = [review["learningOpportunities"], review["workCulture"], review["overallSatisfaction"],
           review["Mentorship"]]
sumRating = int(sum(ratings))
averageRating = sumRating / 40
scaledRating = (averageRating * 5)

st.write("### "+"⭐" * int(scaledRating) + "☆" * math.ceil(5 - scaledRating))
st.write(f"{review['textReview']}")


