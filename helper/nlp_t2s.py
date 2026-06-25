from gtts import gTTS
from py_vncorenlp import VnCoreNLP
import os 
import streamlit as st
from pathlib import Path
from urllib.request import urlretrieve

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURR_DIR)
VNCORENLP_DIR = os.path.join(BASE_DIR, "vncorenlp", "VnCoreNLP")
MODELS_DIR = os.path.join(VNCORENLP_DIR, "models")
JAR_PATH = os.path.join(VNCORENLP_DIR, "VnCoreNLP-1.2.jar")
REMOTE_BASE = "https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master"

if os.name == "nt":
    os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jre-1.8"


def _download_file(url, destination):
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(url, destination)


def _ensure_vncorenlp_bundle():
    os.makedirs(VNCORENLP_DIR, exist_ok=True)
    if os.path.isdir(MODELS_DIR) and os.path.exists(JAR_PATH):
        return

    os.makedirs(os.path.join(MODELS_DIR, "dep"), exist_ok=True)
    os.makedirs(os.path.join(MODELS_DIR, "ner"), exist_ok=True)
    os.makedirs(os.path.join(MODELS_DIR, "postagger"), exist_ok=True)
    os.makedirs(os.path.join(MODELS_DIR, "wordsegmenter"), exist_ok=True)

    assets = [
        ("VnCoreNLP-1.2.jar", "VnCoreNLP-1.2.jar"),
        ("models/wordsegmenter/vi-vocab", "models/wordsegmenter/vi-vocab"),
        ("models/wordsegmenter/wordsegmenter.rdr", "models/wordsegmenter/wordsegmenter.rdr"),
        ("models/postagger/vi-tagger", "models/postagger/vi-tagger"),
        ("models/ner/vi-500brownclusters.xz", "models/ner/vi-500brownclusters.xz"),
        ("models/ner/vi-ner.xz", "models/ner/vi-ner.xz"),
        ("models/ner/vi-pretrainedembeddings.xz", "models/ner/vi-pretrainedembeddings.xz"),
        ("models/dep/vi-dep.xz", "models/dep/vi-dep.xz"),
    ]

    for remote_path, local_path in assets:
        local_file = os.path.join(VNCORENLP_DIR, local_path)
        if not os.path.exists(local_file):
            _download_file(f"{REMOTE_BASE}/{remote_path}", local_file)


@st.cache_resource
def load_model():
    _ensure_vncorenlp_bundle()
    return VnCoreNLP(save_dir=VNCORENLP_DIR, annotators=["wseg"])


def get_model():
    return load_model()

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
    model = get_model()

    # tách thành token
    tokens = model.word_segment(text)

    # xử lý các token trong corpus của Vn trường hợp mà có dấu _
    tokens = [token.replace("_", " ") for token in tokens]

    # thay mapping 1 số từ không có trong từ điển corpus
    tokens = [mapping.get(tok, tok) for tok in tokens]
    return tokens, model.annotate_text(text)

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
    