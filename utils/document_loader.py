from pathlib import Path

def load_all_documents(folder: str) -> list[dict]:
    """
    Загружает все .txt файлы из папки и возвращает список словарей:
    {"name": <имя файла>, "text": <содержимое>}
    """
    docs = []
    for path in Path(folder).glob("*.txt"):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        docs.append({"name": path.name, "text": text})
    return docs
