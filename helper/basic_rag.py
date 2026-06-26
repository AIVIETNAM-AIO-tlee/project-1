import pypdf
import chromadb
import ollama
import os
import streamlit as st

try:
    if "OLLAMA_HOST" in st.secrets:
        os.environ["OLLAMA_HOST"] = st.secrets["OLLAMA_HOST"]
        os.environ["OLLAMA_HEADERS"] = '{"ngrok-skip-browser-warning": "true"}'
except Exception:
    pass

LLM_MODEL = "vicuna:7b-v1.5-q5_1"
EMBEDDING_MODEL = "bge-m3:latest"
PROMPT="""Bạn là trợ lý hỏi đáp. Dùng các đoạn ngữ cảnh dưới đây để trả lời câu hỏi.
Nếu ngữ cảnh không có thông tin, hãy nói là bạn không biết, đừng bịa.
Trả lời ngắn gọn, chính xác, bằng tiếng Việt.

Ngữ cảnh:
{context}

Câu hỏi: {question}

Trả lời:"""


class rag_architecture:
    def __init__(self, llm_model=LLM_MODEL, embedding_model=EMBEDDING_MODEL):
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("rag_collection")

    def chunk_text(self, text, size=1000, overlap=200):
        paras = [p.strip() for p in text.split("\n") if p.strip()] # page 1 \n page 2
        chunks, cur = [], ""
        for p in paras:
            # Nếu một đoạn dài hơn size, cắt nhỏ đoạn đó (vẫn giữ overlap)
            while len(p) > size: # pages 1: 2000 => 1000 (-200) => 800
                if cur:
                    chunks.append(cur.strip())
                    cur = ""
                chunks.append(p[:size].strip())
                p = p[size - overlap:]
            if len(cur) + len(p) + 1 <= size:
                cur += p + "\n"
            else:
                if cur:
                    chunks.append(cur.strip())
                cur = (cur[-overlap:] + p + "\n") if overlap else (p + "\n")
        if cur.strip():
            chunks.append(cur.strip())
        return chunks

    def embed_text(self, texts):
        # Tạo embedding cho văn bản
        embedding = ollama.embed(model=self.embedding_model,input=texts,)['embeddings']

        return embedding
    
    def read_file(self, file):
        # vì chat_input hỗ trợ upload file, nma nó là list, nên lấy file đầu tiên (index = 0)
        if isinstance(file, list):
            file = file[0]
        reader = pypdf.PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages])

        return text
    
    def process_pdf(self, file):
        text = self.read_file(file)
        chunks = self.chunk_text(text)
        
        self.collection.add(
            ids=[str(i) for i in range(len(chunks))],
            documents=chunks,
            embeddings=self.embed_text(chunks)
        )

        return self.collection, len(chunks)

    def retrieval(self, question, top_k=2):
        query = self.collection.query(query_embeddings=self.embed_text([question]), n_results=top_k)

        context = "\n".join(query["documents"][0])
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{
                "role":"user",
                "content": PROMPT.format(context=context, question=question),
                }],
            options={"temperature":0},
        )
        return response.message.content