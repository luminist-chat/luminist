from typing import List

TOKEN_LIMIT = 800

def chunk_text(text: str) -> List[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = []
    length = 0
    for para in paragraphs:
        tokens = len(para.split())
        if length + tokens > TOKEN_LIMIT and current:
            chunks.append("\n\n".join(current))
            current = [para]
            length = tokens
        else:
            current.append(para)
            length += tokens
    if current:
        chunks.append("\n\n".join(current))
    return chunks
