import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sentence_transformers import SentenceTransformer
from db.database import search_similar_documents

# Cargar el modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query, top_k=4):
    """Busca los fragmentos más relevantes a una consulta en español."""
    try:
        query_embedding = model.encode(query)  # Convertir consulta en embedding
        results = search_similar_documents(query_embedding, top_k)

        if results is None:
            return []
        
        return results
    except Exception as e:
        print(f"⚠️ Error en search(): {e}")
        return []
    
if __name__ == "__main__":
    consulta = input("🔎 Ingrese su consulta: ")
    search(consulta)
