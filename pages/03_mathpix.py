# -*- coding: utf-8 -*-
"""
@File    : 03_mathpix.py
@Time    : 2024/7/12 17:41
@Author  : lyq
@Description : 
"""
import streamlit as st
from PIL import Image, ImageGrab
from pix2tex.cli import LatexOCR
import pyperclip
from st_copy_to_clipboard import st_copy_to_clipboard

st.set_page_config(page_title="MathPix", page_icon="Ⓜ️", layout="wide")


@st.cache_resource
def get_model():
    return LatexOCR()


def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.toast("Copied to clipboard!")


def reset():
    pass


def main():
    st.title(r"Mathpix OCR to $\LaTeX$")
    left_col, right_col = st.columns(2)
    # 上传图片
    uploaded_file = left_col.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="upload_file")
    # 读取剪贴板中的图片
    clipboard_image = None
    c1, c2, c3 = left_col.columns(3)
    if c1.button("Read from clipboard"):
        try:
            clipboard_image = ImageGrab.grabclipboard()
            if clipboard_image is None:
                left_col.error("No image found in clipboard")
        except NotImplementedError:
            left_col.error("Clipboard image reading not supported on this platform. Please use the file uploader.")
    if c2.button("GPT to Markdown"):
        try:
            clipboard_text = pyperclip.paste()
            copy_to_clipboard(gpt2md(clipboard_text))
        except NotImplementedError:
            left_col.error("Clipboard not supported on this platform. ")
    if c3.button("Reset"):
        reset()

    # 显示图片
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        right_col.image(image, caption="Uploaded Image")
    elif clipboard_image is not None:
        image = clipboard_image.convert('RGB')
        right_col.image(image, caption="Image from clipboard")

    if image is not None:
        model = get_model()
        latex_formula = model(image)

        md_formula = f"$$\n{latex_formula}\n$$"
        html_formula = f"\\[{latex_formula}\\]"

        st.divider()
        res_left, res_right = st.columns(2)
        res_left.caption("LaTeX Formula")
        res_left.latex(latex_formula)

        res_right.text_area("OCR Output", latex_formula)
        b1, b2, b3 = res_right.columns(3)
        with b1:
            st_copy_to_clipboard(latex_formula, before_copy_label="Copy as LaTeX", after_copy_label="✅Copied!")
        with b2:
            st_copy_to_clipboard(md_formula, before_copy_label="Copy as Markdown", after_copy_label="✅Copied!")
        with b3:
            st_copy_to_clipboard(html_formula, before_copy_label="Copy as HTML", after_copy_label="✅Copied!")


def gpt2md(text):
    return text.replace(r"\[ ", "$$").replace(r"\[", "$$").replace(r" \]", "$$").replace(r"\]", "$$").replace(
        r"\( ", "$").replace(r"\(", "$").replace(r" \)", "$").replace(r"\)", "$")


if __name__ == "__main__":
    main()
