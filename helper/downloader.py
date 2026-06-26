
from urllib.request import urlretrieve
import os
from anyio import Path


CURR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURR_DIR)
VNCORENLP_DIR = os.path.join(BASE_DIR, "vncorenlp", "VnCoreNLP")
MODELS_DIR = os.path.join(VNCORENLP_DIR, "models")
JAR_PATH = os.path.join(VNCORENLP_DIR, "VnCoreNLP-1.2.jar")

REMOTE_BASE = "https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master"

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