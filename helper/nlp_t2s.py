from gtts import gTTS
from py_vncorenlp import VnCoreNLP
import py_vncorenlp
import os 
import streamlit as st

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURR_DIR)
VNCORENLP_DIR = os.path.join(BASE_DIR, "vncorenlp/VnCoreNLP")
MODELS_DIR = os.path.join(VNCORENLP_DIR, "models")


py_vncorenlp.download_model(save_dir=VNCORENLP_DIR)

if os.name == "nt":
    os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jre-1.8"


@st.cache_resource
def load_model():
    return VnCoreNLP(save_dir=VNCORENLP_DIR, annotators=["wseg"])
model = load_model()

mapping = {
    "0-4": "Điểm số từ 0 đến 4",
    "5-6": "Điểm số từ 5 đến 6",
    "7-8": "Điểm số từ 7 đến 8",
    "9-10": "Điểm số từ 9 đến 10",
    "vcl": "vui cười lên",
    "ck": "chuyển khoản"
}

def preprocess_text(text):
    text = text.lower().strip() # bỏ khoảng trắng đầu cuối và chuẩn hóa về dạng chữ thường

    # tách thành token
    tokens = model.word_segment(text)

    # xử lý các token trong corpus của Vn trường hợp mà có dấu _
    tokens = [token.replace("_", " ") for token in tokens]

    # thay mapping 1 số từ không có trong từ điển corpus
    tokens = [mapping.get(tok, tok) for tok in tokens]
    print("Tokens:", tokens) # debug
    annotated = model.annotate_text(text)
    print("Annotated:", annotated) # debug
    return tokens, annotated

def flatten_to_text(tokens):
    sentences = ""
    for sent in tokens:
        sentences += "".join(sent)
    print("Flattened sentences:", sentences) # debug
    return sentences

def text_to_speech(text, lang='vi'):
    # chuyển text sang speech
    tts = gTTS(text=text, lang=lang)
    file = "output.mp3"
    tts.save(file)
    return file
    