import logging
import math

import requests
from pages.student_home import make_listing


logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks


SideBarLinks()
st.write('#### Profile')

user = st.session_state['currentUser'][0]
# st.title(f'Welcome, {user["firstName"]}!')
st.title(f'Welcome, {user.get("firstName")}!')

st.write(f'###### Name:  {user.get("firstName")} {user.get("lastName")}')

col1, col2 = st.columns([2, 3])
with col1:
    st.image("https://www.shutterstock.com/image-illustration/no-picture-available-placeholder-thumbnail-600nw-2179364083.jpg",
         caption="Edit your profile ✏️", width=300)

with col2:
    st.write('###### NUID')
    st.write(f"{user.get('NUID')}")

    st.write('###### Email')
    st.write(f"{user.get('Email')}", disabled=True,)

    st.write('###### Birth Date')
    st.write(f"{user.get('bDate')}")

st.write('### Academics')

st.markdown(f"**Major:** {user.get('major')}, College of {user.get('school')}")
st.markdown(f"**Graduation Year:** {user.get('GradYeaar')}")


st.write('### Work Experience')
st.write("___")
pastJobs = requests.get(f'http://api:4000/j/jobs/student/{user.get("NUID")}').json()

for job in pastJobs:
    st.write(job['Name'])
    st.write(f"{job['numReviews']} reviews")
    rating = requests.get(f'http://api:4000/j/jobs/averageRating/{job.get("JobID")}').json()[0]
    update = (float(rating['AVG(overallSatisfaction)']) / 10)
    # st.write(update)
    scaledRating = update * 5
    st.write("⭐" * int(scaledRating) + "☆" * math.ceil(5 - scaledRating))
    st.write("___")


st.write('### Reviews Written')
st.write("___")
pastJobs = requests.get(f'http://api:4000/j/jobs/student/{user.get("NUID")}').json()

for job in pastJobs:

    st.write(job['Name'])
    st.write(f"{job['numReviews']} reviews")
    rating = requests.get(f'http://api:4000/j/jobs/averageRating/{job.get("JobID")}').json()[0]
    update = (float(rating['AVG(overallSatisfaction)']) / 10)
    scaledRating = update * 5
    st.write("⭐" * int(scaledRating) + "☆" * math.ceil(5 - scaledRating))
    st.write("___")



