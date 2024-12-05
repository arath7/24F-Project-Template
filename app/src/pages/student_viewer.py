import streamlit as st
from modules.nav import SideBarLinks


SideBarLinks()
# st.title("hi")
# st.write(st.session_state["visiting_student"])

student = st.session_state["visiting_student"]
st.title(f"{student['firstName']} {student['lastName']}")

