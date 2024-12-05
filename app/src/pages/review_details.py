import math

import requests
import streamlit as st

from modules.nav import SideBarLinks
from modules.nav import Header
from pages.job_details import saveReviewButton

from pages.job_details import current_user

from pages.job_details import deleteReview
from pages.job_details import editReview

SideBarLinks()

Header()

review = st.session_state.selected_review
position = st.session_state.selected_position
st.session_state['currentPage'] = 'review_details'
#
# prevpage = st.session_state['prevPage']
# if st.button("← Back"):
#     st.session_state.page = prevpage
#     st.switch_page(f"pages/{prevpage}.py")
# col1, col2 = st.columns([1, 3])

employer = requests.get(f'http://api:4000/e/employer/{position["employerID"]}').json()[0]['Name']


# Display review data without allowing edits
st.write(f"### Review for {position['Name']} at {employer}")
if current_user[0].get('NUID') == review['StudentNUID']:
    editReview(review)
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


# st.write(st.session_state.get('currentUser')[0].get('NUID'),)


col1, col2 = st.columns([1, 3])
with col1: saveReviewButton(review)
with col2:
    if current_user[0].get('NUID') == review['StudentNUID']:
        deleteReview(review)