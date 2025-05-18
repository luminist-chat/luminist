import os
from datetime import datetime
from typing import List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import weaviate
from langchain.chains import RetrievalQA
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Weaviate

app = FastAPI()
app.mount("/static", StaticFiles(directory="data/pdf"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Document(BaseModel):
    document_id: str
    content: str

class Message(BaseModel):
    message_id: str
    content: str
    role: str
    created_at: datetime

class Conversation(BaseModel):
    conversation_id: str
    messages: List[Message]

class Space(BaseModel):
    space_id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    documents: List[Document]
    conversations: List[Conversation]

# Create a new knowledge space
@app.post("/space")
# Return a Space object
def create_space():
    return Space(space_id="123",name="My Space", description="My Space Description", created_at=datetime.now(), updated_at=datetime.now(), documents=[], conversations=[])

@app.get("/space/{space_id}")
def get_space(space_id: str):
    return Space(space_id=space_id, name="My Space", description="My Space Description", created_at=datetime.now(), updated_at=datetime.now(), documents=[], conversations=[])

@app.post("/space/{space_id}/document")
def create_document(space_id: str, document: str):
    return Document(document_id="123", content=document)

# Create a new conversation
@app.post("space/{space_id}/conversation")
def create_conversation(space_id: str):
    return Conversation(conversation_id="123", messages=[])

# Chat in a conversation
@app.post("/space/{space_id}/conversation/{conversation_id}")
def chat(space_id: str, conversation_id: str, message: str):
    return Message(message_id="123", content=message, role="user", created_at=datetime.now())

@app.get("/health")
def health():
    return {"status": "ok"}


class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    weaviate_host = os.environ.get("WEAVIATE_HOST", "http://localhost:8080")
    client = weaviate.Client(weaviate_host)
    embeddings = OpenAIEmbeddings()
    vectordb = Weaviate(client, index_name="Paragraph", text_key="text", embedding=embeddings)

    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_kwargs={"k": 6}),
        return_source_documents=True,
    )

    result = qa.invoke({"query": query.question})
    docs = result["source_documents"]
    citations = []
    entities = set()
    for d in docs:
        file = d.metadata.get("file")
        page = d.metadata.get("page")
        citations.append({
            "file": file,
            "page": page,
            "link": f"/static/{file}#page={page}",
        })
        ent_res = client.query.get("Paragraph", ["mentions"])
        ent_res = ent_res.with_where({"path": ["file"], "operator": "Equal", "valueText": file})
        ent_res = ent_res.with_limit(1)
        data = ent_res.do()
        if data.get("data", {}).get("Get", {}).get("Paragraph"):
            for p in data["data"]["Get"]["Paragraph"]:
                for e in p.get("mentions", []):
                    entities.add(e.get("name"))

    return {"answer": result["result"], "citations": citations, "entities": sorted(entities)}

