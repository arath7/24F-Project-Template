import requests
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd

# Page configuration
st.set_page_config(page_title="Statistics", layout="wide")
SideBarLinks()

# Fetch statistics from various routes
routes = {
    'return_offer_percentage': 'http://api:4000/a/admin/return_offer_percentage',
    'total_students': 'http://api:4000/a/admin/total_students',
    'total_jobs': 'http://api:4000/a/admin/total_jobs',
    'total_reviews': 'http://api:4000/a/admin/total_reviews',
    'total_employers': 'http://api:4000/a/admin/total_employers',
    'jobs_by_category': 'http://api:4000/a/admin/jobs_by_category'
}


stats = {}
for key, route in routes.items():
    response = requests.get(route)
    if response.status_code == 200:
        stats[key] = response.json()
    else:
        st.error(f"Failed to fetch statistics from {route}")
        st.stop()

# Display statistics
st.title("Statistics")

return_offer_percentage = stats.get('return_offer_percentage', {}).get('returnOfferPercentage')
total_students = (stats.get('total_students', []))[0]["COUNT(NUID)"]
total_jobs = (stats.get('total_jobs', []))[0]["COUNT(JobID)"]
total_reviews = (stats.get('total_reviews', []))[0]["COUNT(reviewID)"]
total_employers = (stats.get('total_employers', []))[0]["COUNT(employerID)"]


st.markdown("### Application Statistics")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label="Return Offer Percentage", value=return_offer_percentage)
with col2:
    st.metric(label="Total Students", value=total_students)
with col3:
    st.metric(label="Total Jobs", value=total_jobs)
with col4:
    st.metric(label="Total Reviews", value=total_reviews)    
with col5:
    st.metric(label="Total Employers", value=total_employers)



jobs_by_cat = stats.get('jobs_by_category', [])

df = pd.DataFrame(jobs_by_cat)
df.rename(columns={"COUNT(j.JobID)": "Number of Jobs", "Name": "Category"}, inplace=True)
df = df[["Category", "Number of Jobs"]]
st.markdown("### Overview of Job Categories")
st.dataframe(df, use_container_width=True)