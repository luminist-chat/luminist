import json
from pathlib import Path
import time
import openai
import typer
from rich.progress import track

app = typer.Typer(help="Clean raw extracted text using GPT-3.5")

SYSTEM_PROMPT = (
    "Clean this RPG rulebook text: remove headers, footers, page numbers, "
    "and redundant whitespace. Return plain text."
)

@app.command()
def clean(input_jsonl: Path, output_jsonl: Path):
    client = openai.OpenAI()
    with open(output_jsonl, 'w', encoding='utf-8') as outf:
        with open(input_jsonl, 'r', encoding='utf-8') as inf:
            for line in track(inf, description="Cleaning"):
                data = json.loads(line)
                text = data.get('text', '')
                for attempt in range(5):
                    try:
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": text},
                            ],
                        )
                        cleaned = response.choices[0].message.content.strip()
                        break
                    except Exception as e:
                        wait = 2 ** attempt
                        time.sleep(wait)
                else:
                    cleaned = text
                data['text'] = cleaned
                outf.write(json.dumps(data, ensure_ascii=False) + '\n')
                time.sleep(1.0)

if __name__ == '__main__':
    app()
