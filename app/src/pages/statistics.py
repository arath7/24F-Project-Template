import requests
import streamlit as st
from modules.nav import SideBarLinks

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

st.header("Return Offer Percentage")
return_offer_percentage = stats.get('return_offer_percentage', {})
st.write(return_offer_percentage)

st.header("Total Students")
total_students = stats.get('total_students', {})
st.write(total_students)

st.header("Total Jobs")
total_jobs = stats.get('total_jobs', {})
st.write(total_jobs)

st.header("Total Reviews")
total_reviews = stats.get('total_reviews', {})
st.write(total_reviews)

st.header("Total Employers")
total_employers = stats.get('total_employers', {})
st.write(total_employers)

st.header("Jobs by Category")
jobs_by_category = stats.get('jobs_by_category', {})
st.write(jobs_by_category)