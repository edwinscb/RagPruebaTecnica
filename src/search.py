import numpy as np
from sentence_transformers import SentenceTransformer
from database import search_similar_documents

# Cargar el modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query, top_k=4):
    """Busca los fragmentos más relevantes a una consulta en español."""
    query_embedding = model.encode(query)  # Convertir consulta en embedding
    results = search_similar_documents(query_embedding, top_k)

    print("\n🔍 Resultados de la búsqueda:")
    for doc_id, nombre_archivo, contenido_texto in results:
        print(f"\n📄 Documento: {nombre_archivo}\n📝 Fragmento: {contenido_texto[:300]}...")  # Mostrar solo 300 caracteres
    
if __name__ == "__main__":
    consulta = input("🔎 Ingrese su consulta: ")
    search(consulta)
