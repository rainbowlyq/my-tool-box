# -*- coding: utf-8 -*-
"""
@File    : Home.py
@Time    : 2024/7/12 13:42
@Author  : lyq
@Description : 
"""

import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="💫",
)

st.write("# Home")

st.sidebar.success("Open a page above to get started.")

st.page_link("https://docs.streamlit.io/develop/api-reference", label="Streamlit Docs", icon='📖')
st.page_link("https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app", label="Streamlit Icons",
             icon="✨")
st.page_link("https://github.com/rainbowlyq/my-tool-box", label="GitHub", icon="⚒️")
