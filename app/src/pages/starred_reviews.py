import math

import streamlit as st
import requests

from modules.nav import SideBarLinks
# from pages.student_profile import writeReviews



SideBarLinks()
st.title("Bookmarked Reviews 📚")
user = st.session_state["currentUser"][0]
NUID = user.get("NUID")
st.write(f"### Here's all of your saved reviews, {user.get('firstName')}")
st.write("___")
st.write("")

starred_reviews = requests.get(f'http://api:4000/r/review/starred/{NUID}').json()


st.write(f"##### {len(starred_reviews)} reviews:")
if len(starred_reviews) > 0:
    # st.dataframe(starred_reviews)
    for starredreview in starred_reviews:
        review = requests.get(f'http://api:4000/r/review/{starredreview["ReviewID"]}').json()[0]
        job = requests.get(f'http://api:4000/j/jobs/{review.get("JobID")}').json()[0]
        job = requests.get(f'http://api:4000/j/jobs/{review.get("JobID")}').json()[0]
        employerReview = requests.get(f'http://api:4000/e/employer/{job.get("employerID")}').json()[0]
        st.markdown(f'###### Written for {job["Name"]}, {employerReview["Name"]}')
        st.write(review['textReview'])
        reviewSum = sum([review['learningOpportunities'], review['workCulture'],
                         review['overallSatisfaction'], review['Mentorship']])
        rating = (reviewSum / 10)
        st.write("⭐" * int(rating) + "☆" * math.ceil(5 - rating))
        # writeReviews(review)
        # "View Details" button
        col1, col2 = st.columns([1, 2])

        with col1:
            if st.button(f"View Details", key=f'{review["reviewID"]}'):
                st.session_state.page = "review_details"
                st.session_state['prevPage'] = "starred_reviews"
                st.session_state.selected_review = review
                st.session_state.selected_position = job
                st.switch_page('pages/review_details.py');

        with col2:
            if st.button(f"🗑️", key=f'delete{starredreview["ReviewID"]}'):
                delete_url = f'http://api:4000/r/review/starred/{starredreview["ReviewID"]}'  # Correct URL path
                try:
                    response = requests.delete(delete_url)
                    if response.status_code == 200:
                        st.success(f"Review deleted successfully!")
                    elif response.status_code == 404:
                        st.error(f"Review not found.")
                    else:
                        st.error(f"Failed to delete resource. Status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")

else:
    st.markdown("<i>Nothing yet! Go out and save some! 🚗</i>", unsafe_allow_html=True)