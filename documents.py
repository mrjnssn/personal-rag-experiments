from pathlib import Path

from config import DOCUMENTS_FOLDER


def read_txt(file_path):
    return file_path.read_text(encoding="utf-8")


def load_documents():
    documents = []

    folder = Path(DOCUMENTS_FOLDER)

    for file_path in folder.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "filename": file_path.name,
            "text": text
        })
    
    return documents
