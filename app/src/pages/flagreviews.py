import requests
import streamlit as st
from modules.nav import SideBarLinks

# Page configuration
st.set_page_config(page_title="Flag Reviews", layout="wide")
SideBarLinks()

# Fetch reviews
response = requests.get('http://api:4000/reviews')
if response.status_code == 200:
    reviews = response.json()
else:
    st.error("Failed to fetch reviews")
    st.stop()

# Display reviews
st.title("Reviews")
for review in reviews:
    st.write(f"Review ID: {review['reviewID']}")
    st.write(f"Text Review: {review['textReview']}")
    st.write(f"Overall Satisfaction: {review['overallSatisfaction']}")
    st.write(f"Reviewer NUID: {review['StudentNUID']}")
    
    
    # Form to flag a review
    with st.form(f"flag_review_form_{review['reviewID']}"):
        reason = st.text_input("Reason for flagging")
        submitted = st.form_submit_button("Flag Review")
        if submitted:
            flagged_review = {
                "ReviewID": review['reviewID'],
                "ReasonSubmitted": reason
            }
            flag_response = requests.post('http://api:4000/fr/flagged_reviews', json=flagged_review)
            if flag_response.status_code == 200:
                st.success("Review flagged successfully")
            else:
                st.error("Failed to flag review")