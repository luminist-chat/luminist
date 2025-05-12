from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

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
