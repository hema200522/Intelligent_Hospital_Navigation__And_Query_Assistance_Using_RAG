from pathlib import Path

def load_documents(folder):
    documents = []

    for file in Path(folder).glob("*.txt"):
        text = file.read_text(encoding="utf-8")

        documents.append({
            "source": file.name,
            "text": text
        })

    return documents