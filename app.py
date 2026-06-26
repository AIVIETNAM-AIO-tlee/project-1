import streamlit as st
from helper.analysis import *

analysis_page = st.Page("pages/Analysis_Student_Score.py", title="Phân tích dữ liệu điểm số học sinh", icon=":material/analytics:",)
nlp_page = st.Page("pages/NLP_T2S.py", title="NLP Text to Speech", icon=":material/speaker:",)
rag_page =st.Page("pages/RAG.py", title="RAG Cơ bản", icon=":material/question_answer:",)

pg = st.navigation({
    "Analysis": [analysis_page],
    "NLP Learning": [nlp_page],
    "RAG": [rag_page]
}, position="sidebar",)

# cấu hình gồm title, icon với layout
st.set_page_config(page_title="General Streamlit App", page_icon="images/LeetCode_logo.png", layout="wide")

pg.run()