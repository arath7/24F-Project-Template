import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests 

# Sidebar links (assuming this is a function you have defined elsewhere)
SideBarLinks()

# Fetch flagged reviews
response = requests.get('http://api:4000/fr/flagged_content')
if response.status_code == 200:
    flagged_reviews = response.json()
else:
    st.error("Failed to fetch flagged reviews")
    st.stop()

# Search bar to filter flagged reviews by Flag ID
search_query = st.text_input("Search for Flagged Review by Flag ID")

# Filter flagged reviews based on search query
if search_query:
    filtered_flagged_reviews = [review for review in flagged_reviews if search_query.lower() in str(review['FlagID']).lower()]
else:
    filtered_flagged_reviews = flagged_reviews


# Display flagged reviews with delete buttons
st.header("Flagged Reviews")
for review in filtered_flagged_reviews:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"Flag ID: {review['FlagID']}")
        st.write(f"Review ID: {review['ReviewID']}")
        st.write(f"Reason: {review['ReasonSubmitted']}")
        st.write(f"Date Flagged: {review['DateFlagged']}")
        st.write("")
        
    with col2:
        if st.button("Delete Flag", key=f"delete_{review['FlagID']}"):
            response = requests.delete(f'http://api:4000/fr/flagged_content/{review["FlagID"]}')
            if response.status_code == 200:
                st.success(f"Flags for review {review['ReviewID']} deleted successfully")
            else:
                st.error(f"Failed to delete flags for review {review['ReviewID']}")
