import streamlit as st

import requests

from modules.nav import SideBarLinks


SideBarLinks()
user = st.session_state['currentUser'][0]


st.title('Notifications')
st.markdown(f"### Here's some things you should keep an eye on, {user.get('firstName')}")
st.write("_____")
notifications = requests.get(f"http://api:4000/n/Notifications/{user.get('NUID')}").json()

if notifications:
    for notification in notifications:
        with st.container(border=True):
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"##### {notification.get('sentDate')}")
                st.markdown(f"{notification.get('Content')}")

else:
    st.write("*You have no new notifications! 👍*")
