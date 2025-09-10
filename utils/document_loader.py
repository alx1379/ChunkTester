from pathlib import Path

def load_all_documents(folder: str) -> list[dict]:
    """
    Loads all .txt files from a folder and returns a list of dictionaries:
    {"name": <filename>, "text": <content>}
    """
    docs = []
    for path in Path(folder).glob("*.txt"):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        docs.append({"name": path.name, "text": text})
    return docs
