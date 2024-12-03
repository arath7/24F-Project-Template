import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks


SideBarLinks()
st.write('#### Profile')
st.title(st.session_state.get('first_name'))

col1, col2 = st.columns([2, 3])
with col1:
    st.image("https://www.shutterstock.com/image-illustration/no-picture-available-placeholder-thumbnail-600nw-2179364083.jpg",
         caption="Edit your profile ✏️", width=300)

with col2:
    st.write('##### Name')
    st.write(st.session_state.get('first_name'))
    st.write('#### NUID')
    st.write()

    st.write('#### Profile')