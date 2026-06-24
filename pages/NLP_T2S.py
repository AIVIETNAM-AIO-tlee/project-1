import streamlit as st
import time
from helper.nlp_t2s import *
# cái này dùng cho tiếng anh
# import spacy

EXAMPLES = [
    "Hôm nay tôi vui quá",
    "vcl",
    "Xin chào, hôm nay trời đẹp quá.",
]

st.badge("Version 1.0", color="blue")

st.title("NLP Văn bản thành âm thanh😸", text_alignment="center")

with st.expander("Một số câu ví dụ mẫu"):
    for example in EXAMPLES:
        st.markdown(f"- {example}")

text = st.text_area("Nhập văn bản tiếng Việt", height=100, placeholder="Test thử đi nèee...")

if st.button("😼"):
    if text:

        with st.spinner("Đang chuyển văn bản thành âm thanh...", show_time=True):
            time.sleep(1.5)

            tokens, annotated = preprocess_text(text)

            proceed_sentences = flatten_to_text(tokens)
            file = text_to_speech(proceed_sentences)
            st.write(proceed_sentences)
            st.success("Chuyển văn bản thành công", title="Thành công",)
            st.audio(file)

    else: 
        st.warning("Bạn quên nhập text kìa !!!", icon="😹")
        