import json
from pathlib import Path

import openai
import weaviate
import typer
from rich.progress import track

from utils.chunk import chunk_text

app = typer.Typer(help="Load cleaned chunks into Weaviate")

CLASS_NAME = "Paragraph"

SCHEMA = {
    "class": CLASS_NAME,
    "vectorizer": "none",
    "properties": [
        {"name": "text", "dataType": ["text"]},
        {"name": "file", "dataType": ["text"]},
        {"name": "page", "dataType": ["int"]},
    ],
}

@app.command()
def load(clean_jsonl: Path, weaviate_url: str = "http://localhost:8080"):
    client = weaviate.Client(weaviate_url)
    if not client.schema.contains({"class": CLASS_NAME}):
        client.schema.create_class(SCHEMA)

    openai_client = openai.OpenAI()

    batch = client.batch
    batch.batch_size = 100
    with batch as b, open(clean_jsonl, 'r', encoding='utf-8') as f:
        for line in track(f, description="Uploading"):
            data = json.loads(line)
            text = data["text"]
            chunks = chunk_text(text)
            for chunk in chunks:
                resp = openai_client.embeddings.create(
                    input=chunk,
                    model="text-embedding-3-small",
                )
                vector = resp.data[0].embedding
                b.add_data_object(
                    {
                        "text": chunk,
                        "file": data["file"],
                        "page": data["page"],
                    },
                    CLASS_NAME,
                    vector=vector,
                )

if __name__ == '__main__':
    app()
