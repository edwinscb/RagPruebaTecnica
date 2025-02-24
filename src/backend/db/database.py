import sqlite3
import numpy as np
from sentence_transformers.util import cos_sim

DB_PATH = "data/extracted_text.db"

def create_db():
    """Crea la base de datos y las tablas si no existen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla para texto
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT UNIQUE,
            contenido_texto TEXT
        )
    """)
    
    # Tabla para embeddings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER,
            embedding BLOB,
            FOREIGN KEY (doc_id) REFERENCES documentos(id)
        )
    """)
    
    conn.commit()
    conn.close()

def insert_document(nombre_archivo, contenido_texto):
    """Inserta un documento en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO documentos (nombre_archivo, contenido_texto) VALUES (?, ?)", 
                       (nombre_archivo, contenido_texto))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"El archivo {nombre_archivo} ya está en la base de datos.")
    conn.close()

def get_documents():
    """Recupera todos los documentos almacenados en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre_archivo, contenido_texto FROM documentos")
    documentos = cursor.fetchall()
    
    conn.close()
    return documentos

def insert_embedding(doc_id, embedding):
    """Guarda el embedding en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convertir embedding a bytes para almacenamiento
    embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
    
    cursor.execute("INSERT INTO embeddings (doc_id, embedding) VALUES (?, ?)", (doc_id, embedding_bytes))
    conn.commit()
    conn.close()

def search_similar_documents(query_embedding, top_k=5):
    """Busca los documentos más similares al embedding de la consulta."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Recuperar embeddings almacenados
    cursor.execute("SELECT doc_id, embedding FROM embeddings")
    rows = cursor.fetchall()

    similarities = []
    for doc_id, embedding_bytes in rows:
        stored_embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        similarity = cos_sim(query_embedding, stored_embedding).item()
        similarities.append((doc_id, similarity))

    # Ordenar por similitud y seleccionar los top_k
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_results = similarities[:top_k]

    # Obtener los textos de los fragmentos más relevantes
    doc_ids = [doc_id for doc_id, _ in top_results]
    placeholders = ",".join("?" * len(doc_ids))
    cursor.execute(f"SELECT id, nombre_archivo, contenido_texto FROM documentos WHERE id IN ({placeholders})", doc_ids)
    top_documents = cursor.fetchall()

    conn.close()
    return top_documents
