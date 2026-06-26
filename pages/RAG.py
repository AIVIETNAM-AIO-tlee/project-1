import streamlit as st
import helper.basic_rag
import ollama

# tạo object RAG
@st.cache_resource
def get_rag():
    return helper.basic_rag.rag_architecture()

rag = get_rag()

st.badge("Version 1.0", color="blue")

st.title("Chat cùng AI 😼", text_alignment="center")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    if st.button("Xóa lịch sử chat", use_container_width=True):
        st.session_state.chat_history = []
        if "collection" in st.session_state:
            del st.session_state.collection


with st.chat_message(name="ai"):
    st.write("Xin chào, tôi là AI học tập. Tôi có thể giúp gì cho bạn hôm nay?")

for m in st.session_state.chat_history:
            with st.chat_message(name=m["role"]):
                st.write(m["content"])

user_question = st.chat_input("Nhập câu hỏi của bạn vào đây...", accept_file = True, file_type="pdf")

if user_question:
    # khúc này do trong chat_input hỗ trợ upload file luôn, nên mình áp dụng vô và lấy files
    # từ user_question.files, còn text thì lấy từ user_question.text
    user_text = user_question.text
    user_file = user_question.files

    with st.chat_message(name="user"):
            if user_text:
                st.write(user_text)
                st.session_state.chat_history.append({"role": "user", "content": user_text})

            
            if user_file:
                with st.status("Đang xử lý file PDF, bạn chờ tí nhé 😸", expanded=True):
                    st.session_state.collection, n = rag.process_pdf(user_file)
                    st.session_state.pdf_name = user_file[0].name
                    st.info(f"Xử lý file PDF thành công - {user_file[0].name} ❤️",)

    if user_text or user_file:
        with st.chat_message(name="ai"):
            with st.spinner("Đang suy nghĩ..."):
                
                if "collection" in st.session_state and st.session_state.collection is not None:
                    answer = rag.retrieval(user_text)
                else:
                    # trường hợp PDF mà người dùng chưa gửi câu hỏi thì AI tóm tắt giúp.
                    res = ollama.chat(
                        model=rag.llm_model,
                        messages=[{"role": "user", "content": user_text if user_text else "Tóm tắt tài liệu vừa gửi"}]
                    )
                    print(res)
                    answer = res['message']['content']

                st.write(answer)
        
        st.session_state.chat_history.append({"role": "ai", "content": answer})

        
