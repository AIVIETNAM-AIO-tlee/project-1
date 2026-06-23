import streamlit as st
from analysis import *
import time


# cấu hình gồm title, icon với layout
st.set_page_config(
    page_title="Analyze Student Scores",
    page_icon="images/LeetCode_logo.png",
    layout="wide"
)

st.badge("Version 1.0", color="blue")

st.title("Phân tích dữ liệu điểm số học sinh", text_alignment="center")
   
st.header("Tải lên tệp CSV bảng điểm",divider="blue")


uploaded_file = st.file_uploader("Tải lên tệp",type=["csv"])

if uploaded_file is not None:
    data = load_data(uploaded_file)

    # tạo hiệu ứng cho vui
    with st.spinner("Đang phân tích dữ liệu...", show_time=True):
        time.sleep(1.5)
        st.balloons()

    st.subheader("Dữ liệu đã tải lên")
    st.dataframe(data)
    st.subheader("Kết quả phân tích dữ liệu")

    # Kết quả tổng quan cho dữ liệu
    st.write("Điểm trung bình: ", calculate_average_score(data), "Số lượng học sinh: ", len(data))
    st.write("Điểm trung vị: ", calculate_median_score(data))
    st.write("Điểm thấp nhất: ", get_min_max_scores(data)[0], "Điểm cao nhất: ", get_min_max_scores(data)[1])
    col1, col2 = st.columns(2)

    with col1:
        # Biểu đồ cột
        st.markdown("#### Biểu đồ phân phối điểm số",text_alignment="center")
        st.bar_chart(get_score_distribution(data), x_label="Khoảng điểm", y_label="Số lượng học sinh")
    with col2:
        # Biểu đồ đường
        st.markdown("#### Biểu đồ đường phân phối điểm số",text_alignment="center")
        st.line_chart(get_score_distribution(data), x_label="Khoảng điểm", y_label="Số lượng học sinh")


    # lọc học sinh
    threshold = st.slider("Lọc điểm số học sinh", 0, 10, 0)
    filter_students = data[data['Điểm số'] >= threshold]

    st.markdown(f"#### Danh sách học sinh có điểm số từ {threshold} trở lên")
    st.dataframe(filter_students)