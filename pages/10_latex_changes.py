# -*- coding: utf-8 -*-
"""
@File    : 10_latex_changes.py
@Time    : 2024/8/5 15:38
@Author  : lyq
@Description : 
"""
import streamlit as st
import pyperclip

st.set_page_config(page_title="Latex Changes", page_icon="🗓", layout="wide")


def parse_latex_changes(text):
    from TexSoup import TexSoup
    soup = TexSoup(text)
    for add_tag in soup.find_all('added'):
        text = text.replace(repr(add_tag), add_tag.string)
    for del_tag in soup.find_all('deleted'):
        text = text.replace(repr(del_tag), '')
    for rep_tag in soup.find_all('replaced'):
        text = text.replace(repr(rep_tag), rep_tag.expr.args[0].string)
    return text


st.title(r"Remove $\LaTeX$ Changes")
txt = st.text_area("input text")
if txt:
    output = parse_latex_changes(txt)
    st.caption("output text")
    st.code(output, language="latex")
    try:
        pyperclip.copy(output)
        st.success("Copied to clipboard")
    except:
        st.error("Failed to copy to clipboard. "
                 "Please copy manually by clicking the copy button at the right-top corner of the output text.")
