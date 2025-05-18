import json
from pathlib import Path
import spacy
import weaviate
import typer
from rich.progress import track

app = typer.Typer(help="Tag entities and update Weaviate schema")

ENTITY_CLASS = "Entity"
PARAGRAPH_CLASS = "Paragraph"

SCHEMA_ENTITY = {
    "class": ENTITY_CLASS,
    "properties": [
        {"name": "name", "dataType": ["text"]},
        {"name": "type", "dataType": ["text"]},
    ],
}

@app.command()
def tag(clean_jsonl: Path, weaviate_url: str = "http://localhost:8080"):
    nlp = spacy.load("en_core_web_sm")
    client = weaviate.Client(weaviate_url)
    if not client.schema.contains({"class": ENTITY_CLASS}):
        client.schema.create_class(SCHEMA_ENTITY)

    with open(clean_jsonl, 'r', encoding='utf-8') as f:
        for line in track(f, description="Tagging"):
            data = json.loads(line)
            doc = nlp(data["text"])
            for ent in doc.ents:
                if ent.label_ in {"ORG", "PRODUCT", "NORP"}:
                    client.data_object.create_if_not_exists(
                        data_object={"name": ent.text, "type": ent.label_},
                        class_name=ENTITY_CLASS,
                        uuid=weaviate.util.generate_uuid5(ent.text),
                    )
                    # TODO: link paragraph->entity by searching paragraph via metadata

if __name__ == "__main__":
    app()
