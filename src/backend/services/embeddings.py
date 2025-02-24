import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sentence_transformers import SentenceTransformer
from backend.db.database import get_documents, insert_embedding

# Cargar el modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings():
    """Genera y almacena embeddings para cada fragmento en la base de datos."""
    documentos = get_documents()
    
    for doc_id, nombre_archivo, contenido_texto in documentos:
        embedding = model.encode(contenido_texto)  # Genera el embedding
        insert_embedding(doc_id, embedding)  # Guarda el embedding en la BD
        print(f"Embedding almacenado para {nombre_archivo}")

if __name__ == "__main__":
    generate_embeddings()
