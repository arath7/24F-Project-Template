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
            with col2:
                if st.button('🗑️'):
                    delete_url = f"http://api:4000/n/Notifications/{notification.get('notifID')}"
                    try:
                        response = requests.delete(delete_url)
                        if response.status_code == 200:
                            st.success(f"Job removed from saved list!")
                        elif response.status_code == 404:
                            st.error(f"Job not found.")
                        else:
                            st.error(f"Failed to delete job. Status code: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"An error occurred: {e}")

else:
    st.write("*You have no new notifications! 👍*")
