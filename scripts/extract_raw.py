import json
import os
from pathlib import Path
import pdfplumber
import typer
from rich.progress import track

app = typer.Typer(help="Extract raw text from PDFs into JSONL")

@app.command()
def extract(pdf_dir: Path, output: Path):
    lines = []
    for pdf_path in track(sorted(Path(pdf_dir).glob('*.pdf')), description="Processing PDFs"):
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                lines.append({"file": pdf_path.name, "page": i, "text": text})
    with open(output, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(json.dumps(line, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    app()
