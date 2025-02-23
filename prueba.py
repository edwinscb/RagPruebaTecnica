from src.database import get_documents

for doc in get_documents():
    print(doc[0], "-", doc[1])  # Imprime ID y nombre del documento
