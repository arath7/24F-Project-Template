import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks




SideBarLinks()




# Set the current user
if st.session_state['first_name'] != 'Penny':
    st.write("You must select a persona first!")
    st.stop()

# Set page title
st.title("🌟 Your Co-op Review Dashboard")
st.write(f"Hello, {st.session_state['first_name']}! Complete your review for your recent co-op. 📝")

# Fake job reviews (mock data)
fake_reviews = [
    {"job_name": "Software Engineer", "employer": "Tech Corp", "learning_opportunities": 4, "work_culture": 5, "overall_satisfaction": 4, "mentorship": 5, "review_text": "Great company, lots of opportunities to learn and grow."},
    {"job_name": "Data Analyst", "employer": "Data Solutions", "learning_opportunities": 3, "work_culture": 4, "overall_satisfaction": 3, "mentorship": 4, "review_text": "Challenging work, but great mentorship."}
]

# Select job to review
if st.session_state.selected_position == "":
    job_names = [review['job_name'] for review in fake_reviews]
    selected_job_name = st.selectbox("Select Job to Review 💼", job_names)
    selected_review = next(review for review in fake_reviews if review['job_name'] == selected_job_name)





else:
    selected_job_name =  st.selectbox("Writing review for", st.session_state.selected_position['Name'])
    selected_review =   selected_review =  {"job_name": selected_job_name, "employer": "Tech Corp", "learning_opportunities": 0, "work_culture": 0, "overall_satisfaction": 0, "mentorship": 0, "review_text": ""}

# Get selected review data

# Display review data and allow changes
st.write(f"### Review for {selected_job_name} at {selected_review['employer']}")
learning_opportunities = st.slider("Learning Opportunities ⭐", 1, 5, selected_review['learning_opportunities'])
work_culture = st.slider("Work Culture 🌍", 1, 5, selected_review['work_culture'])
overall_satisfaction = st.slider("Overall Satisfaction 🌟", 1, 5, selected_review['overall_satisfaction'])
mentorship = st.slider("Mentorship 🧑‍🏫", 1, 5, selected_review['mentorship'])
review_text = st.text_area("Review Text ✍️", selected_review['review_text'])

# Button to submit the updated review
if st.button("Submit Review 📝"):
    st.success(f"Review for {selected_job_name} at {selected_review['employer']} has been updated! ✅")
