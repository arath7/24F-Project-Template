import streamlit as st
import requests
import pandas as pd

st.title("Admin Dashboard")

# Section 1: Return Offer Percentage
st.header("Return Offer Percentage")
response = requests.get("http://api:4000/a/admin/return_offer_percentage")
if response.status_code == 200:
    return_offer_percentage = response.json().get("returnOfferPercentage", 0)
    st.metric(label="Return Offer Percentage", value=f"{return_offer_percentage:.2f}%")
else:
    st.error("Failed to fetch return offer percentage.")

# Section 2: Total Counts (Students, Jobs, Reviews, Employers)
st.header("Total Counts")
try:
    counts = {
        "Students": requests.get("http://api:4000/a/admin/total_students").json()[0].get("COUNT(NUID)", 0),
        "Jobs": requests.get("http://api:4000/a/admin/total_jobs").json()[0].get("COUNT(JobID)", 0),
        "Reviews": requests.get("http://api:4000/a/admin/total_reviews").json()[0].get("COUNT(reviewID)", 0),
        "Employers": requests.get("http://api:4000/a/admin/total_employers").json()[0].get("COUNT(employerID)", 0),
    }
    st.bar_chart(pd.DataFrame.from_dict(counts, orient="index", columns=["Count"]))
except Exception as e:
    st.error(f"Failed to fetch total counts: {e}")

# Section 3: Jobs by Category 
st.header("Jobs by Category")
response = requests.get("http://api:4000/a/admin/jobs_by_category")
if response.status_code == 200:
    try:
        jobs_by_category = pd.DataFrame(response.json())
        st.table(jobs_by_category)
        st.bar_chart(jobs_by_category.set_index("Name"))
    except Exception as e:
        st.error(f"Error processing jobs by category data: {e}")
else:
    st.error("Failed to fetch jobs by category.")

st.write("Powered by Streamlit")
