from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from PyPDF2 import PdfReader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.callbacks import get_openai_callback
import os
import pickle

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>🤗💬 LLM ChatPDF App</title>
        </head>
        <body>
            <h1>🤗💬 LLM ChatPDF App</h1>
            <p>This app is an LLM-powered chatbot built using:</p>
            <ul>
                <li><a href="https://streamlit.io/">Streamlit</a></li>
                <li><a href="https://python.fastapi.com/">FastAPI</a></li>
                <li><a href="https://platform.openai.com/docs/models">OpenAI</a> LLM model</li>
            </ul>
            <p>Made with ❤️ by Megha Anil</a></p>
        </body>
    </html>
    """

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_reader = PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text=text)

    store_name = file.filename[:-4]

    if os.path.exists(f"{store_name}.pkl"):
        with open(f"{store_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)
    else:
        embeddings = OpenAIEmbeddings()
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        with open(f"{store_name}.pkl", "wb") as f:
            pickle.dump(VectorStore, f)

    return {"message": "PDF uploaded successfully"}

@app.post("/query/")
async def query_pdf(query: str = Form(...)):
    # Implement your query logic here
    return {"query": query}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
